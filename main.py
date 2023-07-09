import pygame
import pygame_gui
from pygame_gui.elements import UIWindow, UIPanel, UITextBox, UITextEntryLine, UIButton, UIImage
import time
import json
import numpy as np
import pyaudio
import random
import soundfile as sf
from tts import tts_infer
from translate import translator
from llm_models import ChainingModel
import threading
from pysentimiento import create_analyzer

with open('config.json') as user_config:
    configs = json.load(user_config)

name=configs['user_name']  
assistant_name=configs['bot_name']

generator = ChainingModel(
    model=configs['model_name'],
    name=name,  
    assistant_name=assistant_name  
)

ts = tts_infer(model_name=configs['vits_model']) 
tl = translator(indonesian=False)


pygame.init()
pygame.display.set_caption('PyWaifu')
window_surface = pygame.display.set_mode((800, 600))
manager = pygame_gui.UIManager((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#cc8890'))
words_to_clean = ["\n<human", "\n<bot"]

def change_words(words, name, assistant_name):
    new_words = []
    for word in words:
        new_word = word.replace('human', name)
        new_words.append(new_word)
        new_word = word.replace('bot', assistant_name)
        new_words.append(new_word)
    return new_words

words_clean = change_words(words_to_clean, name, assistant_name)

def play_audio(callback):
    
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
    if callable(callback):
        callback()
        
def clean_res(result, words_to_clean):
    cleaned_result = result
    for word in words_clean:
        cleaned_result = cleaned_result.replace(word, "")
    return cleaned_result

class OutputText:
    def __init__(self, manager):
        self.manager = manager

    def generated_text(self, result):
        self.text = pygame_gui.elements.UITextBox(html_text=result,
                                                  relative_rect=pygame.Rect((0, 500), (700, 100)),
                                                  manager=self.manager)
        
        self.text.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR,
                                    params={'time_per_letter': 0.001,
                                            'time_per_letter_deviation': 0.01})
    def generating(self):
        self.text = pygame_gui.elements.UITextBox(html_text='Generating.....',
                                                  relative_rect=pygame.Rect((0, 500), (700, 100)),
                                                  manager=self.manager)

output_text = OutputText(manager)
output_text.generated_text('Ready')

emotion_analyzer = create_analyzer(task="emotion", lang="en",model_name='bertweet-base-emotion-analysis')

text_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((450, 450), (250, 40)),
                                               manager=manager, placeholder_text='input text here')

test_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 500), (100, 40)), manager=manager,
                                           text='input')

test_button2 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 550), (100, 40)), manager=manager,
                                            text='config')

idle = [pygame.image.load('waifu/idle.png')]
blink = [pygame.image.load('waifu/blink.png')]
others = [pygame.image.load(f"waifu/other{i}.png") for i in range(1, 6)]
anger = [pygame.image.load(f"waifu/anger{i}.png") for i in range(1, 3)]
disgust = [pygame.image.load(f"waifu/disgust{i}.png") for i in range(1, 3)]
fear = [pygame.image.load(f"waifu/fear{i}.png") for i in range(1, 3)]
joy = [pygame.image.load(f"waifu/joy{i}.png") for i in range(1, 3)]
surprise = [pygame.image.load('waifu/surprise.png')]
sadness = [pygame.image.load('waifu/sad.png')]
emotion_images = {
    'joy': joy,
    'others': others,
    'surprise': surprise,
    'disgust': disgust,
    'sadness': sadness,
    'fear': fear,
    'anger': anger
}

panel = UIPanel(pygame.Rect(0, 300, 205, 205))

def panel_image(image_list):
    random_index = random.randint(0, len(image_list) - 1)
    image = image_list[random_index]
    test_image = pygame_gui.elements.UIImage(pygame.Rect((0, 0), (200, 200)),
                                            image,
                                            manager=manager, container=panel)

def pipeline(user_input):
    result = generator.chain(user_input)
    result = result["text"]
    en_answer = clean_res(result, words_to_clean)
    output_text.generated_text(en_answer)

    emotion = emotion_analyzer.predict(en_answer).output 
    if emotion in emotion_images:
        panel_image(emotion_images[emotion])
    text_box.enable()
    jp_answer = tl.en_jp(en_answer)
    ts.convert(jp_answer)

    if jp_answer is not None:
        def callback():
            if emotion in emotion_images:
                panel_image(emotion_images[emotion])
            text_box.enable()
            
        threading.Thread(target=play_audio, args=(callback,)).start()



def config():
        config_windows = UIWindow(pygame.Rect(0, 300, 300, 300), manager=manager, window_display_title='config')
        test_slider = pygame_gui.elements.UIHorizontalSlider(pygame.Rect((60, 100), (150, 25)), 50.0, (0.0, 100.0),
                                                             manager=manager,
                                                             container=config_windows,
                                                             click_increment=5)



clock = pygame.time.Clock()
blink_duration = 0.2
idle_duration = 5.0 
last_blink_time = 0.0
is_idle = True
is_running = True
ready = False
p = pyaudio.PyAudio()

while is_running:
    if ready is True:
        pipeline(user_input)
        ready = False

    time_delta = clock.tick(30) / 1000.0
    current_time = time.time()
    
    for event in pygame.event.get():
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            user_input = event.text
            text_box.disable()
            output_text.generating()

            ready = True

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == test_button:
                text_box.enable()
            if event.ui_element == test_button2:
                config()

        if event.type == pygame.QUIT:
            is_running = False

        manager.process_events(event)
        
        if is_idle:
            if current_time - last_blink_time >= idle_duration:
                panel_image(blink)
                is_idle = False
                last_blink_time = current_time
        else:
            if current_time - last_blink_time >= blink_duration:
                panel_image(idle)
                is_idle = True
                last_blink_time = current_time
    
    manager.update(time_delta)
    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()

pygame.quit()
