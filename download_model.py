import wget
import os
import subprocess
import os

import requests

url = "https://huggingface.co/Kastor/GPT-J-6B-Pygway-ggml-q4_1/blob/main/GPT-J-6B-Pygway-v2-ggml-q4_1.bin"
response = requests.get(url)

with open("filename", "wb") as file:
    file.write(response.content)

current_dir = os.getcwd()

repo_url = "https://huggingface.co/AndriLawrence/Vits-chihiro"
local_path = current_dir + "/model"
subprocess.run(["git", "clone", repo_url, local_path])

repo_url = "https://huggingface.co/staka/fugumt-en-ja"
local_path = current_dir + "/fugumt-en-ja"
subprocess.run(["git", "clone", repo_url, local_path])

repo_url = "https://huggingface.co/Helsinki-NLP/opus-mt-en-id"
local_path = current_dir + "/opus-mt-en-id"
subprocess.run(["git", "clone", repo_url, local_path])

repo_url = "https://huggingface.co/Helsinki-NLP/opus-mt-id-en"
local_path = current_dir + "/opus-mt-id-en"
subprocess.run(["git", "clone", repo_url, local_path])