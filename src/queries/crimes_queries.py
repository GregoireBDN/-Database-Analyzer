"""
Requêtes SQL optimisées par type d'opération pour l'analyse d'un grand dataset sur le thème des crimes.
"""

CRIMES_QUERIES = [
    # 1. Sélection simple
    """
    SELECT DISTINCT area_name, crm_cd_desc, vict_age, vict_sex
    FROM crimes 
    WHERE vict_age > 18 
    AND time_occ BETWEEN 2000 AND 2359
    LIMIT 1000
    """,

    # 2. Agrégation
    """
    SELECT 
        area_name,
        COUNT(*) as total_crimes,
        AVG(CAST(vict_age AS FLOAT)) as avg_victim_age,
        COUNT(DISTINCT crm_cd_desc) as crime_types
    FROM crimes
    GROUP BY area_name
    HAVING COUNT(*) > 100
    ORDER BY total_crimes DESC
    """,

    # 3. Jointure
    """
    WITH crime_stats AS (
        SELECT area_name, COUNT(*) as area_count
        FROM crimes
        GROUP BY area_name
    )
    SELECT 
        c.area_name,
        c.crm_cd_desc,
        cs.area_count,
        COUNT(*) as specific_crime_count
    FROM crimes c
    JOIN crime_stats cs ON c.area_name = cs.area_name
    GROUP BY c.area_name, c.crm_cd_desc, cs.area_count
    HAVING COUNT(*) > 50
    """,
]

"""
Description détaillée des requêtes:

1. Comptage total des crimes
   - Objectif: Obtenir le nombre total d'incidents
   - Utilisation: Vue d'ensemble rapide du volume de données

2. Analyse par zone
   - Objectif: Identifier les zones les plus touchées par la criminalité
   - Résultat: Distribution géographique des crimes
   - Tri: Par nombre décroissant d'incidents

3. Types de crimes
   - Objectif: Analyser la distribution des types de crimes
   - Filtres: Uniquement les types avec plus de 100 occurrences
   - Métriques: 
     * Nombre total d'incidents par type
     * Nombre de zones affectées

Notes d'utilisation:
-------------------
- Les requêtes sont optimisées pour PostgreSQL et MonetDB
- L'ordre des requêtes correspond à la configuration dans config.py
- Les résultats sont utilisés pour générer des graphiques comparatifs
""" 