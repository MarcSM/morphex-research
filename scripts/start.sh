#!/usr/bin/env bash

# Running the voila server
until cd /notebooks/notebooks/examples/voila-notebooks/
do
    echo "Waiting for the volumes to be mounted"
    sleep 4 # Wait 4 seconds
done

echo "Running the voila application"
voila --port=4444 bqplot.ipynb & # Voila application

echo "Voila application up and running"


echo "Starting the PulseAudio daemon"
pulseaudio --log-level=4 --log-target=stderr -v &

# Running the Jupyter Notebooks server
echo "Running Jupyter Notebooks"
cd /notebooks/
jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --no-browser