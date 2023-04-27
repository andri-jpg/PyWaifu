# AI-Waifu-png

# Readme in progress
All of this run on your local PC
need atleast 4gb vram of nvidia gpu and 12gb ram(GPU mode)
or 16 gb ram(CPU mode)
## Requirements
- git
- python > 3.7 <=3.10
- Veadotube mini [Download](https://olmewe.itch.io/veadotube-mini?download)
- Virtual audio cable, We recommend using VB-CABLE as a virtual cable solution [VB-cable](https://vb-audio.com/Cable/index.htm)
- Google Chrome [Download](https://www.google.com/chrome/)

## Installation
- Make sure you have Installed C/C++ build tools and have Cmake installed 
- Make sure to have [GIT LFS](https://git-lfs.com/) Installed to handle large file download in git
- clone the repo & install packages
- venv or miniconda(optional but strongly recommended, because I haven't cleaned up some unused dependencies)
```bash
git clone https://github.com/andri-jpg/AIwaifu-mini.git
cd ./AIwaifu-mini
```

```bash
# Install pytorch 
# Nvidia GPU only
# CUDA 11.7

conda install pytorch==1.13.0 torchvision==0.14.0 torchaudio==0.13.0 pytorch-cuda=11.7 -c pytorch -c nvidia

# CPU Only

conda install pytorch==1.13.0 torchvision==0.14.0 torchaudio==0.13.0 cpuonly -c pytorch

######################################
pip install -r ./requirements.txt

# You need to install the monotonic_align module for vits to work
cd monotonic_align
python setup.py build_ext --inplace
```

```bash
# Download model
python download_model.py
# Note : this will run multiple terminal
```
## Usage
- Run kobold.bat
- Wait for terminal show localhost:5001
- Run veadotube mini
- Load your own png or use default for testing
- Run main.py
```bash
# for default mode
python main.py
# for indonesian mode
python main_indonesia.py
```
- Wait for chrome windows run
- Click on load and select chat_config.json
- Minimize chrome
- Choose your virtual mic and output device index on terminal
- Press enter on terminal
- Now you can send your input from terminal.
- You can change your vits model in model folder, replace chihiro.pth and config.json
# Credit
[GPT-J_GGML](https://huggingface.co/Kastor/GPT-J-6B-Pygway-ggml-q4_1)
[vits-finetuning](https://github.com/SayaSS/vits-finetuning)
[Koboldcpp](https://github.com/LostRuins/koboldcpp)
[Helsinki-NLP](https://huggingface.co/Helsinki-NLP)
[staka/fugumt](https://huggingface.co/staka/fugumt-ja-en)
