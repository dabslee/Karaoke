import os
import sounddevice
import scipy.io.wavfile
import threading
import numpy

import random

gametitle = "Karaoke Unlimited"
fps = 60

# Basic color library
COLORS = {"BLACK": (0,0,0),
          "WHITE": (255,255,255),
          "RED": (255,0,0),
          "ORANGE": (255,165,0),
          "YELLOW": (255,255,0),
          "GREEN": (0,255,0),
          "BLUE": (0,0,255),
          "INDIGO": (75,0,130),
          "VIOLET": (238,130,238),
          "MAGENTA": (255,0,255),
          "CYAN": (0,255,255),}

# Importing images
_image_library = {}
def get_image(path):
    path = "resources/images/" + path
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image.convert_alpha()

# Recording object, also able to compare audio files
# The main engine of the karaoke calculator
class Recorder:
    INTERNAL = "internal"
    EXTERNAL = "external"

    fs = 44100 # Sample rate
    samplings = 0.1 # Duration (in s) of recording samplings
    externalinternal = EXTERNAL
    targetfilepath = "resources/audio/" + externalinternal + ".wav"

    recording = False
    fullrec = None

    def __init__(self, externalinternal):
        self.externalinternal = externalinternal
        self.targetfilepath = "resources/audio/" + externalinternal + ".wav"

    def record(self):
        sectionrec = sounddevice.rec(int(self.samplings*self.fs), samplerate=self.fs, channels=2)
        sounddevice.wait()
        self.fullrec = sectionrec
        while (self.recording):
            sectionrec = sounddevice.rec(int(self.samplings*self.fs), samplerate=self.fs, channels=2)
            sounddevice.wait()
            self.fullrec = numpy.concatenate([self.fullrec,sectionrec])

    def begin_recording(self):
        self.recording = True
        x = threading.Thread(target=self.record, args=())
        x.start()

    def end_recording(self):
        scipy.io.wavfile.write(self.targetfilepath, self.fs, self.fullrec)
        self.recording = False

# Compares two numpy arrays and returns similarity
def compareNparr(arr1, arr2):
    list1 = arr1.tolist()
    list2 = arr2.tolist()
    compels = min(len(list1), len(list2))

    # Calculate manhattan distance between arr1 and arr2
    manhattan = 0
    for i in range(compels):
        manhattan += abs(list1[i][0] - list2[i][0])
        manhattan += abs(list1[i][1] - list2[i][1])
        
    # Calculate final score
    maxmanhattan = 2*compels
    score = 1 - (manhattan/maxmanhattan)**(0.01)
    return score