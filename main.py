import time
import PySimpleGUIQt as sg
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
    model="RedPajama-INCITE-Chat-3B-v1-q5_1.bin", # Replace with the name of your desired model
    name='<andri>',  # Replace with your preferred name
    assistant_name='<herta>')  # Replace with the desired name for the assistant 

# Initialize TTS
ts = tts_infer(model_name='herta')  # Replace with the name of the TTS model you want to use for TTS initialization

# Initialize Translator
tl = translator(indonesian=False)

##### Main #####

p = pyaudio.PyAudio()

# Get available audio devices
info = p.get_host_api_info_by_index(0)
num_devices = info.get('deviceCount')
for i in range(num_devices):
    device = p.get_device_info_by_host_api_device_index(0, i)
    print(device['index'], device['name'])

# Select an output device
output_device_index = int(input("Enter the index of the virtual microphone device: "))
output_device_info = p.get_device_info_by_index(output_device_index)

output_device_index2 = int(input("Enter the index of the output device: "))
output_device_info2 = p.get_device_info_by_index(output_device_index2)

def play_audio():
    filename = 'dialog.wav'
    data, samplerate = sf.read(filename, dtype='float32')

    # Convert float32 to int16
    data_int = (data * 32767).astype(np.int16)

    # Open the audio stream with the selected output device
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=samplerate,
                    output=True,
                    output_device_index=output_device_index)

    stream_s = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=samplerate,
                    output=True,
                    output_device_index=output_device_index2)

    chunk_size = 1024  # adjust this value to change the chunk size
    i = 0
    while i < len(data_int):
        chunk_end = min(i + chunk_size, len(data_int))
        stream.write(data_int[i:chunk_end].tobytes())
        stream_s.write(data_int[i:chunk_end].tobytes())
        i += chunk_size

    stream.stop_stream()
    stream_s.stop_stream()
    stream.close()
    stream_s.close()

def clean_res(result, words_to_clean):
    cleaned_result = result
    for word in words_to_clean:
        cleaned_result = cleaned_result.replace(word, "")
    return cleaned_result

# Tema antarmuka pengguna
sg.theme("DarkGrey2")

# Tampilan antarmuka pengguna
layout = [
    [sg.Text("Input:", size=(8, 1)), sg.Input(key="-INPUT-", size=(30, 1), enable_events=True, return_keyboard_events=True),sg.Button("Submit")],
    [sg.Text("Result: ")],
    [sg.Multiline("", key="-OUTPUT-", size=(80, 20), background_color="white", text_color="black")]
]


# Membuat window
window = sg.Window("Kuru kuru 😂", layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == "Submit" or event == "\r":  # Jika tombol "Submit" atau tombol Enter ditekan
        user_input = values["-INPUT-"]
        user_input = tl.id_en(user_input)

        if user_input.lower() == "exit":
            break

        result = generator.chain(user_input)
        result = result["text"]
        words_to_clean = ["\n<human", "\n<bot"]

        en_answer = clean_res(result, words_to_clean)
        jp_answer = tl.en_jp(en_answer)
        id_result = tl.en_id(en_answer)

        ts.convert(jp_answer)

        if "```python" in en_answer:
            code_match = re.search(r"```python(.+?)```", en_answer, re.DOTALL)
            if code_match:
                code = code_match.group(1).strip()
                window["-OUTPUT-"].update(id_result, font=("Courier New", 11), background_color="black",
                                          text_color="white")
        else:
            window["-OUTPUT-"].update(id_result, font=("Arial", 11), background_color="white", text_color="black")

        window.refresh()  # Memastikan tampilan terbaru ditampilkan
        window["-INPUT-"].update("")  # Menghapus teks pada kotak input

        if jp_answer is not None:
            play_audio()

window.close()
