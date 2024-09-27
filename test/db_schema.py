# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: m:\dev_env\PokeTradeVault\pokemon_tcg_card_repo\db_schema.py
# Bytecode version: 3.12.0rc2 (3531)
# Source timestamp: 2024-08-07 20:29:32 UTC (1723062572)

import sqlite3
from config import DATABASE_PATH

def create_tables():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('\n    CREATE TABLE IF NOT EXISTS cards (\n        id TEXT PRIMARY KEY,\n        name TEXT,\n        supertype TEXT,\n        level TEXT,\n        hp TEXT,\n        evolvesFrom TEXT,\n        convertedRetreatCost INTEGER,\n        number TEXT,\n        artist TEXT,\n        rarity TEXT,\n        flavorText TEXT,\n        regulationMark TEXT,\n        set_id TEXT,\n        FOREIGN KEY (set_id) REFERENCES card_sets(id)\n    )\n    ')
    cursor.execute('\n    CREATE TABLE IF NOT EXISTS card_sets (\n        id TEXT PRIMARY KEY,\n        name TEXT,\n        series TEXT,\n        printedTotal INTEGER,\n        total INTEGER,\n        ptcgoCode TEXT,\n        releaseDate TEXT,\n        updatedAt TEXT\n    )\n    ')
    cursor.execute('\n    CREATE TABLE IF NOT EXISTS card_subtypes (\n        card_id TEXT,\n        subtype TEXT,\n        FOREIGN KEY (card_id) REFERENCES cards(id)\n    )\n    ')
    cursor.execute('\n    CREATE TABLE IF NOT EXISTS card_types (\n        card_id TEXT,\n        type TEXT,\n        FOREIGN KEY (card_id) REFERENCES cards(id)\n    )\n    ')
    cursor.execute('\n    CREATE TABLE IF NOT EXISTS card_evolves_to (\n        card_id TEXT,\n        evolvesTo TEXT,\n        FOREIGN KEY (card_id) REFERENCES cards(id)\n    )\n    ')
    cursor.execute('\n    CREATE TABLE IF NOT EXISTS card_rules (\n        card_id TEXT,\n        rule TEXT,\n        FOREIGN KEY (card_id) REFERENCES cards(id)\n    )\n    ')
    cursor.execute('\n    CREATE TABLE IF NOT EXISTS card_ancient_traits (\n        card_id TEXT,\n        name TEXT,\n        text TEXT,\n        FOREIGN KEY (card_id) REFERENCES cards(id)\n    )\n    ')
    cursor.execute('\n    CREATE TABLE IF NOT EXISTS card_abilities (\n        card_id TEXT,\n        name TEXT,\n        text TEXT,\n        type TEXT,\n        FOREIGN KEY (card_id) REFERENCES cards(id)\n    )\n    ')
    cursor.execute('\n    CREATE TABLE IF NOT EXISTS card_attacks (\n        card_id TEXT,\n        name TEXT,\n        cost TEXT,\n        convertedEnergyCost INTEGER,\n        damage TEXT,\n        text TEXT,\n        FOREIGN KEY (card_id) REFERENCES cards(id)\n    )\n    ')
    cursor.execute('\n    CREATE TABLE IF NOT EXISTS card_weaknesses (\n        card_id TEXT,\n        type TEXT,\n        value TEXT,\n        FOREIGN KEY (card_id) REFERENCES cards(id)\n    )\n    ')
    cursor.execute('\n    CREATE TABLE IF NOT EXISTS card_resistances (\n        card_id TEXT,\n        type TEXT,\n        value TEXT,\n        FOREIGN KEY (card_id) REFERENCES cards(id)\n    )\n    ')
    cursor.execute('\n    CREATE TABLE IF NOT EXISTS card_retreat_cost (\n        card_id TEXT,\n        cost TEXT,\n        FOREIGN KEY (card_id) REFERENCES cards(id)\n    )\n    ')
    cursor.execute('\n    CREATE TABLE IF NOT EXISTS card_national_pokedex_numbers (\n        card_id TEXT,\n        number INTEGER,\n        FOREIGN KEY (card_id) REFERENCES cards(id)\n    )\n    ')
    cursor.execute('\n    CREATE TABLE IF NOT EXISTS card_legalities (\n        card_id TEXT,\n        standard TEXT,\n        expanded TEXT,\n        unlimited TEXT,\n        FOREIGN KEY (card_id) REFERENCES cards(id)\n    )\n    ')
    cursor.execute('\n    CREATE TABLE IF NOT EXISTS card_images (\n        card_id TEXT,\n        small TEXT,\n        large TEXT,\n        FOREIGN KEY (card_id) REFERENCES cards(id)\n    )\n    ')
    cursor.execute('\n    CREATE TABLE IF NOT EXISTS card_tcgplayer (\n        card_id TEXT,\n        url TEXT,\n        updatedAt TEXT,\n        prices TEXT,\n        FOREIGN KEY (card_id) REFERENCES cards(id)\n    )\n    ')
    cursor.execute('\n    CREATE TABLE IF NOT EXISTS card_cardmarket (\n        card_id TEXT,\n        url TEXT,\n        updatedAt TEXT,\n        prices TEXT,\n        FOREIGN KEY (card_id) REFERENCES cards(id)\n    )\n    ')
    cursor.execute('\n    CREATE TABLE IF NOT EXISTS set_legalities (\n        set_id TEXT,\n        standard TEXT,\n        expanded TEXT,\n        unlimited TEXT,\n        FOREIGN KEY (set_id) REFERENCES card_sets(id)\n    )\n    ')
    cursor.execute('\n    CREATE TABLE IF NOT EXISTS set_images (\n        set_id TEXT,\n        symbol TEXT,\n        logo TEXT,\n        FOREIGN KEY (set_id) REFERENCES card_sets(id)\n    )\n    ')
    conn.commit()
    conn.close()
if __name__ == '__main__':
    create_tables()
