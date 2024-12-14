# Utiliser une image de base ubuntu
FROM ubuntu:22.04

# Installation des dépendances de compilation
RUN apt-get update && apt-get install -y \
    build-essential \
    bison \
    cmake \
    libssl-dev \
    python3-dev \
    python3-pip \
    libpcre3-dev \
    pkg-config \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Téléchargement et compilation de MonetDB
WORKDIR /tmp
RUN git clone https://github.com/MonetDB/MonetDB.git && \
    cd MonetDB && \
    mkdir build && \
    cd build && \
    cmake .. \
        -DCMAKE_BUILD_TYPE=Release \
        -DWITH_PYTHON3=ON \
        -DCMAKE_INSTALL_PREFIX=/usr && \
    make -j$(nproc) && \
    make install && \
    cd / && \
    rm -rf /tmp/MonetDB*

# Installation du client Python
RUN pip3 install pymonetdb

# Création de l'utilisateur MonetDB et configuration
RUN useradd -r -m -d /var/monetdb5 monetdb && \
    mkdir -p /var/monetdb5/dbfarm && \
    chown -R monetdb:monetdb /var/monetdb5

# Configuration de MonetDB
RUN echo "[merovingian] \n\
forward=proxy \n\
passphrase=monetdb \n\
discovery=true \n\
control=true \n\
mapi=50000 \n\
exittimeout=5 \n\
[monetdb] \n\
user=monetdb \n\
password=monetdb" > /var/monetdb5/.merovingian.properties && \
    chown monetdb:monetdb /var/monetdb5/.merovingian.properties

WORKDIR /var/monetdb5

# Exposer le port
EXPOSE 50000

# Copier le script de démarrage
COPY docker/monetdb/scripts/start-monetdb.sh /start-monetdb.sh
RUN chmod +x /start-monetdb.sh

# Définir l'utilisateur MonetDB
USER monetdb

# Commande de démarrage
CMD ["/start-monetdb.sh"]