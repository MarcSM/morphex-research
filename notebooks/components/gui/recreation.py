# Enabling ipympl for interactive plots
get_ipython().run_line_magic('matplotlib', 'widget') # ipympl

import sys, os, time, asyncio
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
DEFAULT_SOUND_FILE_1 = '../data/sounds/violin-B3.wav'
DEFAULT_SOUND_FILE_2 = '../data/sounds/soprano-E4.wav'
ANALYSIS_OUTPUT_FOLDER = '../data/analysis_output'
MORPHINGS_OUTPUT_FOLDER = '../data/morphing_output'
            
def main ():

    # Initializing the audio
    # NOTE: autoplay does not work in the beginning
    #display(Audio('../data/sounds/silence.wav', rate=16000, autoplay=True))
    # display(Audio('../data/sounds/silence.wav', autoplay=True))
    #clear_output()
    
    # Load the sounds by default
    sound_1 = Sound(DEFAULT_SOUND_FILE_1)
    sound_2 = Sound(DEFAULT_SOUND_FILE_2)

    # Empty sound where the morph will be generated 
    sound_morph = Sound()
    
    # GUI elements that does not contain values about the sound
    gui = DotMap()
    
    # Generate the GUI components of the GUI
    generate_gui_components(gui, sound_1, sound_2, sound_morph)
    
    # Display the GUI
    display_gui(gui, sound_1, sound_2, sound_morph)

def on_play_input_file_button_clicked(gui, sound, b):
    """When a button is clicked, we play the sound in a dedicated Output widget.

    Args:
        sound_file: string with the path of the sound file
    """
    
    # with gui.sound_output:
    with Output():
        display(Audio(sound.path, rate=16000, autoplay=True))

def on_play_button_clicked(gui, sound_file, b):
    """When a button is clicked, we play the sound in a dedicated Output widget.

    Args:
        sound_file: string with the path of the sound file
    """
    
    with Output():
        display(Audio(sound_file, rate=16000, autoplay=True))

# async def on_load_sound_button_clicked(sound, b):
def on_load_sound_button_clicked(sound, b):
    """We generate the had when the button is clicked.

    Args:
        sound_file: string with the path of the sound file
    """
    try:
        sound.load_sound_button.description = "Loading sound..."
        sound.load_sound_button.button_style = 'warning'
        sound.load_sound_button.disabled = True

        # Loading the file
        sound.load_had_file()

        sound.load_sound_button.description = "Sound loaded successfully"
        sound.load_sound_button.button_style = 'success'
        sound.load_sound_button.disabled = True

    except Exception as errorMessage:

        # Displaying the error
        sound.load_sound_button.description = str(errorMessage)
        sound.load_sound_button.button_style = 'danger'
        sound.load_sound_button.disabled = True
  
def generate_morph(gui, sound_1, sound_2, sound_morph):
    """Run the sound file analysis.

    Args:
        button: Button that triggers this function
    """
    try:
        # Hiding the player controls
        gui.player_header.layout.visibility = 'hidden'
        sound_morph.synthesis.output.play_button.layout.visibility = 'hidden'

        # Hiding the results
        gui.results_display_header.layout.visibility = 'hidden'

        # Genereting the morph
        hps.transformation_synthesis(sound_1, sound_2, sound_morph, MORPHINGS_OUTPUT_FOLDER)

        # Updating the play morph sound button
        sound_morph.synthesis.output.play_button.on_click(
            partial(on_play_button_clicked, gui, sound_morph.synthesis.output.path)
        )

        # Showing the player controls
        gui.player_header.layout.visibility = 'visible'
        sound_morph.synthesis.output.play_button.layout.visibility = 'visible'

        # Generating the plots
        hps.plot_transformation_synthesis(gui, sound_morph)
        
        # # Generating the plots
        # with gui.plots_output:
        #     clear_output(wait = True)
        #     hps.plot_transformation_synthesis(gui, sound_morph)

        # Showing the results
        gui.results_display_header.layout.visibility = 'visible'
        
    except Exception as errorMessage:

        # Displaying the error
        gui.morph_message.layout.visibility = 'hidden'
        gui.morph_message.description = str(errorMessage)
        gui.morph_message.button_style = 'danger'
        gui.morph_message.layout.visibility = 'visible'

        time.sleep(8)

        gui.morph_message.layout.visibility = 'hidden'

        
def generate_gui_components(gui, sound_1, sound_2, sound_morph):
    """Generate the GUI components.

    Args:
        gui: lambda that contains all GUI objects that don't have any relation with the audio
        sound: Sound that contains the sound properties and all GUI objects related with the sound 
    """
    
    # Header and title of the GUI
    gui.header = HTML(
         value="<center style='color:#b1bed6;font-size:1.6em;overflow:hidden'>Sound Moprhing</center>",
         layout=Layout(width='auto', grid_area='header')
    )

    # - - - - SOUND 1 - - - - #

    # Sound 1 - Header
    sound_1.header = HTML(
        value="<center style='color:#b1bed6;font-size:1.2em;overflow:hidden'>Sound 1</center>",
        layout=Layout(width='auto', grid_area='sound_1_header')
    )

    # Sound 1 - Input File
    sound_1.input_file = Text(
        description='Input File',
        value=sound_1.path,
        layout=Layout(width='auto', grid_area='sound_1_input_file')
    )

    # If the field changes
    sound_1.input_file.observe(sound_1.input_file_changed)
    
    # Sound 1 - Play Input File
    sound_1.play_input_file_button = Button(
        description='Play',
        button_style='',
        layout=Layout(width='auto', grid_area='sound_1_play_input_file_button'),
    )

    # Sound 1 - Play the input file sound
    sound_1.play_input_file_button.on_click(
        partial(on_play_input_file_button_clicked, gui, sound_1)
    )

    # Sound 1 - Load Sound Button
    sound_1.load_sound_button = Button(
        description='Load sound',
        button_style='info',
        layout=Layout(width='auto', grid_area='sound_1_load_sound_button'),
    )
    
    # Sound 1 - Load sound button calling the sound_1.load_sound_file function on click
    sound_1.load_sound_button.on_click(
        partial(on_load_sound_button_clicked, sound_1)
    )

    # - - - - SOUND 2 - - - - #

    # Sound 2 - Header
    sound_2.header = HTML(
        value="<center style='color:#b1bed6;font-size:1.2em;overflow:hidden'>Sound 2</center>",
        layout=Layout(width='auto', grid_area='sound_2_header')
    )

    # Sound 2 - Input File
    sound_2.input_file = Text(
        description='Input File',
        value=sound_2.path,
        layout=Layout(width='auto', grid_area='sound_2_input_file')
    )
    
    # If the field changes
    sound_2.input_file.observe(sound_2.input_file_changed)
    
    # Sound 2 - Play Input File
    sound_2.play_input_file_button = Button(
        description='Play',
        button_style='',
        layout=Layout(width='auto', grid_area='sound_2_play_input_file_button'),
    )

    # Sound 2 - Play the input file sound
    sound_2.play_input_file_button.on_click(
        partial(on_play_input_file_button_clicked, gui, sound_2)
    )

    # Sound 2 - Load Sound Button
    sound_2.load_sound_button = Button(
        description='Load Sound',
        button_style='info',
        layout=Layout(width='auto', grid_area='sound_2_load_sound_button'),
    )
    
    # Sound 2 - Load sound button calling the sound_2.load_sound_file function on click
    sound_2.load_sound_button.on_click(
        partial(on_load_sound_button_clicked, sound_2)
    )

    # - - - - MORPHING - - - - #

    # Morph Controls - Header
    gui.morph_controls_header = HTML(
         value="<center style='color:#b1bed6;font-size:1.5em;margin-top:1em;overflow:hidden'>Morph Controls</center>",
         layout=Layout(width='auto', grid_area='morph_controls_header')
    )

    # Morph Controls - Sub-Header
    gui.morph_controls_sub_header = HTML(
         value="<center style='color:#b1bed6;font-size:1.2em;margin-top:1em;overflow:hidden'>Interpolation Factors - 0 to 1 (time, value pairs)</center>",
         layout=Layout(width='auto', grid_area='morph_controls_sub_header')
    )

    # Morph Controls - Harmonic Frequencies
    sound_morph.harmonic_frequencies = Text(
        value='[0, 0, .1, 0, .9, 1, 1, 1]',
        layout=Layout(width='auto', grid_area='morph_harmonic_frequencies')
    )
    gui.morph_harmonic_frequencies_label = Label(
        value='Harmonic Frequencies',
        layout=Layout(width='auto', grid_area='morph_harmonic_frequencies_label')
    )

    # Morph Controls - Harmonic Magnitudes
    sound_morph.harmonic_magnitudes = Text(
        value='[0, 0, .1, 0, .9, 1, 1, 1]',
        layout=Layout(width='auto', grid_area='morph_harmonic_magnitudes')
    )
    gui.morph_harmonic_magnitudes_label = Label(
        value='Harmonic Magnitudes',
        layout=Layout(width='auto', grid_area='morph_harmonic_magnitudes_label')
    )

    # Morph Controls - Stochastic Component
    sound_morph.stochastic_component = Text(
        value='[0, 0, .1, 0, .9, 1, 1, 1]',
        layout=Layout(width='auto', grid_area='morph_stochastic_component')
    )
    gui.morph_stochastic_component_label = Label(
        value='Stochastic Component',
        layout=Layout(width='auto', grid_area='morph_stochastic_component_label')
    )

    # Morph Controls - Generate Morph Button
    gui.generate_morph_button = Button(
        description='Generate Morph',
        button_style='info',
        layout=Layout(width='auto', grid_area='generate_morph_button'),
    )

    # Function wrap to pass the gui and the sound parameters
    def generate_morph_with_params(button):
        generate_morph(gui, sound_1, sound_2, sound_morph)
    
    # Generate Morph Button calling the run morphing function on click
    gui.generate_morph_button.on_click(generate_morph_with_params)

    # Morph Message
    gui.morph_message = Button(
        description="",
        button_style='danger',
        layout=Layout(width='auto', visibility='hidden', grid_area='morph_message')
    )

    # - - - - RESULTS - - - - #

    # Player Header
    gui.player_header = HTML(
         value="<center style='color:#b1bed6;font-size:1.5em;margin-top:1em;overflow:hidden'>Play the Result</center>",
         layout=Layout(width='auto', visibility = 'hidden', grid_area='player_header')
    )

    # Creating and adding the sound morph play button to the layout
    sound_morph.synthesis.output.play_button = Button(
        description="Play",
        layout=Layout(width='auto', visibility = 'hidden', grid_area='sound_morph_play_button'),
    )

    gui.sound_output = Output(
        layout=Layout(height='0', width = '0', grid_area='sound_output')
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

    
def display_gui(gui, sound_1, sound_2, sound_morph):
    """Mount and display the analysis GUI.

    Args:
        gui: lambda that contains all GUI objects that don't have any relation with the audio
        sound: Sound that contains the sound properties and all GUI objects related with the sound 
    """

    # Sound 1 - Panel
    sound_1_panel = GridBox(
        children=[
            sound_1.header, sound_1.input_file, sound_1.play_input_file_button,
            sound_1.load_sound_button
        ],
        layout=Layout(
            width='auto',
            grid_area='sound_1_panel',
            grid_template_rows='auto auto auto auto',
            grid_template_columns='25% 25% 25% 25%',
            grid_template_areas='''
            "header header header header"
            "sound_1_header sound_1_header sound_1_header sound_1_header"
            "sound_1_input_file sound_1_input_file sound_1_input_file sound_1_play_input_file_button"
            "sound_1_load_sound_button sound_1_load_sound_button sound_1_load_sound_button sound_1_load_sound_button"
            '''
        )
    )

    # Sound 2 - Panel
    sound_2_panel = GridBox(
        children=[
            sound_2.header, sound_2.input_file, sound_2.play_input_file_button,
            sound_2.load_sound_button
        ],
        layout=Layout(
            width='auto',
            grid_area='sound_2_panel',
            grid_template_rows='auto auto auto auto',
            grid_template_columns='25% 25% 25% 25%',
            grid_template_areas='''
            "header header header header"
            "sound_2_header sound_2_header sound_2_header sound_2_header"
            "sound_2_input_file sound_2_input_file sound_2_input_file sound_2_play_input_file_button"
            "sound_2_load_sound_button sound_2_load_sound_button sound_2_load_sound_button sound_2_load_sound_button"
            '''
        )
    )

    # Morph Controls - Panel
    morph_controls_panel = GridBox(
        children=[
            gui.morph_controls_header, gui.morph_controls_sub_header,
            gui.morph_harmonic_frequencies_label, sound_morph.harmonic_frequencies,
            gui.morph_harmonic_magnitudes_label, sound_morph.harmonic_magnitudes,
            gui.morph_stochastic_component_label, sound_morph.stochastic_component,
            gui.generate_morph_button, gui.morph_message
        ],
        layout=Layout(
            width='auto',
            grid_area='morph_controls_panel',
            grid_template_rows='auto auto auto auto',
            grid_template_columns='25% 25% 25% 25%',
            grid_template_areas='''
            "morph_controls_header morph_controls_header morph_controls_header morph_controls_header"
            "morph_controls_sub_header morph_controls_sub_header morph_controls_sub_header morph_controls_sub_header"
            "morph_harmonic_frequencies_label morph_harmonic_frequencies morph_harmonic_frequencies ."
            "morph_harmonic_magnitudes_label morph_harmonic_magnitudes morph_harmonic_magnitudes ."
            "morph_stochastic_component_label morph_stochastic_component morph_stochastic_component ."
            ". generate_morph_button generate_morph_button ."
            ". morph_message morph_message ."
            '''
        )
    )

    # Results Player - Panel
    results_player_panel = GridBox(
        children=[
            gui.player_header, sound_morph.synthesis.output.play_button, gui.sound_output
        ],
        layout=Layout(
            width='auto',
            grid_area='results_player_panel',
            grid_template_rows='auto auto auto auto',
            grid_template_columns='25% 25% 25% 25%',
            grid_template_areas='''
            "player_header player_header player_header player_header"
            ". sound_morph_play_button sound_morph_play_button ."
            ". sound_output . ."
            '''
        )
    )

    # Results Display - Panel
    results_display_panel = GridBox(
        children=[
            gui.results_display_header, gui.plots_output
        ],
        layout=Layout(
            width='auto',
            grid_area='results_display_panel',
            grid_template_rows='auto auto auto auto',
            grid_template_columns='25% 25% 25% 25%',
            grid_template_areas='''
            "results_display_header results_display_header results_display_header results_display_header"
            "plots_output plots_output plots_output plots_output"
            '''
        )
    )

    # Mounting the GUI
    grid = GridBox(
        children=[
            gui.header, sound_1_panel, sound_2_panel, morph_controls_panel, results_player_panel,
            results_display_panel
        ],
        layout=Layout(
            width='100%',
            grid_template_rows='auto auto auto auto',
            grid_template_columns='25% 25% 25% 25%',
            grid_template_areas='''
            "header header header header"
            "sound_1_panel sound_1_panel sound_2_panel sound_2_panel"
            "morph_controls_panel morph_controls_panel morph_controls_panel morph_controls_panel"
            "results_player_panel results_player_panel results_player_panel results_player_panel"
            "results_display_panel results_display_panel results_display_panel results_display_panel"
            '''
        )
    )
    
    display(grid)


if __name__ == "__main__":
    main()

main()
