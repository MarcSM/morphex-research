#!/usr/bin/env bash

# echo "Starting the PulseAudio daemon"
# pulseaudio --log-level=4 --log-target=stderr -v &

# Running the Jupyter Notebooks server
echo "Running Jupyter Notebooks"
cd /notebooks/
jupyter notebook --ip=0.0.0.0 --port=4444 --allow-root --no-browser