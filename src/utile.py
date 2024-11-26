def formater_nombre(nombre: int) -> str:
    """
    Formate un nombre en ajoutant des espaces entre les milliers
    Ex: 1234567 -> 1 234 567
    """
    return f"{nombre:,}".replace(',', ' ')