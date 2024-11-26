from setuptools import setup, find_packages
import src

# Lire les dépendances depuis requirements.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="databaseanalyzer",
    version=src.__version__,  # Utilise la version définie dans __init__.py
    packages=find_packages(),
    description="Outils pour l'analyse de bases de données",
    long_description=src.__doc__,  # Utilise la docstring de __init__.py
    author="Gregoire Bodin",  # À modifier selon vos besoins
    author_email="gregoire.bodin04@gmail.com",  # À modifier selon vos besoins
    url="https://github.com/grbodin/databaseanalyzer",  # À modifier selon vos besoins
    install_requires=required,  # Utilise les dépendances de requirements.txt
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.10',
) 