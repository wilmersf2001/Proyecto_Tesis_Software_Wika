import os
import pygame
from gtts import gTTS
from time import sleep

class TextToSpeech:
    @staticmethod
    def text_to_speech(text):
        tts = gTTS(text=text, lang='es')
        filename = "speech.mp3"
        tts.save(filename)

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            sleep(1)

        pygame.mixer.quit()
        pygame.quit()

        os.remove(filename)



