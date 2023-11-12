use mysql;
CREATE TABLE IF NOT EXISTS users(
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(254) UNIQUE,
    password TEXT,
    activated BOOLEAN
);

CREATE TABLE IF NOT EXISTS activation_codes(
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    code INT(4),
    expiration DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
