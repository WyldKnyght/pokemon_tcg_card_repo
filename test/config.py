# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: m:\dev_env\PokeTradeVault\pokemon_tcg_card_repo\config.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 2024-08-07 16:55:48 UTC (1723049748)

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'pokemon_tcg.db')
CARDS_DATA_DIR = os.path.join(BASE_DIR, 'pokemon-tcg-data', 'cards', 'en')
SETS_DATA_PATH = os.path.join(BASE_DIR, 'pokemon-tcg-data', 'sets', 'en.json')
