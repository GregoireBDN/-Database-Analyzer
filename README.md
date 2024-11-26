# 📊 Database Analyzer

Ce projet utilise PostgreSQL et MonetDB pour l'analyse de données.

## 📋 Table des matières

- [Prérequis](#prérequis)
- [Configuration](#configuration)
- [Installation](#installation)
- [Vérification](#vérification)
- [Dépannage](#dépannage)

## 🔧 Prérequis

<details>
<summary><b>macOS</b></summary>

```bash
# Installation avec Homebrew
brew install postgresql@15
brew install monetdb
```

</details>

<details>
<summary><b>Linux (Ubuntu/Debian)</b></summary>

```bash
# Installation de PostgreSQL
sudo apt update
sudo apt install postgresql-15

# Installation de MonetDB
sudo apt install monetdb5-server monetdb5-client
```

</details>

<details>
<summary><b>Linux (RHEL/CentOS)</b></summary>

```bash
# Installation de PostgreSQL
sudo dnf install postgresql-server
sudo postgresql-setup --initdb

# Installation de MonetDB
# Suivre les instructions sur https://www.monetdb.org/downloads/
```

</details>

## ⚙️ Configuration

1. **Clonage du repository**

   ```bash
   git clone [URL_DU_REPO]
   cd DataBaseAnalyzer
   ```

2. **Configuration de l'environnement**

   ```bash
   cp .env.example .env
   ```

3. **Paramètres de configuration** (.env)

   ```env
   # PostgreSQL Configuration
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=databaseannalizationproject
   POSTGRES_HOST=127.0.0.1
   POSTGRES_PORT=5432

   # MonetDB Configuration
   MONETDB_USER=monetdb
   MONETDB_PASSWORD=monetdb
   MONETDB_DB=databaseannalizationproject
   MONETDB_HOST=127.0.0.1
   MONETDB_PORT=50000

   # Application Configuration
   BATCH_SIZE=1000
   DATA_DIR=./data
   ```

## 🚀 Installation

1. **Préparation du script**

   ```bash
   chmod +x setup_databases.sh
   ```

2. **Exécution de l'installation**
   ```bash
   ./setup_databases.sh
   ```

> 📝 **Le script effectue automatiquement :**
>
> - Vérification et démarrage de PostgreSQL
> - Configuration et démarrage de MonetDB
> - Création des bases de données
> - Configuration des utilisateurs
> - Tests de connexion

## ✅ Vérification

### PostgreSQL

```bash
psql -U postgres -d databaseannalizationproject
```

### MonetDB

```bash
mclient -h 127.0.0.1 -p 50000 -u monetdb -d databaseannalizationproject
```

## 🔍 Dépannage

En cas de problèmes, vérifiez les points suivants :

| Problème              | Solution                                              |
| --------------------- | ----------------------------------------------------- |
| Services non démarrés | Vérifiez le statut des services PostgreSQL et MonetDB |
| Erreurs MonetDB       | Consultez `./data/monetdb/merovingian.log`            |
| Ports occupés         | Vérifiez si les ports 5432 et 50000 sont disponibles  |
| Permissions           | Assurez-vous que `./data` a les bonnes permissions    |

## 📫 Support

Si vous rencontrez des problèmes :

1. Consultez la section dépannage ci-dessus
2. Vérifiez les logs des services
3. Ouvrez une issue sur GitHub

---

_Développé avec ❤️ pour l'analyse de données_
