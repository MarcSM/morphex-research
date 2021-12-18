# Morphex Research
*A Spectral Morphing Synthesizer* 

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

### Abstract

The main goal of this project was to find a way to **perform spectral morphing** while exploring the latent timbral space that emerges from the spectral analysis of musical sounds, and to craft new hybrid instruments.
The project is split into two very well defined parts.

The first is **research**; here we have written a collection of **jupyter notebooks** that address the main problems that needed to be approached such as how to perform the harmonic plus magnitudes interpolations in real-time; how to manage the result of the sound analysis into a file to be able to load it afterwards on the plugin and allow the user to build your own collection of sounds and presets; how to normalize both sounds magnitudes before the synthesis and how to transpose all the harmonics of the sound properly to be able to play the sound across every note.

The second part of this project is the **development of a plugin** that implements all the features designed in the research part, plus designing a user interface with the proper compoentnts to allow the user to interact with the morphing engine and thus, with the generated sound.

**We have ended up designing and developing a plugin that accomplishes that mission**, keeping in mind that it's meant to be used professionally by producers, musicians and sound designers.

### Description

This repository contains a docker-compose file to run a Jupyter server. To run the notebooks, you need to first install docker and run the Jupyter server available in the docker image.

## Plugin Repository

https://github.com/MarcSM/morphex

## Install docker

### Windows
https://docs.docker.com/docker-for-windows/install/

### Mac
https://docs.docker.com/docker-for-mac/install/

### Ubuntu
https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/#install-docker-ce

## Running the Jupyter server 
Once Docker is up and running, in a terminal/console window, change to the project directory.

On MacOS or Windows, run:

    docker-compose up

On Linux, run the following (this command ensures that any files you create are owned by your own user):

    JUPYTER_USER_ID=$(id -u) docker-compose up

The first time you run this command it will download the required docker images (about 2GB in size). If you have previously downloaded the images and would like to update them with the last version, run:

    docker-compose pull

Then accesss http://localhost:4444 with your browser and when asked for a
password use the default password ***mir***

Then, you can access the notebooks from the browser and run them.

**NOTE**: To run the notebooks "3 - Live Audio & Widgets.ipynb" and "4 - Live Morphing.ipynb" it is needed for "PyAudio" to stream audio outside of the docker container. This has not been achieved yet so you have two options, write the result of the processing as a ".wav" file, or install all the packages on "requirements.txt" on your own computer and run the Jupyter server on your machine instead of inside the docker container; to do so, you need to open a terminal, go to the project's folder and run the command "jupyter notebook" to run the server. 

## License

All the software is distributed with the Affero GPL license (http://www.gnu.org/licenses/agpl-3.0.en.html). The sounds located at "data/sounds" come from freesound.org, in particular from http://www.freesound.org/people/xserra/packs/13038/.
