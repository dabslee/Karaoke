import pafy
import os
import pyglet

ROOTPATH = "resources/videos/"

def download_video(url):
    video = pafy.new(url)
    best = video.getbest()
    best.download(quiet=False, filepath=ROOTPATH)

def rename_video(currentname, futurename):
    try:
        os.rename(ROOTPATH+currentname+".mp4", ROOTPATH+futurename+".mp4")
        return 0
    except:
        return 1

def delete_video(name):
    try:
        os.remove(name+".mp4")
        return 0
    except:
        return 1

def video_list():
    return list([s.rstrip(".mp4") for s in os.listdir(ROOTPATH)])

def has_video(name):
    return name in video_list()

def play_video(name):
    vidPath = ROOTPATH+name+".mp4"
    window = pyglet.window.Window()
    player = pyglet.media.Player()
    source = pyglet.media.StreamingSource()
    MediaLoad = pyglet.media.load(vidPath)

    player.queue(MediaLoad)
    player.play()

    @window.event
    def on_draw():
        if player.source and player.source.video_format:
            player.get_texture().blit(50,50)

    pyglet.app.run()