import time
import numpy as np
from tts import tts_infer
from translate import translator
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyaudio
import soundfile as sf
import scipy.io.wavfile as wavfile
import logging
import os
#from selenium.webdriver.remote.remote_connection import LOGGER
#from urllib3.connectionpool import log as urllibLogger
# Set logging level to warning
#LOGGER.setLevel(logging.WARNING)
#urllibLogger.setLevel(logging.WARNING)
# Initialize text-to-speech model
# Set the threshold for selenium to WARNING
from selenium.webdriver.remote.remote_connection import LOGGER as seleniumLogger
seleniumLogger.setLevel(logging.WARNING)
# Set the threshold for urllib3 to WARNING
from urllib3.connectionpool import log as urllibLogger
urllibLogger.setLevel(logging.WARNING)
ts = tts_infer(model_name='herta') # change model_name to .pth file in model folder

# Initialize translator
tl = translator(indonesian=True)

# Initialize Selenium Chrome driver and load koboldcpp
driver = webdriver.Chrome()
page = "http://localhost:5001/#"
driver.get(page)

# clean text by removing line breaks
def cleaner(text):
    if text is None:
        return None
    else :
        return text.split('\n')[-1]

def get_answer():
    ans=driver.find_elements(By.TAG_NAME, 'p')
    line = []
    for i in ans:
        line.append(i)
    if not line:
        return None
    answer = line[-1].text
    return answer

# play audio
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

# Initialize flag to check if chatbot is busy generating response
if_busy = False

# Main loop
while True:
    # Check if chatbot is currently generating a response
    generating = driver.find_elements(By.CLASS_NAME,'hidden')
    
    if len(generating) < 31:
        if_busy = True
        #print("generating")
    else:
        if_busy = False
        
    time.sleep(0.5)

    # If chatbot is busy generating response, continue loop
    if if_busy:
        continue
    else:
        # Get English response from chat application
        en_answer = cleaner(get_answer())

        # Translate English response to Japanese
        jp_answer = tl.en_jp(en_answer)

        # Translate English response to Indonesian
        id_result = tl.en_id(en_answer)



        # If chatbot has just been loaded, prompt user to load configuration
        if id_result is None:
            print("Kamu baru memulai model, silahkan load config terlebih dahulu")
            user_input = input("Tekan tombol Enter jika sudah load config atau ketik 'exit' untuk keluar: ")
            if user_input.lower() == 'exit':
                break

        text_input = driver.find_element(By.XPATH, '//*[@id="cht_inp"]')
        text_input.click()
        ts.convert(jp_answer)
        os.system('cls')
        print(id_result)
        if jp_answer is not None:
            play_audio()
        user_input = input("Masukkan input, ketik 'exit' untuk keluar: ")
        user_input = tl.id_en(user_input)
        if user_input.lower() == 'exit':
            break
        text_input.send_keys(user_input)
        text_input.send_keys('\ue007')
        print("Memproses input user....")



