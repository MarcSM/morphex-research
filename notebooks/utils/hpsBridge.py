# function to call the main analysis/synthesis functions in software/models/hpsModel.py

import sys, os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import get_window
sys.path.append('/sms-tools/software/models')
import utilFunctions as UF
import hpsModel as HPS
sys.path.append('/sms-tools/software/transformations')
import hpsTransformations as HPST

DARK_MODE = True

NS = 512 # size of fft used in synthesis
H = 128 # hop size (has to be 1/4 of NS)

def analysis(sound=None, analysisOutputPath="analysis_output"):
    
    inputFile = sound.path # input sound file (monophonic with sampling rate of 44100)
    window = sound.window_type.value # analysis window type (rectangular, hanning, hamming, blackman, blackmanharris)
    M = sound.window_size.value # analysis window size
    N = sound.fft_size.value # fft size (power of two, bigger or equal than M)
    t = sound.magnitude_threshold.value # magnitude threshold of spectral peaks 
    minSineDur = sound.min_sine_dur.value # minimum duration of sinusoidal tracks
    nH = sound.max_harm.value # maximum number of harmonics 
    minf0 = sound.min_f0.value # minimum fundamental frequency in sound
    maxf0 = sound.max_f0.value # maximum fundamental frequency in sound
    f0et = sound.max_f0_error.value # maximum error accepted in f0 detection algorithm
    harmDevSlope = sound.harm_dev_slope.value # allowed deviation of harmonic tracks, higher harmonics have higher allowed deviation
    stocf = sound.stoc_fact.value # decimation factor used for the stochastic approximation
    
    if sound.analysis_progress: 
        sound.analysis_progress.description='Analyzing'
        sound.analysis_progress.bar_style=''
        sound.analysis_progress.layout.visibility = 'visible'
        sound.analysis_progress.value = 2

    # read input sound
    (fs, x) = UF.wavread(inputFile)

    # compute analysis window
    w = get_window(window, M)
    
    # saving these values for the plotting part
    sound.audio = x
    sound.fs = fs
    sound.window = w
    sound.synthesis_fft_size = NS
    sound.hop_size = H
    
    if sound.analysis_progress: sound.analysis_progress.value = 12
        
    # compute the harmonic plus stochastic model of the whole sound
    hfreq, hmag, hphase, stocEnv = HPS.hpsModelAnal(x, fs, w, N, H, t, nH, minf0, maxf0, f0et, harmDevSlope, minSineDur, NS, stocf)

    # saving these values for the plotting part
    sound.analysis.output.values.hfreq = hfreq
    sound.analysis.output.values.hmag = hmag
    sound.analysis.output.values.hphase = hphase
    sound.analysis.output.values.stocEnv = stocEnv
    
    if sound.analysis_progress: sound.analysis_progress.value = 45
        
    # synthesize a sound from the harmonic plus stochastic representation
    y, yh, yst = HPS.hpsModelSynth(hfreq, hmag, hphase, stocEnv, NS, H, fs)
    
    # saving these values for the plotting part
    sound.synthesis.output.values.y = y
    sound.synthesis.output.values.yh = yh
    sound.synthesis.output.values.yst = yst
    
    # if the output folder does not exists we create it
    #if os.path.exists(analysisOutputPath): os.makedirs(analysisOutputPath)
    
    if sound.analysis_progress: sound.analysis_progress.value = 78
        
    # output sound file (monophonic with sampling rate of 44100)
    outputFileSines = analysisOutputPath + '/' + os.path.basename(inputFile)[:-4] + '_hpsModel_sines.wav'
    outputFileStochastic = analysisOutputPath + '/' + os.path.basename(inputFile)[:-4] + '_hpsModel_stochastic.wav'
    outputFile = analysisOutputPath + '/' + os.path.basename(inputFile)[:-4] + '_hpsModel.wav'
    
    if sound.analysis_progress: sound.analysis_progress.value = 82
    
    sound.synthesis.output.sines.path = outputFileSines
    sound.synthesis.output.stochastic.path = outputFileStochastic
    sound.synthesis.output.mixed.path = outputFile
    
    if sound.analysis_progress: sound.analysis_progress.value = 85
        
    # write sounds files for harmonics, stochastic, and the sum
    UF.wavwrite(yh, fs, outputFileSines)
    if sound.analysis_progress: sound.analysis_progress.value = 90
        
    UF.wavwrite(yst, fs, outputFileStochastic)
    if sound.analysis_progress: sound.analysis_progress.value = 94
        
    UF.wavwrite(y, fs, outputFile)
    if sound.analysis_progress: sound.analysis_progress.value = 98

    # Updating the values for the .had structure
    sound.update_had_values();
    if sound.analysis_progress: sound.analysis_progress.value = 100

def plot_analysis(gui, sound):
    
    # frequency range to plot
    maxplotfreq = 15000.0

    inputFile = sound.path
    window = sound.window_type.value
    M = sound.window_size.value
    N = sound.fft_size.value
    t = sound.magnitude_threshold.value
    minSineDur = sound.min_sine_dur.value
    nH = sound.min_f0.value
    minf0 = sound.max_f0.value
    maxf0 = sound.max_f0_error.value
    f0et = sound.harm_dev_slope.value
    harmDevSlope = sound.max_harm.value
    stocf = sound.stoc_fact.value
    
    x = sound.audio
    fs = sound.fs
    hfreq = sound.analysis.output.values.hfreq
    hmag = sound.analysis.output.values.hmag
    hphase = sound.analysis.output.values.hphase
    stocEnv = sound.analysis.output.values.stocEnv
    
    y = sound.synthesis.output.values.y
    yh = sound.synthesis.output.values.yh
    yst = sound.synthesis.output.values.yst
    
    if sound.analysis_progress:
        sound.analysis_progress.description='Plotting Results'
        sound.analysis_progress.bar_style='info'
        sound.analysis_progress.value = 4

    try: gui.plots_results.clear()
    except Exception: pass

    # create figure to plot
    gui.plots_results = plt.figure(num='Analysis result of ' + sound.name + sound.extension, figsize=(8.65, 9)) # 8.25
    # gui.plots_results.suptitle(sound.name + sound.extension, fontsize=16)

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

    # plot the input sound
    ax1 = gui.plots_results.add_subplot(311)
    ax1.plot(np.arange(x.size)/float(fs), x)
    ax1.axis([0, x.size/float(fs), min(x), max(x)])
    ax1.set_ylabel('amplitude')
    ax1.set_xlabel('time (sec)')
    ax1.set_title('input sound: x')

    # plot spectrogram stochastic component
    ax2 = gui.plots_results.add_subplot(312)
    numFrames = int(stocEnv[:,0].size)
    sizeEnv = int(stocEnv[0,:].size)
    frmTime = H*np.arange(numFrames)/float(fs)
    binFreq = (.5*fs)*np.arange(sizeEnv*maxplotfreq/(.5*fs))/sizeEnv
    ax2.pcolormesh(frmTime, binFreq, np.transpose(stocEnv[:,:int(sizeEnv*maxplotfreq/(.5*fs)+1)]))
    ax2.autoscale(tight=True)

    # plot harmonic on top of stochastic spectrogram
    if (hfreq.shape[1] > 0):
        harms = hfreq*np.less(hfreq,maxplotfreq)
        harms[harms==0] = np.nan
        numFrames = harms.shape[0]
        frmTime = H*np.arange(numFrames)/float(fs)
        ax2.plot(frmTime, harms, color='k', ms=3, alpha=1)
        ax2.set_xlabel('time (sec)')
        ax2.set_ylabel('frequency (Hz)')
        ax2.autoscale(tight=True)
        ax2.set_title('harmonics + stochastic spectrogram')
    
    # plot the output sound
    ax3 = gui.plots_results.add_subplot(313)
    ax3.plot(np.arange(y.size)/float(fs), y)
    ax3.axis([0, y.size/float(fs), min(y), max(y)])
    ax3.set_ylabel('amplitude')
    ax3.set_xlabel('time (sec)')
    ax3.set_title('output sound: y')
    
    gui.plots_results.tight_layout()
    gui.plots_results.show()
    
    if sound.analysis_progress:
        sound.analysis_progress.value = 100
        sound.analysis_progress.layout.visibility = 'hidden'

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
    hfreqIntp = np.fromstring(sound_morph.harmonic_frequencies.value[1:-1], dtype=np.float, sep=',')
    hmagIntp = np.fromstring(sound_morph.harmonic_magnitudes.value[1:-1], dtype=np.float, sep=',')
    stocIntp = np.fromstring(sound_morph.stochastic_component.value[1:-1], dtype=np.float, sep=',')

    # morph the two sounds
    yhfreq, yhmag, ystocEnv = HPST.hpsMorph(hfreq1, hmag1, stocEnv1, hfreq2, hmag2, stocEnv2, hfreqIntp, hmagIntp, stocIntp)

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

    gui.plots_results = plt.figure(num='Generated file analysis ' + sound_morph.name + sound_morph.extension, figsize=(8.65, 6)) # 8.25
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