import time

from pygame import mixer
mixer.init()

#~ mixer.Sound("background-sounds/intense_knives_out.wav").play()
mixer.music.load("background-sounds/intense_knives_out.wav")
mixer.music.play()
time.sleep(30)
