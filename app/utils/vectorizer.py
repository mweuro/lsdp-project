from sentence_transformers import SentenceTransformer


class TextVectorizer:
    """
    A class to handle text vectorization using a pre-trained SentenceTransformer model.
    Implements a singleton pattern to ensure the model is loaded only once.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TextVectorizer, cls).__new__(cls, *args, **kwargs)
            cls._instance.model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        return cls._instance

    def vectorize(self, text: str) -> list:
        """
        Vectorize the input text using the pre-trained model.

        Args:
            text (str): The input text to be vectorized.

        Returns:
            list: The vectorized representation of the input text.
        """
        return self.model.encode(text).tolist()

def get_model() -> TextVectorizer:
    """
    Get the singleton instance of LanguageDetection.

    Returns:
        LanguageDetection: The shared instance.
    """
    return TextVectorizer()
