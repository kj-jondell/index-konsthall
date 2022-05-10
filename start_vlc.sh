#!/bin/bash
export DISPLAY=:0.0
export VLC_JACK_NAME=vlc
export SC_JACK_DEFAULT_INPUTS=""

/home/pi/index/start_sc.scd &
#jackd -d alsa -d hdmi:CARD=vc4hdmi0 & #RUNS FROM systemd INSTEAD
sleep 5
/home/pi/index/buttons.py &
sleep 5
cvlc -f /home/pi/tragedy_4.mov --aout jack -L --jack-name $VLC_JACK_NAME --no-osd --jack-connect-regex ^SuperCollider &
