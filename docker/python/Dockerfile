FROM python:3.9

WORKDIR /app

# 1. Installe d'abord les dépendances
COPY docker/python/requirements.txt .
RUN pip install -r requirements.txt

# 2. Copie et installe le code source
COPY src/ src/
COPY setup.py .
RUN pip install -e .

# Créer le dossier results
RUN mkdir -p results

CMD ["python", "src/main.py"]