import time
import vlc

player = vlc.MediaPlayer("background-sounds/countdown.mp4")
player.play()
time.sleep(10)
player.stop()
