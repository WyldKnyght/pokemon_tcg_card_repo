-- Tables
-- This table structure mirrors the https://docs.pokemontcg.io/ API's card set representation

-- The 'cards' table represents individual Pokemon cards https://docs.pokemontcg.io/api-reference/cards/card-object.
CREATE TABLE cards (
    id TEXT PRIMARY KEY NOT NULL,
    name TEXT,
    supertype TEXT,
    hp TEXT,
    evolvesFrom TEXT,
    artist TEXT,
    rarity TEXT,
    flavorText TEXT,
    number TEXT,
    set_id TEXT,
    created_at TEXT DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (set_id) REFERENCES card_sets(id)
);

-- The 'card_sets' table represents sets of Pokemon cards https://docs.pokemontcg.io/api-reference/sets/set-object.
CREATE TABLE card_sets (
    id TEXT PRIMARY KEY NOT NULL,
    name TEXT,
    series TEXT,
    printedTotal INTEGER,
    total INTEGER,
    ptcgoCode TEXT,
    releaseDate TEXT,
    updatedAt TEXT,
    created_at TEXT DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE card_subtypes (
    card_id TEXT,
    subtype TEXT,
    PRIMARY KEY (card_id, subtype),
    FOREIGN KEY (card_id) REFERENCES cards(id)
);

CREATE TABLE card_types (
    card_id TEXT,
    type TEXT,
    PRIMARY KEY (card_id, type),
    FOREIGN KEY (card_id) REFERENCES cards(id)
);

CREATE TABLE card_evolves_to (
    card_id TEXT,
    evolvesTo TEXT,
    PRIMARY KEY (card_id, evolvesTo),
    FOREIGN KEY (card_id) REFERENCES cards(id)
);

CREATE TABLE card_rules (
    card_id TEXT,
    rule TEXT,
    PRIMARY KEY (card_id, rule),
    FOREIGN KEY (card_id) REFERENCES cards(id)
);

CREATE TABLE card_ancient_traits (
        card_id TEXT,
        name TEXT,
        text TEXT,
        FOREIGN KEY (card_id) REFERENCES cards(id)
    );

CREATE TABLE card_abilities (
        card_id TEXT,
        name TEXT,
        text TEXT,
        type TEXT,
        FOREIGN KEY (card_id) REFERENCES cards(id)
    );

CREATE TABLE card_attacks (
        card_id TEXT,
        name TEXT,
        cost TEXT,
        convertedEnergyCost INTEGER,
        damage TEXT,
        text TEXT,
        FOREIGN KEY (card_id) REFERENCES cards(id)
    );

CREATE TABLE card_weaknesses (
    card_id TEXT,
    type TEXT,
    value TEXT,
    PRIMARY KEY (card_id, type),
    FOREIGN KEY (card_id) REFERENCES cards(id)
);

CREATE TABLE card_resistances (
    card_id TEXT,
    type TEXT,
    value TEXT,
    PRIMARY KEY (card_id, type),
    FOREIGN KEY (card_id) REFERENCES cards(id)
);

CREATE TABLE card_retreat_cost (
    card_id TEXT,
    cost TEXT,
    PRIMARY KEY (card_id, cost),
    FOREIGN KEY (card_id) REFERENCES cards(id)
);

CREATE TABLE card_national_pokedex_numbers (
    card_id TEXT,
    number INTEGER,
    PRIMARY KEY (card_id, number),
    FOREIGN KEY (card_id) REFERENCES cards(id)
);

CREATE TABLE card_legalities (
        card_id TEXT,
        standard TEXT,
        expanded TEXT,
        unlimited TEXT,
        FOREIGN KEY (card_id) REFERENCES cards(id)
    );

CREATE TABLE card_images (
        card_id TEXT,
        small TEXT,
        large TEXT,
        FOREIGN KEY (card_id) REFERENCES cards(id)
    );

CREATE TABLE card_tcgplayer (
    card_id TEXT,
    url TEXT,
    updatedAt TEXT,
    prices JSON,
    FOREIGN KEY (card_id) REFERENCES cards(id)
);

CREATE TABLE card_cardmarket (
    card_id TEXT,
    url TEXT,
    updatedAt TEXT,
    prices JSON,
    FOREIGN KEY (card_id) REFERENCES cards(id)
);

CREATE TABLE set_legalities (
        set_id TEXT,
        standard TEXT,
        expanded TEXT,
        unlimited TEXT,
        FOREIGN KEY (set_id) REFERENCES card_sets(id)
    );

CREATE TABLE set_images (
        set_id TEXT,
        symbol TEXT,
        logo TEXT,
        FOREIGN KEY (set_id) REFERENCES card_sets(id)
    );

-- Indexes
CREATE INDEX idx_cards_name ON cards(name);
CREATE INDEX idx_cards_set_id ON cards(set_id);
CREATE INDEX idx_card_sets_name ON card_sets(name);
CREATE INDEX idx_card_types_type ON card_types(type);
CREATE INDEX idx_card_sets_series ON card_sets(series);

-- Views

