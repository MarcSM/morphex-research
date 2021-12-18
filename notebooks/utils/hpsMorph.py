# function to call the main analysis/synthesis functions in software/models/hpsModel.py

import sys, os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import get_window
sys.path.append('/sms-tools/software/models')
import utilFunctions as UF
import hpsModel as HPS
from scipy.interpolate import interp1d
#sys.path.append('/sms-tools/software/transformations')
#import hpsTransformations as HPST

DARK_MODE = True

NS = 512 # size of fft used in synthesis
H = 128 # hop size (has to be 1/4 of NS)

def hpsMorphFrame(hfreq1, hmag1, stocEnv1, hfreq2, hmag2, stocEnv2, hfreqIntp, hmagIntp, stocIntp):
    
    # create empty output matrix
    yhfreq = np.zeros_like(hfreq1)

    # create empty output matrix
    yhmag = np.zeros_like(hmag1)

    # create empty output matrix
    ystocEnv = np.zeros_like(stocEnv1)

    # For each frame in the audio file
    for freqs_frame in zip(hfreq1, hfreq2):

        #print(freqs_frame[1])

        #harmonics = np.intersect1d(np.array(np.nonzero(hfreq1[l,:]), dtype=np.int)[0], np.array(np.nonzero(hfreq2[int(round(L2*l/float(L1))),:]), dtype=np.int)[0])

        # identify harmonics that are present in both frames
        harmonics = np.intersect1d(np.array(np.nonzero(freqs_frame[0]), dtype=np.int)[0], np.array(np.nonzero(freqs_frame[1]), dtype=np.int)[0])

        # interpolate the frequencies of the existing harmonics
        yhfreq[harmonics] =  (1-hfreqIntp) * hfreq1[harmonics] + hfreqIntp * hfreq2[harmonics]

        # interpolate the magnitudes of the existing harmonics
        yhmag[harmonics] = (1-hmagIntp) * hmag1[harmonics] + hmagIntp * hmag2[harmonics]

        

def hpsMorph(hfreq1, hmag1, stocEnv1, hfreq2, hmag2, stocEnv2, hfreqIntp, hmagIntp, stocIntp):
    """
    Morph between two sounds using the harmonic plus stochastic model
    hfreq1, hmag1, stocEnv1: hps representation of sound 1
    hfreq2, hmag2, stocEnv2: hps representation of sound 2
    hfreqIntp: interpolation factor between the harmonic frequencies of the two sounds, 0 is sound 1 and 1 is sound 2 (time,value pairs)
    hmagIntp: interpolation factor between the harmonic magnitudes of the two sounds, 0 is sound 1 and 1 is sound 2  (time,value pairs)
    stocIntp: interpolation factor between the stochastic representation of the two sounds, 0 is sound 1 and 1 is sound 2  (time,value pairs)
    returns yhfreq, yhmag, ystocEnv: hps output representation
    """

    L1 = hfreq1[:,0].size # number of frames of sound 1
    L2 =  hfreq2[:,0].size # number of frames of sound 2
    hfreqIntp = (L1-1)*hfreqIntp/hfreqIntp # normalize input values
    hmagIntp = (L1-1)*hmagIntp/hmagIntp # normalize input values
    stocIntp = (L1-1)*stocIntp/stocIntp # normalize input values
    
    # interpolation function
    hfreqIntpEnv = interp1d(hfreqIntp[0::2], hfreqIntp[1::2], fill_value=0)
    
    # generate frame indexes for the output
    hfreqIndexes = hfreqIntpEnv(np.arange(L1))
    
    # interpolation function
    hmagIntpEnv = interp1d(hmagIntp[0::2], hmagIntp[1::2], fill_value=0)
    
    # generate frame indexes for the output
    hmagIndexes = hmagIntpEnv(np.arange(L1))
    
    # interpolation function
    stocIntpEnv = interp1d(stocIntp[0::2], stocIntp[1::2], fill_value=0)
    
    # generate frame indexes for the output
    stocIndexes = stocIntpEnv(np.arange(L1))                 
    
    # create empty output matrix
    yhfreq = np.zeros_like(hfreq1)
    
    # create empty output matrix
    yhmag = np.zeros_like(hmag1)
    
    # create empty output matrix
    ystocEnv = np.zeros_like(stocEnv1)

    # generate morphed frames
    for l in range(L1):
        # identify harmonics that are present in both frames
        harmonics = np.intersect1d(np.array(np.nonzero(hfreq1[l,:]), dtype=np.int)[0], np.array(np.nonzero(hfreq2[int(round(L2*l/float(L1))),:]), dtype=np.int)[0])
        # interpolate the frequencies of the existing harmonics
        yhfreq[l,harmonics] =  (1-hfreqIndexes[l])* hfreq1[l,harmonics] + hfreqIndexes[l] * hfreq2[int(round(L2*l/float(L1))),harmonics]
        # interpolate the magnitudes of the existing harmonics
        yhmag[l,harmonics] =  (1-hmagIndexes[l])* hmag1[l,harmonics] + hmagIndexes[l] * hmag2[int(round(L2*l/float(L1))),harmonics]
        # interpolate the stochastic envelopes of both frames
        ystocEnv[l,:] =  (1-stocIndexes[l])* stocEnv1[l,:] + stocIndexes[l] * stocEnv2[int(round(L2*l/float(L1))),:]
    return yhfreq, yhmag, ystocEnv

def transformation_synthesis(sound_1=None, sound_2=None, sound_morph=None,
                             morphingOutputPath="morphing_output"):
    """
    Transform the analysis values returned by the analysis function and synthesize the sound
    inputFile1: name of input file 1
    fs: sampling rate of input file	1
    hfreq1, hmag1, stocEnv1: hps representation of sound 1
    inputFile2: name of input file 2
    hfreq2, hmag2, stocEnv2: hps representation of sound 2
    hfreqIntp: interpolation factor between the harmonic frequencies of the two sounds, 0 is sound 1 and 1 is sound 2 (time,value pairs)
    hmagIntp: interpolation factor between the harmonic magnitudes of the two sounds, 0 is sound 1 and 1 is sound 2  (time,value pairs)
    stocIntp: interpolation factor between the stochastic representation of the two sounds, 0 is sound 1 and 1 is sound 2  (time,value pairs)
    """

    if not sound_1.had_file_loaded: raise Exception("Sound 1 is not loaded")
    if not sound_2.had_file_loaded: raise Exception("Sound 2 is not loaded")
    
    fs = sound_morph.fs = int(sound_1.fs)

    inputFile1 = sound_1.path
    hfreq1 = sound_1.analysis.output.values.hfreq
    hmag1 = sound_1.analysis.output.values.hmag
    stocEnv1 = sound_1.analysis.output.values.stocEnv
    inputFile2 = sound_2.path
    hfreq2 = sound_2.analysis.output.values.hfreq
    hmag2 = sound_2.analysis.output.values.hmag
    stocEnv2 = sound_2.analysis.output.values.stocEnv
    hfreqIntp = sound_morph.harmonic_frequencies.value
    hmagIntp = sound_morph.harmonic_magnitudes.value
    stocIntp = sound_morph.stochastic_component.value

    # morph the two sounds
    yhfreq, yhmag, ystocEnv = hpsMorph(hfreq1, hmag1, stocEnv1, hfreq2, hmag2, stocEnv2, hfreqIntp, hmagIntp, stocIntp)

    # empty phases
    yhphase = np.array([])
    
    # saving these values for the plotting part
    sound_morph.analysis.output.values.hfreq = yhfreq
    sound_morph.analysis.output.values.hmag = yhmag
    sound_morph.analysis.output.values.hphase = yhphase
    sound_morph.analysis.output.values.stocEnv = ystocEnv

    # synthesis 
    y, yh, yst = HPS.hpsModelSynth(yhfreq, yhmag, yhphase, ystocEnv, NS, H, fs)

    # saving these values for the plotting part
    sound_morph.synthesis.output.values.y = y
    sound_morph.synthesis.output.values.yh = yh
    sound_morph.synthesis.output.values.yst = yst

    # creating the directory if does not exist already
    if not os.path.isdir(morphingOutputPath): os.makedirs(morphingOutputPath)

    # write output sound
    outputFile = morphingOutputPath + '/' + os.path.basename(sound_1.path)[:-4] + '_hpsMorph.wav'

    sound_morph.synthesis.output.path = outputFile

    # write sound file
    UF.wavwrite(y, fs, outputFile)

    # Loading the sound object
    sound_morph.load(outputFile)

def plot_transformation_synthesis(gui, sound_morph):

    # frequency range to plot
    maxplotfreq = 15000.0

    fs = sound_morph.fs

    yhfreq = sound_morph.analysis.output.values.hfreq
    yhmag = sound_morph.analysis.output.values.hmag
    yhphase = sound_morph.analysis.output.values.hphase
    ystocEnv = sound_morph.analysis.output.values.stocEnv

    y = sound_morph.synthesis.output.values.y
    yh = sound_morph.synthesis.output.values.yh
    yst = sound_morph.synthesis.output.values.yst

    try: gui.plots_results.clear()
    except Exception: pass

    gui.plots_results = plt.figure(num='Generated file analysis ' + sound_morph.name + sound_morph.extension, figsize=(8.5, 6)) # 8.25
    # gui.plots_results.suptitle(sound_morph.name + sound_morph.extension, fontsize=16)

    if (DARK_MODE):
        params = {
            "text.color" : "w",
            "ytick.color" : "w",
            "xtick.color" : "w",
            "axes.labelcolor" : "w",
            "axes.edgecolor" : "w",
            "axes.facecolor" : 'e5e5e5'
        }
        plt.rcParams.update(params)
        gui.plots_results.patch.set_facecolor('#373e4b')

    # plot spectrogram of transformed stochastic compoment
    ax1 = gui.plots_results.add_subplot(211)
    numFrames = int(ystocEnv[:,0].size)
    sizeEnv = int(ystocEnv[0,:].size)
    frmTime = H*np.arange(numFrames)/float(fs)
    binFreq = (.5*fs)*np.arange(sizeEnv*maxplotfreq/(.5*fs))/sizeEnv                      
    ax1.pcolormesh(frmTime, binFreq, np.transpose(ystocEnv[:,:int(sizeEnv*maxplotfreq/(.5*fs))+1]))
    ax1.autoscale(tight=True)

    # plot transformed harmonic on top of stochastic spectrogram
    if (yhfreq.shape[1] > 0):
        harms = np.copy(yhfreq)
        harms = harms*np.less(harms,maxplotfreq)
        harms[harms==0] = np.nan
        numFrames = int(harms[:,0].size)
        frmTime = H*np.arange(numFrames)/float(fs) 
        ax1.plot(frmTime, harms, color='k', ms=3, alpha=1)
        ax1.set_xlabel('time (sec)')
        ax1.set_ylabel('frequency (Hz)')
        ax1.autoscale(tight=True)
        ax1.set_title('harmonics + stochastic spectrogram')

    # plot the output sound
    ax2 = gui.plots_results.add_subplot(212)
    ax2.plot(np.arange(y.size)/float(fs), y)
    ax2.axis([0, y.size/float(fs), min(y), max(y)])
    ax2.set_ylabel('amplitude')
    ax2.set_xlabel('time (sec)')
    ax2.set_title('output sound: y')

    gui.plots_results.tight_layout()
    gui.plots_results.show()

if __name__ == "__main__":
    analysis()