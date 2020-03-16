import videomanager
import auxiliary

print("----")
print("Welcome to KARAOKE UNLIMITED (text ver)!")
print("Brandon Lee 2020")
print("----")

# The instructions and their functions

class INSTR:
    all_instr = {}

    name = ""
    desc = ""
    fxn = None

    def __init__(self, name, desc, fxn):
        self.name = name
        self.desc = desc
        self.fxn = fxn
        INSTR.all_instr[self.name] = self

def HELP_fxn():
    for name, i in INSTR.all_instr.items():
        print(name + " : " + i.desc)
INSTR("HELP", "Prints a list of instructions", HELP_fxn)

def QUIT_fxn():
    pass
INSTR("QUIT", "Ends the program", QUIT_fxn)

def ADDVID_fxn():
    url = input("What is the YouTube URL of the video? ")
    if videomanager.download_video(url) == 1:
        print("Failed to add video.")
INSTR("ADDVID", "Takes a YouTube URL and downloads the video into the library", ADDVID_fxn)

def DELVID_fxn():
    name = input("What video would you like to delete? ")
    if videomanager.delete_video(name) == 1:
        print("Failed to delete.")
INSTR("DELVID", "Removes a video from the library", DELVID_fxn)

def RENAME_fxn():
    prevname = input("What is the video you would like to rename? ")
    newname = input("What would you like to rename it to? ")
    if videomanager.rename_video(prevname, newname) == 1:
        print("Failed to rename.")
INSTR("RENAME", "Renames a video in the library", RENAME_fxn)

def LISTVIDS_fxn():
    for videoname in videomanager.video_list():
        print(videoname)
INSTR("LISTVIDS", "Lists all the videos in the library", LISTVIDS_fxn)

def PLAYVID_fxn():
    name = input("What video would you like to play? ")
    videomanager.play_video(name)
INSTR("PLAYVID", "Plays a video in the library", PLAYVID_fxn)

# Runs the loop

print("Enter " + INSTR.all_instr["HELP"].name + " for a list of instructions.")

inp = ""
while inp != INSTR.all_instr["QUIT"].name:
    print()
    inp = input(">>> ")
    try:
        INSTR.all_instr[inp].fxn.__call__()
    except:
        print("Invalid command.")