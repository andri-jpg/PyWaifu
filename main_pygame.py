import pygame
import pygame_gui
from pygame_gui.elements import UIWindow
from pygame_gui.elements import UIPanel
import time
import numpy as np
from tts import tts_infer
from translate import translator
from llm_models import ChainingModel
import pyaudio
import soundfile as sf
import scipy.io.wavfile as wavfile
import logging
import os
import re

##### Configuration #####
# Change the parameters below to use your desired model and customize names
generator = ChainingModel(
    model="RedPajama-INCITE-Chat-3B-v1-q5_1", # Replace with your desired model
    name='andri',  # Replace with your preferred name
    assistant_name='herta')  # Replace with the desired name for the assistant

# Initialize VITS
ts = tts_infer(model_name='herta')  # Replace with the name of the VITS model you want to use for VITS initialization

# Initialize Translator
tl = translator(indonesian=True)

##### Main #####

p = pyaudio.PyAudio()


def play_audio():
    filename = 'dialog.wav'
    data, samplerate = sf.read(filename, dtype='float32')

    data_int = (data * 32767).astype(np.int16)

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=samplerate,
                    output=True)

    chunk_size = 1024
    i = 0
    while i < len(data_int):
        chunk_end = min(i + chunk_size, len(data_int))
        stream.write(data_int[i:chunk_end].tobytes())
        i += chunk_size

    stream.stop_stream()
    stream.close()

def clean_res(result, words_to_clean):
    cleaned_result = result
    for word in words_to_clean:
        cleaned_result = cleaned_result.replace(word, "")
    return cleaned_result

pygame.init()
pygame.display.set_caption('PyWaifu')
window_surface = pygame.display.set_mode((800, 600))
manager = pygame_gui.UIManager((800, 600), 'theme1.json')

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#be76b5'))
words_to_clean = ["\n<human", "\n<bot"]
text_panel = UIPanel(pygame.Rect(0,500,700,100))
def generated_text(result):
    pygame_gui.elements.UITextBox(html_text=result,
                              relative_rect=pygame.Rect((0, 500), (700, 100)),
                              manager=manager)

def config():
    config_windows = UIWindow(pygame.Rect(0, 300, 300, 300), manager=manager, window_display_title='config')
    test_slider = pygame_gui.elements.UIHorizontalSlider(pygame.Rect((60, 100), (150, 25)), 50.0, (0.0, 100.0),
                                                         manager=manager,
                                                         container=config_windows,
                                                         click_increment=5)

a = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((450, 450), (250, 40)),
                                        manager=manager, placeholder_text='input text here')
test_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 500), (100, 40)), manager=manager,
                                           text='hide')
test_button2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 550), (100, 40)), manager=manager,
                                            text='config')
loaded_test_image = pygame.image.load('test.png')
panel = UIPanel(pygame.Rect(0, 300, 205, 205))
test_image = pygame_gui.elements.UIImage(pygame.Rect((0, 0), (200, 200)),
                                         loaded_test_image,
                                         manager=manager, container=panel)

clock = pygame.time.Clock()
is_running = True


while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            user_input = event.text
            a.hide()
            generated_text("generating....")
            try:
                user_input = tl.id_en(user_input)
                result = generator.chain(user_input)
                result = result["text"]
                en_answer = clean_res(result, words_to_clean)
                jp_answer = tl.en_jp(en_answer)
                id_result = tl.en_id(en_answer)
                ts.convert(jp_answer)
                generated_text(id_result)
                if jp_answer is not None:
                    play_audio()
                a.show()
            except:
                print('5')
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == test_button:
                a.hide()
            if event.ui_element == test_button2:
                config()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            generated_text()

        if event.type == pygame.KEYDOWN:
            a.show()
        if event.type == pygame.QUIT:
            is_running = False

        manager.process_events(event)
        



    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
        
