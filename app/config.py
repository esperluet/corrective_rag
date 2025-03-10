import os
from app.environment import init_environment

init_environment()  # Charge les variables d'env

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-r1")
# Ajoute d'autres variables si besoin
