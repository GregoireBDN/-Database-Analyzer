CRIMES_QUERIES = [
    # Requête simple de comptage
    "SELECT COUNT(*) FROM crimes",
    
    # Analyse des crimes par zone
    """
    SELECT area_name, COUNT(*) as crime_count
    FROM crimes
    GROUP BY area_name
    ORDER BY crime_count DESC
    """,
    
    # Statistiques par type de crime
    """
    SELECT crm_cd_desc, COUNT(*) as count,
           COUNT(DISTINCT area) as areas_affected
    FROM crimes
    GROUP BY crm_cd_desc
    HAVING COUNT(*) > 100
    ORDER BY count DESC
    """,
    
    # Analyse temporelle des crimes
    """
    SELECT FLOOR(time_occ / 100) as hour_of_day,
           COUNT(*) as crime_count
    FROM crimes
    GROUP BY hour_of_day
    ORDER BY hour_of_day
    """,
    
    # Analyse géographique complexe
    """
    SELECT c1.area,
           c1.crm_cd_desc,
           COUNT(*) as crime_count,
           AVG(CAST(c1.vict_age as float)) as avg_victim_age
    FROM crimes c1
    WHERE c1.vict_age != '0'
    GROUP BY c1.area, c1.crm_cd_desc
    HAVING COUNT(*) > 50
    ORDER BY crime_count DESC
    LIMIT 100
    """
] 