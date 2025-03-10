import logging
from dotenv import load_dotenv
from pathlib import Path


def init_environment():
    """
    Loads environment variables from .env and optionally from .env.local.
    - .env is always loaded (if it exists).
    - .env.local overrides .env values if present.
    """
    dotenv_path = Path(".env")

    if dotenv_path.exists():
        load_dotenv(dotenv_path=dotenv_path, override=False)
        logging.info("Loaded environment variables from .env")

    # Load .env.local if available (overrides .env)
    dotenv_local_path = Path(".env.local")
    if dotenv_local_path.exists():
        load_dotenv(dotenv_path=dotenv_local_path, override=True)
        logging.info("Loaded environment variables from .env.local (overriding .env values)")
