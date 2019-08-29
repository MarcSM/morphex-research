#!/usr/bin/env bash


# docker run -it -e PULSE_SERVER=docker.for.mac.localhost -v ~/.config/pulse:/home/pulseaudio/.config/pulse 5fd623bdee93
# docker run -it -e PULSE_SERVER=docker.for.mac.localhost -v ~/.config/pulse:/home/pulseaudio/.config/pulse --entrypoint speaker-test --rm jess/pulseaudio -c 2 -l 1 -t wav

# docker run -it -e PULSE_SERVER=docker.for.mac.localhost \
# -v ~/.config/pulse:/home/pulseaudio/.config/pulse \
# /Users/Marc/Research/Datasets:/notebooks/datasets \
# .:/notebooks \
# -p "8888:8888" \
# --rm 5fd623bdee93

# If you are on macos: 

# Install PulseAudio on the Mac:
# - brew install pulseaudio

# Run the daemon
# - pulseaudio --load=module-native-protocol-tcp --load=module-esound-protocol-tcp --exit-idle-time=-1 --daemon
# - pulseaudio --load=module-native-protocol-tcp --exit-idle-time=-1 --daemon

# Test the audio
# - docker run -it -e PULSE_SERVER=docker.for.mac.localhost -v ~/.config/pulse:/home/pulseaudio/.config/pulse --entrypoint speaker-test --rm research-workspace_mir-tool-extension -c 2 -l 1 -t wav
# - docker run -it -e PULSE_SERVER=docker.for.mac.localhost --entrypoint speaker-test --rm research-workspace_mir-tool-extension -c 2 -l 1 -t wav

# Handy
# docker exec -it silly_lamarr /bin/bash
# speaker-test -c 2 -l 1 -t wav

# docker run -it -e PULSE_SERVER=docker.for.mac.localhost -v ~/.config/pulse:/home/pulseaudio/.config/pulse --entrypoint speaker-test --rm research-workspace_mir-tool-extension -c 2 -l 1 -t wav
# docker run -it -e PULSE_SERVER=docker.for.mac.localhost --entrypoint speaker-test --rm research-workspace_mir-tool-extension -c 2 -l 1 -t wav
# docker exec -it research-workspace_mir-tool-extension_1 /bin/bash
# docker exec -i -t research-workspace_mir-tool-extension_1 /bin/bash

# docker run --device /dev/snd -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /run/dbus/:/run/dbus/:rw -v /dev/shm:/dev/shm --rm jess/pulseaudio -c 2 -l 1 -t wav
# docker run -it -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /dev/shm:/dev/shm --rm jess/pulseaudio -c 2 -l 1 -t wav
# docker run -it -e PULSE_SERVER=docker.for.mac.localhost --entrypoint speaker-test --rm jess/pulseaudio -c 2 -l 1 -t wav
# docker run -it -e PULSE_SERVER=docker.for.mac.localhost --rm jess/pulseaudio
# docker run -it -e PULSE_SERVER=docker.for.mac.localhost -v ~/.config/pulse:/home/pulseaudio/.config/pulse --rm jess/pulseaudio
# docker run -it -e PULSE_SERVER=docker.for.mac.localhost --entrypoint speaker-test --rm jess/pulseaudio -c 2 -l 1 -t wav
# docker run -it -e PULSE_SERVER=docker.for.mac.localhost -v ~/.config/pulse:/home/pulseaudio/.config/pulse --entrypoint speaker-test --rm jess/pulseaudio -c 2 -l 1 -t wav

# If you can't hear anything run the following comands
# - pacmd list-sinks # showing all audio devices
# - pacmd set-default-sink Channel_1__Channel_2.5 # set the default

# Run the daemon again
# - killall pulseaudio
# - pulseaudio --load=module-native-protocol-tcp --exit-idle-time=-1 --daemon

# Check that it's actually running
# pulseaudio --check -v

# Test the audio again
# - docker run -it -e PULSE_SERVER=docker.for.mac.localhost -v ~/.config/pulse:/home/pulseaudio/.config/pulse --entrypoint speaker-test --rm jess/pulseaudio -c 2 -l 1 -t wav

# docker run -e PULSE_SERVER=docker.for.mac.localhost -v ~/.config/pulse:/home/pulseaudio/.config/pulse jess/pulseaudio



#TODO Check to run comands on guest's machine to configure PulseAudio automatically


# Other tests
# aplay -l # list soundcards

FROM mtgupf/mir-toolbox

# Copy external libraries to the image
COPY externals/sms-tools-master /sms-tools
COPY externals/portaudio /portaudio
COPY externals/packages /packages

# Upgrades
RUN pip3 install --upgrade pip
#RUN pip3 install --upgrade numpy

# Installing PyAudio, PortAudio and PulseAudio # (no londer needed)
# RUN apt-get update
# RUN apt-get install python-pyaudio -y
# # RUN pip install --upgrade setuptools
# RUN apt-get install portaudio19-dev -y
# RUN apt-get install pulseaudio -y

# Adding a repository that has PulseAudio 12.2
# RUN add-apt-repository ppa:eh5/pulseaudio-a2dp
# RUN add-apt-repository 'deb http://deb.debian.org/debian sid main'
# RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 7638D0442B90D010
# RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 04EE7237B7D453EC
# RUN add-apt-repository ppa:mikhailnov/pulseeffects

# Installing PortAudio dependencies (no londer needed)

RUN apt-get update && apt-get install -y \
	m4 \
	intltool \
	libtool \
	libsndfile-dev \
	libcap-dev

# RUN cd /packages && tar xzf pulseaudio-12.2.tar.xz
RUN cd /packages/pulseaudio-12.2 && ./configure --prefix=/usr        \
									            --sysconfdir=/etc    \
									            --localstatedir=/var \
									            --disable-bluez4     \
									            --disable-bluez5     \
									            --disable-rpath
RUN cd /packages/pulseaudio-12.2 && make && make install

# RUN cd /packages && tar xzf pulseaudio-12.2.tar.xz && cd pulseaudio-12.2 && \
# 	./configure --prefix=/usr    \
#             --sysconfdir=/etc    \
#             --localstatedir=/var \
#             --disable-bluez4     \
#             --disable-bluez5     \
#             --disable-rpath      && \
# 	make && make install

RUN rm -fv /etc/dbus-1/system.d/pulseaudio-system.conf

# Installing needed librearies for live audio
RUN apt-get update && apt-get install -y \
	alsa-utils \
	libasound2 \
	libasound2-plugins \
	python-pyaudio \
	portaudio19-dev \
	pavucontrol \
	--no-install-recommends \
	&& rm -rf /var/lib/apt/lists/*

# pulseaudio-utils \

# Requirements
ADD requirements.txt /tmp/requirements/requirements.txt
RUN pip3 install -r /tmp/requirements/requirements.txt

# Compiling sms-tools
RUN cd /sms-tools/software/models/utilFunctions_C && python3 compileModule.py build_ext --inplace

ENV USER mir
ENV HOME /home/mir
RUN groupadd pulse
RUN groupadd pulse-access
RUN usermod -aG audio,pulse,pulse-access mir \
    && chown -R mir:mir $HOME
USER mir

COPY --chown=mir:mir config/jupyter_notebook_config.json /home/mir/.jupyter/
RUN mkdir -p /home/mir/.config/pulse

# ENV USER dsp_user
# ENV HOME /home/dsp_user
# RUN useradd --create-home --home-dir $HOME dsp_user \
#     && usermod -aG audio,pulse,pulse-access dsp_user \
#     && chown -R dsp_user:dsp_user $HOME
# USER dsp_user

# chown -R dsp_user:dsp_user $HOME/
# chown -R mir:mir /home/mir
# sudo chown -R $USER:$USER $HOME/

COPY externals/pulseaudio/default.pa /etc/pulse/default.pa
COPY externals/pulseaudio/client.conf /etc/pulse/client.conf
COPY externals/pulseaudio/daemon.conf /etc/pulse/daemon.conf

# ENV PULSE_SERVER = docker.for.mac.localhost # macos only
# RUN adduser mir pulse-access

# # Copy files to the image for testing purposes
COPY externals/testing /testing



# ENV HOME /home/dsp
# RUN useradd --create-home --home-dir $HOME dsp \
# 	&& usermod -aG audio,pulse,pulse-access dsp \
# 	&& chown -R dsp:dsp $HOME

# USER dsp

### END

# ENV USER_NAME dsp

# ENV HOME /home/$USER_NAME
# RUN useradd --create-home --home-dir $HOME $USER_NAME \
# 	&& usermod -aG audio,pulse,pulse-access $USER_NAME \
# 	&& chown -R $USER_NAME:$USER_NAME $HOME

# USER $USER_NAME

# Installing PortAudio dependencies (no londer needed)
#RUN cd /packages && apt install -y ./libfftw3-single3_3.3.5-3_amd64.deb
#RUN cd /packages && apt install ./libasound2-data_1.1.3-5_all.deb
#RUN cd /packages && apt install ./libasound2_1.1.3-5_amd64.deb
#RUN cd /packages && apt install ./libkmod2_23-2_amd64.deb
#RUN cd /packages && apt install ./kmod_23-2_amd64.deb
#RUN cd /packages && apt install ./libjack-jackd2-0_1.9.12~dfsg-2_amd64.deb
#RUN cd /packages && apt install ./libportaudio2_19.6.0-1_amd64.deb
#RUN cd /packages && apt install ./libslang2_2.3.1-5_amd64.deb
#RUN cd /packages && apt install ./libnewt0.52_0.52.19-1+b1_amd64.deb
#RUN cd /packages && apt install ./whiptail_0.52.19-1+b1_amd64.deb
#RUN cd /packages && apt install ./alsa-utils_1.1.3-1_amd64.deb

# Jupyter Notebooks sublime text keymap (no londer needed)
# ADD scripts/add_sublime_shortcuts.py /
# RUN python3 /add_sublime_shortcuts.py

# pulseaudio --log-level=4 --log-target=stderr -v

# ENV JUPYTER_TOKEN = 'dsp' # Set a custom password
# $ jupyter notebook password
# Enter password:  ****
# Verify password: ****

# Jupyter Notebooks settings
RUN jt -t onedork -N -kl # Selecting the theme (-T)
#RUN jupyter dashboards quick-setup --sys-prefix # Activating the dashboard extension
RUN jupyter contrib nbextension install --user
RUN jupyter nbextensions_configurator enable --user

# ENTRYPOINT [ "pulseaudio" ]
# CMD [ "--log-level=4", "--log-target=stderr", "-v" ]

# Start commands
ADD scripts/start.sh /
CMD /start.sh

#ENTRYPOINT cd /notebooks/examples/voila-notebooks/ && voila bqplot.ipynb # Voila application
