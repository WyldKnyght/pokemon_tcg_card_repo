# config.py
import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'pokemon_tcg.db')

# Data directories
CARDS_DATA_DIR = os.path.join(BASE_DIR, 'data','pokemon-tcg-data', 'cards', 'en')
SETS_DATA_PATH = os.path.join(BASE_DIR, 'data', 'pokemon-tcg-data', 'sets', 'en.json')