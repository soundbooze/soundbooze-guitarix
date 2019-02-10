#!/bin/sh

mod-host &
sleep 2
python init.py > /dev/null 2>&1

while [ 1 ]
do
  jack_capture_ms -d 1000 -p system:playback* -f wav out.wav > /dev/null 2>&1
  ffmpeg -i out.wav tmp.wav > /dev/null 2>&1
  BPM=`aubio tempo tmp.wav | awk '{ print $1 }'`
  python param_delay.py $BPM > /dev/null 2>&1
  rm -f out.wav tmp.wav
done
