"""
Requêtes SQL optimisées par type d'opération pour l'analyse d'un petit dataset sur le thème de la qualité de l'air.
"""

AIR_QUALITY_QUERIES = [
    # 1. Sélection simple
    """
    SELECT DISTINCT Name, Measure, Geo_Place_Name, Data_Value
    FROM air_quality
    WHERE Data_Value > (
        SELECT AVG(Data_Value) FROM air_quality
    )
    AND Measure_Info = 'number'
    ORDER BY Data_Value DESC
    LIMIT 1000
    """,

    # 2. Agrégation
    """
    SELECT 
        Geo_Place_Name,
        COUNT(*) as total_measures,
        AVG(Data_Value) as avg_value,
        MIN(Data_Value) as min_value,
        MAX(Data_Value) as max_value
    FROM air_quality
    GROUP BY Geo_Place_Name
    HAVING COUNT(*) > 5
    ORDER BY avg_value DESC
    """,

    # 3. Jointure
    """
    WITH location_stats AS (
        SELECT Geo_Place_Name, AVG(Data_Value) as location_avg
        FROM air_quality
        GROUP BY Geo_Place_Name
    )
    SELECT 
        aq.Geo_Place_Name,
        aq.Name,
        aq.Data_Value,
        ls.location_avg
    FROM air_quality aq
    JOIN location_stats ls ON aq.Geo_Place_Name = ls.Geo_Place_Name
    WHERE aq.Data_Value > ls.location_avg
    """,
]