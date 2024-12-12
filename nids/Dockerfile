# Utiliser une image de base Python
FROM python:3.9-slim

# Mettre à jour le système et installer les dépendances nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    libpcap-dev \
    python3-dev \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Créer un répertoire de travail
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY . /app

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer les ports nécessaires (si vous avez un port spécifique en tête, remplacez `1234` par celui-ci)
EXPOSE 80 3000 8080

# Définir la commande par défaut pour exécuter le script
CMD ["./start_nids.sh"]