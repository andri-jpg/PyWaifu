import os
import json
import math
import torch
import commons
import utils
from downloader import ModelDownloader
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence
from scipy.io.wavfile import write
from pathlib import Path

class tts_infer:
    def __init__(self, model_name='herta'):
        """
        Initialize the VITS inference model.
        
        Args:
        - model_name (str): The name of the VITS model to load.
        """
        print("loading tts")
        self.model_name = model_name
        self.config_path = "model/config.json"
        self.model_path = f"model/{model_name}.pth"
        self.model_download = ModelDownloader()
    
        os.makedirs("model", exist_ok=True)

        if not Path(self.config_path).is_file():
            raise FileNotFoundError(f'{self.config_path} not found')

        if not Path(self.model_path).is_file():
            self.model_download.ask_download(f"https://huggingface.co/spaces/zomehwh/vits-models/resolve/main/pretrained_models/herta/herta.pth", self.model_path)
            
        self.hps = utils.get_hparams_from_file(self.config_path)
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
            self.net_g = SynthesizerTrn(
                len(self.hps.symbols),
                self.hps.data.filter_length // 2 + 1,
                self.hps.train.segment_size // self.hps.data.hop_length,
                n_speakers=self.hps.data.n_speakers,
                **self.hps.model).to(self.device)
        else:
            self.device = torch.device("cpu")
            self.net_g = SynthesizerTrn(
                len(self.hps.symbols),
                self.hps.data.filter_length // 2 + 1,
                self.hps.train.segment_size // self.hps.data.hop_length,
                n_speakers=self.hps.data.n_speakers,
                **self.hps.model).to(self.device)

        self.model = utils.load_checkpoint(self.model_path, self.net_g, None)

        print("tts loaded")
    
    def get_text(self, text, hps):
        """
        Convert the input text into a sequence of integers (symbols) using the text-to-sequence function.
        
        Args:
        - text (str): The input text to convert.
        - hps (object): The hyperparameters object.
        
        Returns:
        - A tensor containing the integer sequence of the input text.
        """
        text_norm = text_to_sequence(text, hps.data.text_cleaners)
        if hps.data.add_blank:
            text_norm = commons.intersperse(text_norm, 0)
        text_norm = torch.LongTensor(text_norm)
        return text_norm
    
    def convert(self, text):
        """
        Convert the input text into speech by running the VITS inference model.
        
        Args:
        - text (str): The input text to convert.
        """
        if text is None:
            pass
        else:
            speaker_id = 0
            text = text
            noise_scale = 0.6
            noise_scale_w = 0.668
            length_scale = 1.0
            stn_tst = self.get_text(text, self.hps)
            with torch.no_grad():
                x_tst = stn_tst.to(self.device).unsqueeze(0)
                x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).to(self.device)
                sid = torch.LongTensor([speaker_id]).to(self.device)
                audio = self.net_g.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=noise_scale, noise_scale_w=noise_scale_w, length_scale=length_scale)[0][0, 0].data.cpu().float().numpy()
            write('dialog.wav', self.hps.data.sampling_rate, audio)