import sys, os, ast, xmltodict
import numpy as np

from dotmap import DotMap

# Sound class definition
class Sound:
    def __init__(self, filepath=''):
        self.loaded = False
        self.analyzed = False
        self.had_file_loaded = False
        
        # Generating needed structure for the analysis output data
        self.analysis = DotMap()
        self.analysis.output = DotMap()
        self.analysis.output.values = DotMap()
        
        # Generating needed structure for the synthesis output data
        self.synthesis = DotMap()
        self.synthesis.output = DotMap()
        self.synthesis.output.values = DotMap()
        self.synthesis.output.sines = DotMap()
        self.synthesis.output.stochastic = DotMap()
        self.synthesis.output.mixed = DotMap()
        
        # Initializing default values
        self.fs = 44100
        
        # Initializing the harmonic analysis data structure for the .had file
        self.had = {}
        
        self.load(filepath)
        #self.name = name
        #self.path = path
        
    def load(self, filepath):
        self.path = filepath
        self.name, self.extension = os.path.splitext(os.path.basename(self.path))
        self.dirpath = os.path.dirname(self.path)
        self.loaded = True
        self.analyzed = False
        
    def analyze(self):
        raise Exception("Method not implemented")
        if not self.loaded: raise Exception("The file couldn't be analyzed becaus it wasn't loaded")
        self.analyzed = True
    
    def update_had_values(self):
        """Updating the harmonic analysis data structure for the .had file"""
        self.had = {
            "sound": {
                "file": {
                    "name": self.name,
                    "extension": self.extension,
                    "path": self.path,
                    "dirpath": self.dirpath
                },
                #"x": self.x,
                "fs": self.fs
            },
            "parameters": {
                "window": self.window,
                "window_type": self.window_type.value,
                "window_size": self.window_size.value,
                "fft_size": self.fft_size.value,
                "magnitude_threshold": self.magnitude_threshold.value,
                "min_sine_dur": self.min_sine_dur.value,
                "max_harm": self.max_harm.value,
                "min_f0": self.min_f0.value,
                "max_f0": self.max_f0.value,
                "max_f0_error": self.max_f0_error.value,
                "harm_dev_slope": self.harm_dev_slope.value,
                "stoc_fact": self.stoc_fact.value,
                "synthesis_fft_size": self.synthesis_fft_size,
                "hop_size": self.hop_size
            },
            "output": {
                "values": {
                    "harmonic_frequencies": self.analysis.output.values.hfreq.tolist(),
                    "harmonic_magnitudes": self.analysis.output.values.hmag.tolist(),
                    "harmonic_phases": self.analysis.output.values.hphase.tolist(),
                    "stochastic_residual": self.analysis.output.values.stocEnv.tolist()
                }
            }
        }
        
    def generate_had_file(self):
        xml = xmltodict.unparse({"harmonic_analysis_data": self.had })
        had_file = open(self.dirpath + "/" + self.name + ".had", "w")
        had_file.write(xml)
    
    def xml_postprocessor(self, path, key, value):
        try:
            return key, float(value)
        except (ValueError, TypeError):      
            try:
                return key, np.array(ast.literal_eval(value))
            except Exception:
                return key, value
        
    def load_had_file(self):
        had_file_path = self.dirpath + "/" + self.name + ".had"
        xml = open(had_file_path).read();
        had = xmltodict.parse(xml, postprocessor=self.xml_postprocessor)['harmonic_analysis_data']
        
        # Sound
        self.fs = had["sound"]["fs"]

        # File
        self.name = had["sound"]["file"]["name"]
        self.extension = had["sound"]["file"]["extension"]
        self.path = had["sound"]["file"]["path"]
        self.dirpath = had["sound"]["file"]["dirpath"]

        # Parameters
        self.window = had["parameters"]["window"]
        self.window_type = had["parameters"]["window_type"]
        self.window_size = had["parameters"]["window_size"]
        self.fft_size = had["parameters"]["fft_size"]
        self.magnitude_threshold = had["parameters"]["magnitude_threshold"]
        self.min_sine_dur = had["parameters"]["min_sine_dur"]
        self.max_harm = had["parameters"]["max_harm"]
        self.min_f0 = had["parameters"]["min_f0"]
        self.max_f0 = had["parameters"]["max_f0"]
        self.max_f0_error = had["parameters"]["max_f0_error"]
        self.harm_dev_slope = had["parameters"]["harm_dev_slope"]
        self.stoc_fact = had["parameters"]["stoc_fact"]
        self.synthesis_fft_size = had["parameters"]["synthesis_fft_size"]
        self.hop_size = had["parameters"]["hop_size"]

        # Output Values
        #testa = np.fromstring(test[0][1:-1], dtype=np.float, sep='\n')
        self.analysis.output.values.hfreq = np.array(had["output"]["values"]["harmonic_frequencies"])
        self.analysis.output.values.hmag = np.array(had["output"]["values"]["harmonic_magnitudes"])
        self.analysis.output.values.hphase = np.array(had["output"]["values"]["harmonic_phases"])
        self.analysis.output.values.stocEnv = np.array(had["output"]["values"]["stochastic_residual"])
        
        # Updating flags
        self.had_file_loaded = True
        
    def input_file_changed(self, change):
        if change['type'] == 'change' and change['name'] == 'value':
            self.load(change['new'])
            self.had_file_loaded = False
            if hasattr(self, 'load_sound_button'):
                self.load_sound_button.description = "Load sound"
                self.load_sound_button.button_style = 'info'
                self.load_sound_button.disabled = False
