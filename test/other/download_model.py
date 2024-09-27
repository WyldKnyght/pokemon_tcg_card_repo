"""
src/download_model.py
Models are downloaded sequentially, one after another. 

This module contains two functions: download_model and download_models_sequentially. The 
download_model function takes a model name and a folder path as arguments, and downloads the 
model and tokenizer from Hugging Face to the specified folder. The download_models_sequentially 
function downloads a list of models sequentially, one after another.

The download_models_sequentially function can be run as a script, and it will download all the 
models in the list to the specified folder.

"""
import os
from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer


def download_model(model_name: str, model_folder: str) -> None:
    """
    Downloads a model and tokenizer from Hugging Face and saves them to the specified folder.

    Args:
        model_name (str): The name of the model to download.
        model_folder (str): The folder where the model should be saved.
    """
    save_directory = os.path.join(model_folder, model_name.split('/')[-1])
    os.makedirs(save_directory, exist_ok=True)
    print(f"Downloading {model_name} model...")

    _download_and_save_tokenizer_or_model(
        AutoTokenizer,
        model_name,
        save_directory,
        "Tokenizer downloaded and saved.",
    )
    _download_and_save_tokenizer_or_model(
        AutoModelForCausalLM,
        model_name,
        save_directory,
        "Model downloaded and saved.",
    )


def _download_and_save_tokenizer_or_model(
    model_class,
    model_name: str,
    save_directory: str,
    success_message: str,
) -> None:
    """
    Downloads a tokenizer or model from Hugging Face and saves it to the specified folder.

    Args:
        model_class: The class of the model to download.
        model_name (str): The name of the model to download.
        save_directory (str): The folder where the model should be saved.
        success_message (str): The message to print when the model is successfully downloaded.
    """
    model = model_class.from_pretrained(model_name)
    model.save_pretrained(save_directory)
    print(success_message)


def download_models_sequentially() -> None:
    """
    Downloads a list of models sequentially, one after another.

    The list of models is specified in the MODEL_NAMES environment variable.
    """
    load_dotenv()
    model_folder = os.getenv("MODEL_FOLDER")

    # List of models to download
    model_names = [
        "TheBloke/CodeLlama-7B-Python-GGUF",
        "TheBloke/WizardCoder-Python-7B-V1.0-GGUF",
        "TheBloke/CodeLlama-13B-Python-GGUF",
        "TheBloke/WizardCoder-Python-13B-V1.0-GGUF",
        "mistralai/Mamba-Codestral-7B-v0.1",
        "mistralai/Mistral-7B-v0.3",
        "mistralai/Mixtral-8x7B-v0.1",
        "microsoft/Phi-3.5-mini-instruct",
        "microsoft/Phi-3.5-MoE-instruct",
        "microsoft/Phi-3.5-vision-instruct",
    ]

    for model_name in model_names:
        download_model(model_name, model_folder)
        print(f"Finished downloading {model_name}")
        print("---")

if __name__ == "__main__":
    download_models_sequentially()
    print("All models downloaded successfully.")
