DROP TABLE IF EXISTS currency_names;
CREATE TABLE currency_names (
	currency_code VARCHAR(3) PRIMARY KEY NOT NULL UNIQUE,
	currency_name VARCHAR(60) NOT NULL UNIQUE
);
DROP TABLE IF EXISTS exchange_rates;
CREATE TABLE exchange_rates (
	currency_code VARCHAR(3) PRIMARY KEY NOT NULL UNIQUE,
	rate REAL NOT NULL
);