import torch
import pysbd
import spacy
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, MarianMTModel, pipeline
from downloader import ModelDownloader
class translator:
    """
    A class for translating text between English, Japanese, and Indonesian using Hugging Face Transformers.

    Args:
    indonesian (bool): Whether to include Indonesian translation capabilities. Default is False.

    Attributes:
    model_jp: A Hugging Face pipeline for English-to-Japanese translation.
    model_id: A Hugging Face MarianMTModel for Indonesian-to-English translation.
    tokenizer_id: A Hugging Face AutoTokenizer for Indonesian-to-English translation.
    model_en: A Hugging Face MarianMTModel for English-to-Indonesian translation.
    tokenizer_en: A Hugging Face AutoTokenizer for English-to-Indonesian translation.

    Methods:
    en_jp(inputs_en): Translates English text to Japanese.
    en_id(inputs_en): Translates English text to Indonesian.
    id_en(inputs_id): Translates Indonesian text to English.
    """
    def __init__(self, indonesian=False):
        self.model_download = ModelDownloader()
        use_gpu = torch.cuda.is_available()
        print("Detecting GPU...")
        if use_gpu:
            print("GPU detected!")
            print("loading translator")
            self.device = torch.device('cuda')
        else:
            print('Using CPU Only')
            self.device = torch.device('cpu')
        if not Path('fugumt-en-ja').is_dir():
            self.model_download.install_git_lfs()
            self.model_download.clone_repository("https://huggingface.co/staka/fugumt-en-ja")
            self.model_download.clone_repository("https://huggingface.co/finiteautomata/bertweet-base-emotion-analysis")
        self.model_jp = pipeline('translation', model='fugumt-en-ja')
        if indonesian:
            if not Path('opus-mt-id-en').is_dir():
                self.model_download.clone_repository("https://huggingface.co/Helsinki-NLP/opus-mt-id-en")
                self.model_download.clone_repository("https://huggingface.co/Helsinki-NLP/opus-mt-en-id")
            self.model_id = MarianMTModel.from_pretrained("opus-mt-id-en")
            self.tokenizer_id = AutoTokenizer.from_pretrained("opus-mt-id-en")
            self.model_id = self.model_id.to(self.device)
            self.model_en = MarianMTModel.from_pretrained("opus-mt-en-id")
            self.tokenizer_en = AutoTokenizer.from_pretrained("opus-mt-en-id")
            self.model_en = self.model_en.to(self.device)

        print("translator loaded")
    
    def en_jp(self, inputs_en):
        """
        Translates English text to Japanese using a Hugging Face pipeline.

        Args:
        inputs_en (str): The English text to be translated.

        Returns:
        A string containing the translated Japanese text.
        """
        if inputs_en is None:
            return None
        else:
            segmenter = pysbd.Segmenter(language="en", clean=True)
            pipeline_result = self.model_jp(segmenter.segment(inputs_en))
            result_text = ""
            for idx, item in enumerate(pipeline_result):
                if idx > 0:
                    result_text += ", "
                result_text += item['translation_text']
            return result_text

    def en_id(self, inputs_en):
        """
        Translates English text to Indonesian using a Hugging Face MarianMTModel.

        Args:
        inputs_en (str): The English text to be translated.

        Returns:
        A string containing the translated Indonesian text.
        """
        if inputs_en is None:
            return None
        else :
            inputs = self.tokenizer_en([inputs_en], return_tensors="pt")
            inputs = inputs.to(self.device)
            generated_ids = self.model_en.generate(**inputs)
            result = self.tokenizer_en.batch_decode(generated_ids, skip_special_tokens=True)[0]
            return result

    def id_en(self, inputs_id):
        """
        Translates Indonesian text to English using a Hugging Face MarianMTModel.

        Args:
        inputs_en (str): The Indonesian text to be translated.

        Returns:
        A string containing the translated English text.
        """
        if inputs_id is None:
            return None
        else :
            inputs = self.tokenizer_id([inputs_id], return_tensors="pt")
            inputs = inputs.to(self.device)
            generated_ids = self.model_id.generate(**inputs)
            result = self.tokenizer_id.batch_decode(generated_ids, skip_special_tokens=True)[0]
            return result
