DROP TABLE IF EXISTS currency_names;
CREATE TABLE currency_names (
	currency_name varchar(60),
	currency_code varchar(3),
	UNIQUE(currency_name, currency_code)
);