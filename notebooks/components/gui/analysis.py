# Enabling ipympl for interactive plots
get_ipython().run_line_magic('matplotlib', 'widget') # ipympl

import sys, os
sys.path.append('../../../')
import utils.hpsBridge as hps
from utils.structures import Sound
from dotmap import DotMap
from IPython.display import (Audio, display, clear_output)
from functools import partial
from ipywidgets import (
    Output, HTML, Text, Label, Dropdown, BoundedIntText, BoundedFloatText, Button, GridBox, Layout, Box,
    ButtonStyle, IntProgress
)

# Constants
DEFAULT_SOUND_FILE = '../data/sounds/violin-B3.wav'
ANALYSIS_OUTPUT_FOLDER = '../data/analysis_output'
            
def main ():

    # Initializing the audio
    #with Output(): display(Audio('../data/sounds/silence.wav', autoplay=True))
    # Audio('../data/sounds/silence.wav', autoplay=True)
    # clear_output()
    
    # Load the sound by default
    sound = Sound(DEFAULT_SOUND_FILE)
    
    # GUI elements that does not contain values about the sound
    gui = DotMap()
    
    # Generate the GUI components of the GUI
    generate_gui_components(gui, sound)
    
    # Display the GUI
    display_gui(gui, sound)

def on_play_input_file_button_clicked(sound, b):
    """When a button is clicked, we play the sound in a dedicated Output widget.

    Args:
        sound_file: string with the path of the sound file
    """

    with Output():
        display(Audio(sound.path, rate=16000, autoplay=True))

def on_play_button_clicked(sound_file, b):
    """When a button is clicked, we play the sound in a dedicated Output widget.

    Args:
        sound_file: string with the path of the sound file
    """
    
    with Output():
        display(Audio(sound_file, rate=16000, autoplay=True))

def on_generate_had_file_button_clicked(sound, b):
    """We generate the had when the button is clicked.

    Args:
        sound_file: string with the path of the sound file
    """
    
    # Generatin the file
    sound.generate_had_file()

    # Successful Analysis Message
    sound.generate_had_file_button.description = "File Generated Successfully"
    sound.generate_had_file_button.button_style = 'success'
  
def run_analysis(gui, sound):
    """Run the sound file analysis.

    Args:
        button: Button that triggers this function
    """
    try:
        # Hiding the analysis message
        sound.analysis_message.layout.visibility = 'hidden'
        
        # Hiding the generate .had file button
        sound.generate_had_file_button.layout.visibility = 'hidden'
        
        # Hiding the play buttons
        sound.synthesis.output.mixed.play_button.layout.visibility = 'hidden'
        sound.synthesis.output.sines.play_button.layout.visibility = 'hidden'
        sound.synthesis.output.stochastic.play_button.layout.visibility = 'hidden'
        
        # Showing the player controls
        gui.player_header.layout.visibility = 'hidden'
        
        # Hiding the results
        gui.results_display_header.layout.visibility = 'hidden'
        
        # Computing the analysis
        hps.analysis(sound, ANALYSIS_OUTPUT_FOLDER)
        
        # Successful Analysis Message
        sound.analysis_message.description = "Analysis Completed"
        sound.analysis_message.button_style = 'success'
        sound.analysis_message.layout.visibility = 'visible'
        
        # Showing the player controls
        gui.player_header.layout.visibility = 'visible'
        
        # Updating the "Both Mixed" button
        sound.synthesis.output.mixed.play_button.on_click(
            partial(on_play_button_clicked, sound.synthesis.output.mixed.path)
        )
        sound.synthesis.output.mixed.play_button.layout.visibility = 'visible'
        
        # Updating the "Sinusoidal Part" button
        sound.synthesis.output.sines.play_button.on_click(
            partial(on_play_button_clicked, sound.synthesis.output.sines.path)
        )
        sound.synthesis.output.sines.play_button.layout.visibility = 'visible'
        
        # Updating the "Stochastic Part" button
        sound.synthesis.output.stochastic.play_button.on_click(
            partial(on_play_button_clicked, sound.synthesis.output.stochastic.path)
        )
        sound.synthesis.output.stochastic.play_button.layout.visibility = 'visible'
        
        # Showing the generate .had file button
        sound.generate_had_file_button.description = 'Generate .had file'
        sound.generate_had_file_button.button_style = 'info'
        sound.generate_had_file_button.layout.visibility = 'visible'
        
        # Generating the plots
        hps.plot_analysis(gui, sound)

        # # Generating the plots
        # with gui.plots_output:
        #     clear_output(wait = True)
        #     hps.plot_analysis(gui, sound)

        # Showing the results
        gui.results_display_header.layout.visibility = 'visible'
        
    except ValueError as errorMessage:
        # Displaying the error
        sound.analysis_progress.layout.visibility = 'hidden'
        sound.analysis_message.description = str(errorMessage)
        sound.analysis_message.button_style = 'danger'
        sound.analysis_message.layout.visibility = 'visible'

        
def generate_gui_components(gui, sound):
    """Generate the GUI components.

    Args:
        gui: lambda that contains all GUI objects that don't have any relation with the audio
        sound: Sound that contains the sound properties and all GUI objects related with the sound 
    """
    
    # Header and title of the GUI
    gui.header  = HTML(
         value="<center style='color:#b1bed6;font-size:1.6em;overflow:hidden'>Sound File Analysis</center>",
         layout=Layout(width='auto', grid_area='header')
    )

    # Sound - Input File
    sound.input_file = Text(
        description='Input File',
        value=sound.path,
        layout=Layout(width='auto', grid_area='input_file')
    )
    
    # If the field changes
    sound.input_file.observe(sound.input_file_changed)
    
    # Sound - Play Input File
    sound.play_input_file_button = Button(
        description='Play',
        button_style='',
        layout=Layout(width='auto', grid_area='play_input_file_button'),
    )
    
    # Play the input file sound
    sound.play_input_file_button.on_click(
        partial(on_play_input_file_button_clicked, sound)
    )

    # Sound - Analysis Window Type
    sound.window_type = Dropdown(
        description='Window',
        value='blackman',
        options=['rectangular', 'hanning', 'hamming', 'blackman', 'blackmanharris'],
        layout=Layout(width='auto', grid_area='window_type'),
    )

    # Sound - Window Size
    sound.window_size = BoundedIntText(
        description='Window Size',
        value=1001, min=1, max=10000, step=1,
        layout=Layout(width='auto', grid_area='window_size')
    )

    # Sound - FFT Size
    sound.fft_size = BoundedIntText(
        description='FFT Size',
        value=1024, min=2, max=16384, step=1,
        layout=Layout(width='auto', grid_area='fft_size')
    )

    # Sound - Magnitude Threshold
    sound.magnitude_threshold = BoundedIntText(
        description='Magn. Thres.',
        value=-100, min=-200, max=0, step=1,
        layout=Layout(width='auto', grid_area='magnitude_threshold')
    )

    # Sound - Minimum Sinusoidal Tracks Duration
    sound.min_sine_dur = BoundedFloatText(
        description='Min. Sine Dur.',
        value=0.05, min=0.01, max=5.00, step=1,
        layout=Layout(width='auto', grid_area='min_sine_dur')
    )

    # Sound - Minimum Fundamental Frequency
    sound.min_f0 = BoundedIntText(
        description='Min. f0',
        value=200, min=0, max=20000, step=1,
        layout=Layout(width='auto', grid_area='min_f0')
    )

    # Sound - Maximum Fundamental Frequency
    sound.max_f0 = BoundedIntText(
        description='Max. f0',
        value=300, min=0, max=20000, step=1,
        layout=Layout(width='auto', grid_area='max_f0')
    )

    # Sound - Maximum Fundamental Frequency Error Accepted
    sound.max_f0_error = BoundedIntText(
        description='Max. f0 Err.',
        value=10, min=0, max=100, step=1,
        layout=Layout(width='auto', grid_area='max_f0_error')
    )

    # Sound - Allowed Deviation of Harmonic Tracks
    sound.harm_dev_slope = BoundedFloatText(
        description='Harm. Dev. Slope',
        value=0.01, min=0.01, max=10.0, step=1,
        layout=Layout(width='auto', grid_area='harm_dev_slope')
    )

    # Sound - Max Number of Harmonics
    sound.max_harm = BoundedIntText(
        description='Max. Harm.',
        value=60, min=1, max=200, step=1,
        layout=Layout(width='auto', grid_area='max_harm')
    )

    # Sound - Stochastic Decimation Factor
    sound.stoc_fact = BoundedFloatText(
        description='Stoc. Fact.',
        value=0.1, min=0.1, max=10.0, step=1,
        layout=Layout(width='auto', grid_area='stoc_fact')
    )

    # Sound - Analysis Button
    sound.analysis_button = Button(
        description='Anaysis',
        button_style='info',
        layout=Layout(width='auto', grid_area='analysis_button'),
    )

    # Function wrap to pass the gui and the sound parameters
    def run_analysis_with_params(button):
        run_analysis(gui, sound)
    
    # Analysis Button calling the run analysis function on click
    sound.analysis_button.on_click(run_analysis_with_params)

    # Analysis Progress Bar
    sound.analysis_progress = IntProgress(
        value=0, min=0, max=100, step=1,
        description='Analyzing', bar_style='', orientation='horizontal',
        # 'success', 'info', 'warning', 'danger' or ''
        layout=Layout(width='auto', visibility = 'hidden', grid_area='analysis_progress')
    )

    # Analysis Error
    sound.analysis_message = Button(
        description="",
        button_style='danger', disabled=False,
        layout=Layout(width='auto', visibility = 'hidden', grid_area='analysis_message')
    )

    # Player Header
    gui.player_header  = HTML(
         value="<center style='color:#b1bed6;font-size:1.5em;margin-top:1em;overflow:hidden'>Play the Result</center>",
         layout=Layout(width='auto', visibility = 'hidden', grid_area='player_header')
    )

    # Creating and adding the "Both Mixed" button to the layout
    sound.synthesis.output.mixed.play_button = Button(
        description="Both Mixed",
        layout=Layout(width='auto', visibility = 'hidden', grid_area='analysis_output_mixed'),
    )

    # Creating and adding the "Sinusoidal Part" button to the layout
    sound.synthesis.output.sines.play_button = Button(
        description="Sinusoidal Part",
        layout=Layout(width='auto', visibility = 'hidden', grid_area='analysis_output_sines'),
    )

    # Creating and adding the "Stochastic Part" button to the layout
    sound.synthesis.output.stochastic.play_button = Button(
        description="Stochastic Part",
        layout=Layout(width='auto', visibility = 'hidden', grid_area='analysis_output_stochastic'),
    )

    # Sound - Generate .had File Button
    sound.generate_had_file_button = Button(
        description='Generate .had file',
        button_style='info',
        layout=Layout(width='auto', visibility = 'hidden', grid_area='generate_had_file_button'),
    )
    
    # Generate .had File Button calling the sound.generate_had_file function on click
    sound.generate_had_file_button.on_click(
        partial(on_generate_had_file_button_clicked, sound)
    )

    # - - - - RESULTS DISPLAY - - - - #

    # Results Display Header
    gui.results_display_header = HTML(
        value="<center style='color:#b1bed6;font-size:1.5em;margin-top:1em;overflow:hidden'>Results Display</center>",
        layout=Layout(width='auto', visibility = 'hidden', grid_area='results_display_header')
    )

    # Output element to display the plots on the GUI
    gui.plots_output = Output(
        layout=Layout(width = 'auto', grid_area='plots_output'),   
    )

    
def display_gui(gui, sound):
    """Mount and display the analysis GUI.

    Args:
        gui: lambda that contains all GUI objects that don't have any relation with the audio
        sound: Sound that contains the sound properties and all GUI objects related with the sound 
    """

    # Mounting the GUI
    grid = GridBox(
        children=[
            gui.header, sound.input_file, sound.play_input_file_button, sound.window_type, 
            sound.window_size, sound.fft_size, sound.magnitude_threshold, sound.min_sine_dur, 
            sound.min_f0, sound.max_f0, sound.max_f0_error, sound.harm_dev_slope, sound.max_harm, 
            sound.stoc_fact, sound.analysis_button, sound.analysis_progress, 
            sound.analysis_message, gui.player_header, sound.synthesis.output.mixed.play_button, 
            sound.synthesis.output.sines.play_button, 
            sound.synthesis.output.stochastic.play_button, sound.generate_had_file_button,
            gui.results_display_header, gui.plots_output
        ],
        layout=Layout(
            width='100%',
            grid_template_rows='auto auto auto auto',
            grid_template_columns='25% 25% 25% 25%',
            grid_template_areas='''
            "header header header header"
            "input_file input_file input_file play_input_file_button"
            "window_type window_size fft_size magnitude_threshold"
            "min_sine_dur min_f0 max_f0 max_f0_error"
            "harm_dev_slope max_harm stoc_fact analysis_button"
            "analysis_progress analysis_progress analysis_progress analysis_progress"
            "analysis_message analysis_message analysis_message analysis_message"
            "player_header player_header player_header player_header"
            "analysis_output_sines analysis_output_mixed analysis_output_mixed analysis_output_stochastic"
            ". generate_had_file_button generate_had_file_button ."
            "results_display_header results_display_header results_display_header results_display_header"
            "plots_output plots_output plots_output plots_output"
            '''
        )
    )
    
    display(grid)


if __name__ == "__main__":
    main()

main()
