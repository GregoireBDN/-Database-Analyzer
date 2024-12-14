FROM postgres:15

# Variables d'environnement par défaut
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=testdb

# Installation d'extensions courantes
RUN apt-get update && apt-get install -y \
    postgresql-contrib \
    postgresql-15-postgis-3 \
    postgresql-15-postgis-3-scripts \
    && rm -rf /var/lib/apt/lists/*

# Exposer le port PostgreSQL
EXPOSE 5432

# Le volume pour la persistance des données
VOLUME /var/lib/postgresql/data 