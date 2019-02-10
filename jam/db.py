import os
import librosa
import numpy as np

def CaptureLoad():

    SILENT_THRESHOLD = -41

    y1 = []
    y2 = []
    sr1 = 0
    sr2 = 0

    os.system("(jack_capture -p 'PulseAudio JACK Sink:front*' -d 1 -f wav playback.wav > /dev/null 2>&1) | (jack_capture -p jack_thru:output* -d 1 -f wav guitar.wav > /dev/null 2>&1)")

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

      return 0

    os.system('rm -f playback.wav guitar.wav')

if __name__ == "__main__":
    while (1):
        CaptureLoad()
