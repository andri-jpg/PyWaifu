import time
import tkinter as tk
import numpy as np
from tts import tts_infer
from translate import translator
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyaudio
import soundfile as sf
import scipy.io.wavfile as wavfile
import logging
from selenium.webdriver.remote.remote_connection import LOGGER

# Set logging level to warning
LOGGER.setLevel(logging.WARNING)

# Initialize text-to-speech model
ts = tts_infer(model_name='chihiro') # change model_name to .pth file in model folder

# Initialize translator
tl = translator()

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
    

# Create a new Tkinter window
root = tk.Tk()
# Create a new Tkinter window

# Set the window to always be on top
root.attributes("-topmost", True)

# Set the window size
root.geometry("800x600")
# Create a label to display the en_answer
en_answer_label = tk.Label(root, text="")
en_answer_label.pack()

# Create an entry to get user input
user_input_entry = tk.Entry(root)
user_input_entry.pack()

# Create a button to send user input
send_button = tk.Button(root, text="Send", command=lambda: send_user_input())
send_button.pack()

def send_user_input():
    # Get user input from entry
    user_input = user_input_entry.get()
    
    # Clear the entry
    user_input_entry.delete(0, tk.END)
    
    # Send user input to chat application
    text_input = driver.find_element(By.XPATH, '//*[@id="cht_inp"]')
    text_input.click()
    text_input.send_keys(user_input)
    text_input.send_keys('\ue007')
    
    # Lock the send button
    send_button.config(state=tk.DISABLED)

def update_en_answer(en_answer):
    # Update the en_answer label with the new en_answer
    en_answer_label.config(text=en_answer)

# Initialize a flag to check if audio has been played for the current response
audio_played = False

# Initialize a flag to check if audio has been played for the current response
audio_played = False

# Main loop
while True:
    # Check if chatbot is currently generating a response
    generating = driver.find_elements(By.CLASS_NAME,'hidden')
    
    if len(generating) < 31:
        if_busy = True
        #print("generating")
    else:
        if_busy = False

    time.sleep(0.01)

    # If chatbot is busy generating response, continue loop
    if if_busy:
        continue
    else:
        # Get English response from chat application
        en_answer = cleaner(get_answer())
        
        # Update the en_answer label with the new en_answer
        update_en_answer(en_answer)

        # Translate English response to Japanese
        jp_answer = tl.en_jp(en_answer)

        # Convert Japanese response to speech and play audio
        ts.convert(jp_answer)
        if jp_answer is not None and not audio_played:
            play_audio()
            
            # Set the audio_played flag to True to prevent audio from being played again
            audio_played = True
            
            # Unlock the send button after playing audio
            send_button.config(state=tk.NORMAL)
            
            # Wait for user input before continuing the loop
            root.wait_variable(tk.StringVar())
            
            # Reset the audio_played flag to False to allow audio to be played again for the next response
            audio_played = False

    # Update the Tkinter window
    root.update_idletasks()
    root.update()