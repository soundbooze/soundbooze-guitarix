import os
import sys
import signal
import librosa
import numpy as np

import socket, time
import subprocess as sp

# get mod-host pid
pid = sp.check_output("pgrep mod-host; exit 0", shell=True)
if pid == '':
    print 'mod-host is not running'
    exit(0)

# setup socket
s = socket.socket()
s.connect(('127.0.0.1', 5555))
s.settimeout(5)

def check_mod_host():
    if sp.check_output("pgrep mod-host; exit 0", shell=True) != pid:
        print 'mod-host died'
        exit(1)

def send_command(command):
    s.send(command)
    print 'sent:', command
    check_mod_host()

    try:
        resp = s.recv(1024)
        if resp: print 'resp:', resp
        return True

    except Exception:
        return False

# ----------------------------------------------------

def Initialize():  
    signal.signal(signal.SIGINT, SignalExit)

def SignalExit(signal, frame):
    os.system("rm -f playback.wav guitar.wav")
    sys.exit(0)

def dB2Amplitude(db):
    return pow(10, db / 20);
		
def CaptureDB():

    SILENT_THRESHOLD = -51

    y1 = []
    y2 = []
    sr1 = 0
    sr2 = 0

    os.system("(jack_capture_ms -p 'PulseAudio JACK Sink:front*' -d 500 -f wav playback.wav > /dev/null 2>&1) | (jack_capture_ms -p jack_thru:output* -d 500 -f wav guitar.wav > /dev/null 2>&1)")

    y1, sr1 = librosa.load('playback.wav')
    y2, sr2 = librosa.load('guitar.wav')

    S1 = np.abs(librosa.stft(y1))
    S2 = np.abs(librosa.stft(y2))

    ypow1 = librosa.power_to_db(S1**2)
    ypow2 = librosa.power_to_db(S2**2)

    system = np.average(ypow1)
    guitar = np.average(ypow2)

    if (system <= SILENT_THRESHOLD and guitar <= SILENT_THRESHOLD):
      return -1

    else :
      fs = '[Playback]: ' + repr(system) + ' db'
      print fs

      fg = '[Guitar]: ' + repr(guitar)  + ' db'
      print fg

      dist = '[Distance]: ' + repr(system - guitar) + ' db'
      print dist

      gain = -11 + dB2Amplitude(system - guitar) 
      send_command('param_set 1 gain %f' % gain)

      return 0

if __name__ == "__main__":

    Initialize()

    while (1):
        CaptureDB()
