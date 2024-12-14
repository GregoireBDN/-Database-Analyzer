"""
Module de visualisation des performances comparatives PostgreSQL vs MonetDB.

Ce module fournit des fonctionnalités pour créer des graphiques comparatifs
détaillés des performances entre PostgreSQL et MonetDB. Il génère deux types
de visualisations :
1. Temps de chargement moyen par ligne
2. Temps d'exécution moyen par type de requête

Les graphiques utilisent une palette de couleurs cohérente :
- PostgreSQL : #336699 (bleu)
- MonetDB : #CC3366 (rose)

Dépendances:
    - matplotlib: Pour la création des graphiques
    - logging: Pour la journalisation des événements

Notes:
    Les graphiques sont sauvegardés automatiquement dans le dossier 'results/'
    avec une résolution de 300 DPI pour une qualité optimale.
"""

import matplotlib.pyplot as plt
import logging

# Configuration du logger
logger = logging.getLogger(__name__)

def create_performance_graph(results_analyzer, config):
    """
    Crée un graphique comparatif des performances entre PostgreSQL et MonetDB.
    
    Cette fonction génère une figure avec deux sous-graphiques :
    1. Temps de chargement moyen par ligne (ms/ligne)
    2. Temps d'exécution moyen par type de requête (ms)
    
    Args:
        results_analyzer (list): Liste des résultats d'analyse contenant :
            - query_id: Identifiant de la requête
            - pg_execution_time: Métriques PostgreSQL
            - monet_execution_time: Métriques MonetDB
            
        config (dict): Configuration du graphique contenant :
            - title: Titre du graphique
            - output_file: Nom du fichier de sortie
            - loading_times: Temps de chargement {pg_load_time, monet_load_time}
            - total_rows: Nombre total de lignes
    
    Returns:
        None: Les graphiques sont sauvegardés dans le dossier 'results/'
    
    Notes:
        - Les types de requêtes sont affichés sous chaque barre
        - La rotation des étiquettes est de 45° pour une meilleure lisibilité
        - Les graphiques utilisent tight_layout pour optimiser l'espace
    """
    if not results_analyzer or not isinstance(results_analyzer, list):
        logger.warning("Aucun résultat d'analyse à visualiser")
        return
        
    # Créer une figure avec deux sous-graphiques
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Premier graphique : Temps de chargement par ligne (en ms/ligne)
    if ('loading_times' in config and 'total_rows' in config 
        and config['total_rows'] > 0):
        loading_per_row = [
            (config['loading_times']['pg_load_time']) / config['total_rows'],  # ms/ligne
            (config['loading_times']['monet_load_time']) / config['total_rows']
        ]
        ax1.bar(['PostgreSQL', 'MonetDB'], loading_per_row, 
                color=['#336699', '#CC3366'])
        ax1.set_title('Temps de Chargement Moyen par Ligne')
        ax1.set_ylabel('Temps (ms/ligne)')
    else:
        logger.warning("Données de chargement manquantes ou invalides")
        ax1.text(0.5, 0.5, 'Données de chargement non disponibles', 
                horizontalalignment='center', verticalalignment='center')
        ax1.set_title('Temps de Chargement Moyen par Ligne')

    # Deuxième graphique : Temps d'exécution moyen des requêtes
    query_ids = []
    pg_times = []
    monet_times = []
    
    for result in results_analyzer:
        if isinstance(result, dict) and 'query_id' in result:
            query_ids.append(f"Q{result['query_id']}")
            pg_times.append(result['pg_execution_time']['mean'])
            monet_times.append(result['monet_execution_time']['mean'])

    width = 0.35
    x = range(len(query_ids))
    
    ax2.bar([i - width/2 for i in x], pg_times, width, 
            label='PostgreSQL', color='#336699')
    ax2.bar([i + width/2 for i in x], monet_times, width, 
            label='MonetDB', color='#CC3366')
    
    # Définition des types de requêtes
    query_types = ['Sélection', 'Agrégation', 'Jointure']
    
    # Modification de l'affichage des étiquettes
    query_labels = [f"Q{i+1}\n({query_types[i]})" for i in range(len(query_ids))]
    ax2.set_xticklabels(query_labels, rotation=45)
    
    ax2.set_xlabel('Type de Requête')
    ax2.set_ylabel('Temps d\'exécution moyen (ms)')
    ax2.set_title(f'Temps d\'Exécution Moyen des Requêtes - {config["title"]}')
    ax2.set_xticks(x)
    ax2.legend()

    plt.tight_layout()
    output_path = f'results/{config["output_file"]}'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Graphique sauvegardé : {output_path}")