USE gans;
TRUNCATE table weathers;
TRUNCATE table flights;
-- insert here your DB name
-- uncomment to reset database
-- DROP TABLE populations;
-- DROP TABLE cities_location;
-- DROP TABLE weathers;
-- DROP TABLE cities_airports;
-- DROP TABLE cities;
-- DROP TABLE airports_location;
-- DROP TABLE flights;
-- DROP TABLE airports;
-- create cities table
CREATE TABLE IF NOT EXISTS cities (
    city_id INT AUTO_INCREMENT,
    city_name VARCHAR(200),
    country VARCHAR(200),
    country_code VARCHAR(3),
    PRIMARY KEY(city_id)
);
-- create population table
CREATE TABLE IF NOT EXISTS populations (
    city_id INT,
    population INT,
    measurement_year YEAR,
    PRIMARY KEY(city_id, measurement_year),
    FOREIGN KEY(city_id) REFERENCES cities(city_id)
);
-- create city location table
CREATE TABLE IF NOT EXISTS cities_location (
    id INT AUTO_INCREMENT,
    city_id INT,
    latitude DECIMAL(8, 4),
    longitude DECIMAL(8, 4),
    PRIMARY KEY(id),
    FOREIGN KEY(city_id) REFERENCES cities(city_id)
);
-- create weather table
CREATE TABLE IF NOT EXISTS weathers (
    id INT AUTO_INCREMENT,
    city_id INT,
    forecast_time DATETIME,
    forecast VARCHAR(200),
    temperature DECIMAL (4, 2),
    temperature_feels_like DECIMAL (4, 2),
    humidity INT,
    cloudiness INT,
    rain INT,
    snow INT,
    probability DECIMAL(3, 2),
    wind_speed DECIMAL(4, 2),
    wind_direction INT,
    wind_gust DECIMAL(4, 2),
    PRIMARY KEY(id),
    FOREIGN KEY(city_id) REFERENCES cities(city_id)
);
-- create airports table
CREATE TABLE IF NOT EXISTS airports (
    airport_id VARCHAR(25),
    airport_name VARCHAR(255),
    PRIMARY KEY (airport_id)
);
-- create cities_airports table
CREATE TABLE IF NOT EXISTS cities_airports (
    city_id INT,
    airport_id VARCHAR(5),
    PRIMARY KEY(city_id, airport_id),
    FOREIGN KEY(city_id) REFERENCES cities(city_id),
    FOREIGN KEY(airport_id) REFERENCES airports(airport_id)
);
-- create airport location table
CREATE TABLE IF NOT EXISTS airports_location (
    id INT AUTO_INCREMENT,
    airport_id VARCHAR(5),
    latitude DECIMAL(8, 4),
    longitude DECIMAL(8, 4),
    PRIMARY KEY(id),
    FOREIGN KEY(airport_id) REFERENCES airports(airport_id)
);
-- create flights table
CREATE TABLE IF NOT EXISTS flights (
    flight_id INT NOT NULL AUTO_INCREMENT,
    airport_id VARCHAR(5),
    flight_number VARCHAR(25),
    departure_city VARCHAR(200),
    arrival_time DATETIME,
    terminal INT,
    PRIMARY KEY (flight_id),
    FOREIGN KEY (airport_id) REFERENCES airports(airport_id)
);