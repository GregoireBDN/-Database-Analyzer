"""
Module d'initialisation pour le package DataBaseAnalyzer.
Ce package fournit des outils pour l'analyse de bases de données.
"""

__version__ = "0.1.0"


__all__ = ['DatabaseConnector', 'DatabaseLoader', 'QueryAnalyzer']

from .base_classes import DatabaseConnector, DatabaseLoader, QueryAnalyzer


import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Vérification de l'environnement
import os
if not os.path.exists('.env'):
    logger.warning("Fichier .env non trouvé")