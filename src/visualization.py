import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_performance_graph(results, config):
    """
    Crée un graphique de comparaison des performances incluant les temps de chargement
    """
    plt.figure(figsize=(15, 8))
    
    # Nombre total de barres (requêtes + chargement)
    total_bars = len(results) + 1 if 'loading_times' in config else len(results)
    x = range(total_bars)
    width = 0.35
    
    # Préparer les données pour les barres
    pg_times = []
    monet_times = []
    labels = []
    
    # Ajouter les temps de chargement si disponibles
    if 'loading_times' in config:
        pg_times.append(config['loading_times']['postgres'])
        monet_times.append(config['loading_times']['monetdb'])
        labels.append('Chargement')
    
    # Ajouter les temps d'exécution des requêtes
    pg_times.extend([r['pg_execution_time']['mean'] for r in results])
    monet_times.extend([r['monet_execution_time']['mean'] for r in results])
    labels.extend(config['query_names'])
    
    # Créer les barres
    plt.bar([i - width/2 for i in x], 
            pg_times,
            width, 
            label='PostgreSQL', 
            color='#336791')
    plt.bar([i + width/2 for i in x], 
            monet_times,
            width, 
            label='MonetDB', 
            color='#FF6B6B')
    
    plt.ylabel('Temps d\'exécution (ms)')
    plt.title(config['title'])
    plt.xticks(x, labels, rotation=45, ha='right')
    plt.legend()
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Sauvegarde du graphique
    os.makedirs('results', exist_ok=True)
    plt.savefig(config['output_path'])
    print(f"\n📊 Graphique sauvegardé dans '{config['output_path']}'")
    
    plt.show()
    plt.close()