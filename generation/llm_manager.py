import logging
from langchain_ollama import ChatOllama
from app.config import OLLAMA_MODEL  # Environment variable defined in config.py


def get_llm(model: str = "", output_format: str = None) -> ChatOllama:
    """
    Returns an instance of the ChatOllama LLM.
    If no model is specified, it uses the default model from the environment variable.

    Args:
        model (str, optional): The name of the Ollama model to load. Defaults to the configured model.
        output_format (str, optional): The desired output format (e.g., "json").

    Returns:
        ChatOllama: An instance of the ChatOllama LLM.
    """
    if not model:
        if not OLLAMA_MODEL:
            logging.error("OLLAMA_MODEL is not set in the environment configuration.")
            raise ValueError("OLLAMA_MODEL must be defined in the environment configuration.")
        model = OLLAMA_MODEL

    try:
        return ChatOllama(model=model) if output_format is None else ChatOllama(model=model, format=output_format)
    except Exception as e:
        logging.error(f"Error initializing ChatOllama with model '{model}': {e}")
        raise
