<div align="center">
<h1>PyWaifu: Virtual Anime Waifu Interaction Pipeline</h1>
  
[![madewithlove](https://forthebadge.com/images/badges/built-with-love.svg)](https://github.com/andri-jpg/PyWaifu)

</div>

Simple UI web based version [chatwaifu](https://github.com/andri-jpg/chatwaifu)

## Description:
PyWaifu is an all-in-one pipeline designed to facilitate seamless interactions with virtual anime waifus through Text-to-Speech (TTS), language modeling, and translation capabilities. The primary objective of this project is to enable users to engage in immersive and lifelike conversations with their favorite virtual anime waifus. With PyWaifu, users can generate natural-sounding speech from text inputs, understand the emotional expressions of generated text, easily customize the system, and even translate their conversations into different languages. This unique integration of TTS, language modeling, and translation technologies brings a whole new level of interactivity and enjoyment to the anime fandom, providing users with an unforgettable experience of communicating with their cherished virtual companions.

PyWaifu runs offline on your PC and requires at least 8gb of RAM (in CPU mode).

## The anime character illustrations used in this project are provided by @Zr6Ov through Picrew. <br> Twitter: [@Zr6Ov](https://twitter.com/Zr6Ov) <br> Picrew Profile Link: [✦絢瀬](https://picrew.me/en/search/creator?crid=1560771)

*Sound on 🔊

https://github.com/andri-jpg/PyWaifu/assets/91838310/05ed2c6d-498b-4a11-a7e7-afb5376cb8ff

## Features:
- Text-to-Speech (TTS) conversion
- Emotion understanding: PyWaifu can analyze the emotional expressions conveyed in the generated text, allowing for a more engaging and dynamic interaction.
- Customizability: Easily customize and personalize the PyWaifu system according to your preferences.
- Translation capabilities: Translate conversations with your virtual waifu into different languages, broadening the reach and accessibility of your interactions.
- User-friendly interface: PyWaifu provides a graphical user interface (GUI) for easy interaction
- Offline: PyWaifu runs locally on your PC, without the need for an internet connection.

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
  
  ```

## Usage:
- Run `main.py`:
  ```bash
  # For the default mode
  python main.py

  # For Indonesian mode
  python main_indonesian.py
  ```

Note: You will be prompted to download the suggested model when running `main.py`. It is recommended to enter 'y' for all questions if you are unsure.

- The PyWaifu window will appear.
- You can now enter your input in the text box.
- You can change the VITS model by replacing the `herta.pth` and `config.json` files in the `model` folder.

## Todo:
- Implement threading and optimize the code for better performance.
- Polish the graphical user interface (GUI) to enhance the visual appeal and user experience.
- Add more customization options to allow users to personalize the application according to their preferences.
- Incorporate animation into the GUI to make it more dynamic and engaging.
- Create an executable binary of the project using PyInstaller for easy distribution and deployment.

## Your feedback is valuable and contributions through pull requests are welcomed to make this project even better.

[![buymekofi](src/kofi.png)](https://ko-fi.com/andrilawrence#)

## Credits:
- [pysentimentio](https://github.com/pysentimiento)
- [@Zr6Ov](https://twitter.com/Zr6Ov)
- [zomehwh](https://huggingface.co/spaces/zomehwh/vits-models)
- [llm-rs](https://github.com/LLukas22/llm-rs-python)
- [vits-finetuning](https://github.com/SayaSS/vits-finetuning)
- [Helsinki-NLP](https://huggingface.co/Helsinki-NLP)
- [staka/fugumt](https://huggingface.co/staka/fugumt-ja-en)
- [rustformers](https://github.com/rustformers/llm)
