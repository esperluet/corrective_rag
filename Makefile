# -----------------------------------------------------------------
# Makefile pour gérer le projet "corrective_rag"
# -----------------------------------------------------------------
# Commandes principales :
#   make help               : Affiche l'aide
#   make install            : Installe les dépendances via pip
#   make active-venv        : Activate virtual environment
#   make run-cli            : Lance l'application en CLI
#   make run-api            : Lance l'application FastAPI
#   make test               : Exécute la suite de tests
#   make docker-build       : Construit l'image Docker
#   make docker-run         : Lance un conteneur Docker (mode détaché)
#   make docker-stop        : Stoppe et supprime le conteneur Docker
#   make docker-sh          : Ouvre un shell dans un conteneur en cours d'exécution
#   make clean              : Nettoie les artefacts temporaires
#   make format             : Formate le code avec black
#   make lint               : Vérifie la qualité du code avec flake8
#
# -----------------------------------------------------------------

PROJECT_NAME    := corrective-rag
DOCKER_IMAGE    := $(PROJECT_NAME):latest
CONTAINER_NAME  := $(PROJECT_NAME)-container

## help : Affiche cette aide.
.PHONY: help
help:
	@echo "Commandes disponibles :"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	    | sort \
	    | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Exemple: make install"

## install : Installe les dépendances via pip.
.PHONY: install
install:
	@echo "==> Installation des dépendances (pip)..."
	pip install --no-cache-dir -r requirements.txt

## install : Installe les dépendances via pipenv.
.PHONY: install
create-venv:
	@echo "==> Creating virtual environment (pip)..."
	python -m venv venv

## install : Installe les dépendances via pip.
.PHONY: install
activate-venv:
	@echo "==> Installation des dépendances (pip)..."
	source ./venv/bin/active

## run-cli : Lance l'application en CLI.
.PHONY: run-cli
run-cli:
	@echo "==> Lancement de l'application CLI..."
	python cli.py

## run-api : Lance l'application FastAPI.
.PHONY: run-api
run-api:
	@echo "==> Lancement de l'API FastAPI..."
	pipenv run uvicorn api:app --host 0.0.0.0 --port 5054 --reload

## test : Exécute la suite de tests unitaires.
.PHONY: test
test:
	@echo "==> Exécution des tests..."
	pipenv run pytest --maxfail=1 --disable-warnings -q tests/

## docker-build : Construit l'image Docker.
.PHONY: docker-build
docker-build:
	@echo "==> Construction de l'image Docker : $(DOCKER_IMAGE)"
	docker build -t $(DOCKER_IMAGE) .

## docker-run : Lance le conteneur Docker en mode détaché.
.PHONY: docker-run
docker-run:
	@echo "==> Lancement du conteneur : $(CONTAINER_NAME)"
	docker run -d --name $(CONTAINER_NAME) -p 5054:5054 $(DOCKER_IMAGE)

## docker-stop : Stoppe et supprime le conteneur Docker.
.PHONY: docker-stop
docker-stop:
	@echo "==> Arrêt et suppression du conteneur : $(CONTAINER_NAME)"
	-docker stop $(CONTAINER_NAME)
	-docker rm $(CONTAINER_NAME)

## docker-sh : Ouvre un shell dans un conteneur en cours d'exécution.
.PHONY: docker-sh
docker-sh:
	@echo "==> Shell dans le conteneur Docker..."
	docker exec -it $(CONTAINER_NAME) /bin/bash

## clean : Nettoie les fichiers temporaires.
.PHONY: clean
clean:
	@echo "==> Nettoyage des fichiers temporaires..."
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

## format : Formate le code avec Black.
.PHONY: format
format:
	@echo "==> Formatage du code avec Black..."
	pipenv run black .

## lint : Vérifie la qualité du code avec Flake8.
.PHONY: lint
lint:
	@echo "==> Vérification de la qualité du code avec Flake8..."
	pipenv run flake8 .
