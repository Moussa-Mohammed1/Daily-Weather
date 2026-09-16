CREATE TABLE IF NOT EXISTS cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,

    CONSTRAINT unique_city_name UNIQUE (name)
);


CREATE TABLE IF NOT EXISTS weather_forecasts (
    id SERIAL PRIMARY KEY,

    city_id INTEGER NOT NULL,

    forecast_date DATE NOT NULL,

    temperature_max DOUBLE PRECISION,
    temperature_min DOUBLE PRECISION,

    precipitation_sum DOUBLE PRECISION,
    precipitation_probability DOUBLE PRECISION,

    wind_speed_max DOUBLE PRECISION,
    wind_gust_max DOUBLE PRECISION,

    weather_code INTEGER,

    temperature_category VARCHAR(30),
    precipitation_category VARCHAR(30),
    wind_category VARCHAR(30),

    temperature_risk DOUBLE PRECISION,
    precipitation_risk DOUBLE PRECISION,
    wind_risk DOUBLE PRECISION,

    risk_score DOUBLE PRECISION,
    risk_level VARCHAR(20),

    CONSTRAINT fk_weather_city
        FOREIGN KEY (city_id)
        REFERENCES cities(id),

    CONSTRAINT unique_city_forecast
        UNIQUE (city_id, forecast_date)
);