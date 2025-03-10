# Utilise une image Python légère
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances nécessaires pour le projet
RUN apt-get update && \
    apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copier Pipfile et Pipfile.lock en premier pour mieux gérer le cache Docker
COPY Pipfile Pipfile.lock ./

# Installer les dépendances avec pipenv
RUN pip install pipenv && pipenv install --system --deploy

# Copier tout le code restant
COPY . .

# Définir le port exposé
EXPOSE 8000

# Par défaut, lancer l'API (modifiable au démarrage)
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5054"]
