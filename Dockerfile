# Utilise une image Python légère
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && \
    apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances en premier pour optimiser le cache Docker
COPY requirements.txt ./

# Installer les dépendances avec pip
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code de l'application
COPY . .

# Définir le port exposé
EXPOSE 8000

# Par défaut, lancer l'API FastAPI
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5054"]