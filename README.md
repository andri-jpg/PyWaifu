# PyWaifu: Virtual Anime Waifu Interaction Pipeline
## Description:
PyWaifu is an all-in-one pipeline designed to facilitate seamless interactions with virtual anime waifus through Text-to-Speech (TTS), language modeling, and translation capabilities. The primary objective of this project is to enable users to engage in immersive and lifelike conversations with their favorite virtual anime waifus. With PyWaifu, users can generate natural-sounding speech from text inputs, engage in interactive dialogues using advanced language models, and even translate their conversations into different languages. This unique integration of TTS, language modeling, and translation technologies brings a whole new level of interactivity and enjoyment to the anime fandom, providing users with an unforgettable experience of communicating with their cherished virtual companions.

All of this run Offline on your pc
need atleast 4gb vram of nvidia gpu and 6gb ram (GPU mode)
or 8 gb ram(CPU mode)
## Requirements
- git
- python tested on 3.9.16(recommended)
  
## Installation
- Make sure you have Installed C/C++ build tools and have Cmake installed 
- venv or miniconda(optional but strongly recommended)
- clone the repo
```bash
git clone https://github.com/andri-jpg/PyWaifu
cd ./AIwaifu-png
```
- Install requirements
```bash
pip install -r ./requirements.txt

cd monotonic_align
python setup.py build_ext --inplace
```
- If you using nvidia GPU, Run line below
```bash
pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu117
```
## Usage
- Run main.py
```bash
# for default mode
python main.py
# for indonesian mode
python main_indonesia.py
```
note : there will be a question to download suggested model when run main.py (I suggest you to enter 'y' on all question if you don't know what to do)
- then a pywaifu windows will appear
- Now you can send your input from text box.
- You can change your vits model in model folder, replace herta.pth and config.json
# Credit
[llm-rs](https://github.com/LLukas22/llm-rs-python)
[vits-finetuning](https://github.com/SayaSS/vits-finetuning)
[Helsinki-NLP](https://huggingface.co/Helsinki-NLP)
[staka/fugumt](https://huggingface.co/staka/fugumt-ja-en)
[rustformers](https://github.com/rustformers/llm)
