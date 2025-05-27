import fasttext
import os


class LanguageDetection:
    """
    A class to handle language detection using a pre-trained FastText model.
    Implements a singleton pattern to ensure the model is loaded only once.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LanguageDetection, cls).__new__(cls, *args, **kwargs)
            cls._instance.model = fasttext.load_model("lid.176.bin")
        return cls._instance

    def detect_language(self, text: str) -> str:
        """
        Detect the language of the given text using the pre-trained FastText model.

        Args:
            text (str): The input text to detect the language for.

        Returns:
            str: Detected language label (e.g., 'en', 'pl', etc.).
        """
        labels, _ = self.model.predict(text)
        label = labels[0].replace("__label__", "")
        return label


def get_model() -> LanguageDetection:
    """
    Get the singleton instance of LanguageDetection.

    Returns:
        LanguageDetection: The shared instance.
    """
    return LanguageDetection()


def is_polish(label: str) -> bool:
    """
    Check if the detected language is Polish.

    Args:
        label (str): The detected language label.

    Returns:
        bool: True if the detected language is Polish, False otherwise.
    """
    return label == "en"