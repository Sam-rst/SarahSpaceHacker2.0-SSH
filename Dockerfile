# Image Python officielle légère
FROM python:3.13-slim

# Installer uv (gestionnaire moderne ultra-rapide)
RUN pip install --no-cache-dir uv

# Crée un répertoire de travail
WORKDIR /app

# Copie uniquement les fichiers nécessaires pour l’installation
COPY pyproject.toml uv.lock* ./

# Installe les dépendances du projet avec uv
RUN uv pip install -e .

# Copie le reste du code source
COPY . .

# Expose le port utilisé par ton serveur TCP
EXPOSE 50006

# Démarre ton serveur via uv
CMD ["uv", "run", "server.py", "--host", "0.0.0.0", "--port", "50006"]
