AIR_QUALITY_QUERIES = [
    # Requête simple de comptage
    "SELECT COUNT(*) FROM air_quality",
    
    # Requête avec GROUP BY et agrégation
    """
    SELECT Geo_Place_Name, COUNT(*), AVG(Data_Value)
    FROM air_quality
    GROUP BY Geo_Place_Name
    HAVING COUNT(*) > 10
    """,
    
    # Requête avec sous-requête et fonction de fenêtrage
    """
    SELECT Name, Data_Value, Geo_Place_Name,
        AVG(Data_Value) OVER (PARTITION BY Geo_Place_Name) as avg_by_place
    FROM air_quality
    WHERE Data_Value > (SELECT AVG(Data_Value) FROM air_quality)
    """,
    
    # Requête avec jointure simple
    """
    SELECT a1.Geo_Place_Name, 
           a1.Data_Value as current_value,
           a2.Data_Value as other_value,
           a1.Start_Date
    FROM air_quality a1
    LEFT JOIN air_quality a2 
        ON a1.Geo_Place_Name = a2.Geo_Place_Name
        AND a1.Name = a2.Name
        AND a1.Data_Value <> a2.Data_Value
    WHERE a1.Data_Value > 10
    ORDER BY a1.Data_Value DESC
    LIMIT 100
    """,
    
    # Requête avec agrégation par région
    """
    SELECT 
        Geo_Place_Name,
        COUNT(*) as total_measures,
        MIN(Data_Value) as min_value,
        MAX(Data_Value) as max_value,
        AVG(Data_Value) as avg_value
    FROM air_quality
    GROUP BY Geo_Place_Name
    ORDER BY avg_value DESC
    """
] 