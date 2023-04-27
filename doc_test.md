# Translator Class Documentation

This is a class to perform translations from English to Japanese and from English to Indonesian. It uses PyTorch and Hugging Face Transformers.

## Dependencies
- PyTorch
- Pysbd
- Hugging Face Transformers

## Usage
```
from translator import translator

t = translator()

# Translation from English to Japanese
result = t.en_jp("How are you?")
print(result)  # お元気ですか？

# Translation from English to Indonesian
result = t.en_id("How are you?")
print(result)  # Apa kabar?
```

## Class Methods
### __init__(self, indonesian=False)
- Description: Constructor method for the Translator class
- Input:
    - indonesian (bool): If True, initializes Indonesian-to-English translation models and tokenizers. If False (default), initializes only English-to-Japanese translation models and tokenizers.
    
### en_jp(self, inputs_en)
- Description: Translates English input to Japanese
- Input:
    - inputs_en (str): English input sentence
- Output:
    - result_text (str): Japanese translation of the input sentence
    
### en_id(self, inputs_en)
- Description: Translates English input to Indonesian
- Input:
    - inputs_en (str): English input sentence
- Output:
    - result_text (str): Indonesian translation of the input sentence
    
### id_en(self, inputs_id)
- Description: Translates Indonesian input to English
- Input:
    - inputs_id (str): Indonesian input sentence
- Output:
    - result_text (str): English translation of the input sentence