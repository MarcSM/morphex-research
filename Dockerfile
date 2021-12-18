FROM mtgupf/mir-toolbox

# Copy external libraries to the image
COPY externals/sms-tools /sms-tools
# COPY externals/portaudio /portaudio
# COPY externals/packages /packages

# Upgrade pip
RUN pip3 install --upgrade pip

# Installing PyAudio, PortAudio and PulseAudio (WIP)
# RUN apt-get update
# RUN apt-get install python-pyaudio -y
# # RUN pip install --upgrade setuptools
# RUN apt-get install portaudio19-dev -y
# RUN apt-get install pulseaudio -y

# # Installing PortAudio dependencies (WIP)
# RUN apt-get update && apt-get install -y \
# 	m4 \
# 	intltool \
# 	libtool \
# 	libsndfile-dev \
# 	libcap-dev

# # Installing PulseAudio dependencies (WIP)
# RUN cd /packages/pulseaudio-12.2 && ./configure --prefix=/usr        \
# 									            --sysconfdir=/etc    \
# 									            --localstatedir=/var \
# 									            --disable-bluez4     \
# 									            --disable-bluez5     \
# 									            --disable-rpath
# RUN cd /packages/pulseaudio-12.2 && make && make install
# RUN rm -fv /etc/dbus-1/system.d/pulseaudio-system.conf

# # Installing needed librearies for live audio (WIP)
# RUN apt-get update && apt-get install -y \
# 	alsa-utils \
# 	libasound2 \
# 	libasound2-plugins \
# 	python-pyaudio \
# 	portaudio19-dev \
# 	pavucontrol \
# 	--no-install-recommends \
# 	&& rm -rf /var/lib/apt/lists/*

# Requirements
ADD requirements.txt /tmp/requirements/requirements.txt
RUN pip3 install -r /tmp/requirements/requirements.txt

# Compiling sms-tools
RUN cd /sms-tools/software/models/utilFunctions_C && python3 compileModule.py build_ext --inplace

# # Ading a new user for PulseAudio (WIP)
# ENV USER mir
# ENV HOME /home/mir
# RUN groupadd pulse
# RUN groupadd pulse-access
# RUN usermod -aG audio,pulse,pulse-access mir \
#     && chown -R mir:mir $HOME
# USER mir

# # Copy PulseAudio config files (WIP)
# COPY --chown=mir:mir config/jupyter_notebook_config.json /home/mir/.jupyter/
# RUN mkdir -p /home/mir/.config/pulse
# COPY externals/pulseaudio/default.pa /etc/pulse/default.pa
# COPY externals/pulseaudio/client.conf /etc/pulse/client.conf
# COPY externals/pulseaudio/daemon.conf /etc/pulse/daemon.conf

# # Run PulseAudio server on your host (WIP)
# ENV PULSE_SERVER = docker.for.mac.localhost # macos only
# RUN adduser mir pulse-access

# Jupyter Notebooks settings
RUN jt -t onedork -N -kl # Selecting the theme (-T)
#RUN jupyter dashboards quick-setup --sys-prefix # Activating the dashboard extension
RUN jupyter contrib nbextension install --user
RUN jupyter nbextensions_configurator enable --user

# Start commands
ADD scripts/start.sh /
CMD /start.sh
