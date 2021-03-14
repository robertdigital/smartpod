from gtts import gTTS


import pygame
import time, sys

from pygame import mixer
from io import BytesIO



def tts(text):


    

    # initialize tts, create mp3 and play
    tts = gTTS(text, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

temp = "71"        
#text = ("{}".format("temp"))
word = 'The temperature is "{}" degrees fahrenheit.'.format(temp)
tts(word)