# PyWaifu: Virtual Anime Waifu Interaction Pipeline

## Description:
PyWaifu is an all-in-one pipeline designed to facilitate seamless interactions with virtual anime waifus through Text-to-Speech (TTS), language modeling, and translation capabilities. The primary objective of this project is to enable users to engage in immersive and lifelike conversations with their favorite virtual anime waifus. With PyWaifu, users can generate natural-sounding speech from text inputs, engage in interactive dialogues using advanced language models, and even translate their conversations into different languages. This unique integration of TTS, language modeling, and translation technologies brings a whole new level of interactivity and enjoyment to the anime fandom, providing users with an unforgettable experience of communicating with their cherished virtual companions.

PyWaifu runs offline on your PC and requires at least 4GB VRAM of an NVIDIA GPU and 6GB of RAM (in GPU mode) or 8GB of RAM (in CPU mode).

src/example.mp4

## Requirements:
- Git
- Python 3.9.16 (recommended)

## Installation:
- Make sure you have installed C/C++ build tools and have CMake installed.
- Set up a virtual environment (venv) or install Miniconda (optional but strongly recommended).
- Clone the repository:
  ```bash
  git clone https://github.com/andri-jpg/PyWaifu
  cd PyWaifu
  ```
- Install the required packages:
  ```bash
  pip install -r requirements.txt

  cd monotonic_align
  python setup.py build_ext --inplace
  ```
- If you are using an NVIDIA GPU, run the following command:
  ```bash
  pip install torch==1.13.1+cu117 torchvision==0.14.1+cu117 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu117
  ```

## Usage:
- Run `main.py`:
  ```bash
  # For the default mode
  python main.py

  # For Indonesian mode
  python main_indonesia.py
  ```

Note: You will be prompted to download the suggested model when running `main.py`. It is recommended to enter 'y' for all questions if you are unsure.

- The PyWaifu window will appear.
- You can now enter your input in the text box.
- You can change the VITS model by replacing the `herta.pth` and `config.json` files in the `model` folder.

## Credits:
- [llm-rs](https://github.com/LLukas22/llm-rs-python)
- [vits-finetuning](https://github.com/SayaSS/vits-finetuning)
- [Helsinki-NLP](https://huggingface.co/Helsinki-NLP)
- [staka/fugumt](https://huggingface.co/staka/fugumt-ja-en)
- [rustformers](https://github.com/rustformers/llm)
