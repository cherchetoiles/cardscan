CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    id_card_number TEXT UNIQUE
);

INSERT INTO users (first_name, last_name, id_card_number)
VALUES ('John', 'Doe', '123456789');
