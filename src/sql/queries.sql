-- Which cities have the highest average risk?

SELECT
    c.name AS city,
    ROUND(AVG(w.risk_score), 2) AS average_risk_score
FROM weather_forecasts w
JOIN cities c
    ON w.city_id = c.id
GROUP BY c.name
ORDER BY average_risk_score DESC;

-- What are the highest-risk forecast days?
SELECT
    c.name AS city,
    w.forecast_date,
    w.risk_score,
    w.risk_level
FROM weather_forecasts w
JOIN cities c
    ON w.city_id = c.id
ORDER BY w.risk_score DESC
LIMIT 10;

-- How many risky days does each city have?
SELECT
    c.name AS city,
    COUNT(*) AS risky_days
FROM weather_forecasts w
JOIN cities c
    ON w.city_id = c.id
WHERE w.risk_level IN ('High', 'Critical')
GROUP BY c.name
ORDER BY risky_days DESC;

-- Which cities have the most precipitation?

SELECT
    c.name AS city,
    ROUND(SUM(w.precipitation_sum), 2) AS total_precipitation
FROM weather_forecasts w
JOIN cities c
    ON w.city_id = c.id
GROUP BY c.name
ORDER BY total_precipitation DESC;

-- Which forecast days have strong winds?

SELECT
    c.name AS city,
    w.forecast_date,
    w.wind_speed_max,
    w.wind_gust_max
FROM weather_forecasts w
JOIN cities c
    ON w.city_id = c.id
WHERE w.wind_speed_max >= 40
ORDER BY w.wind_speed_max DESC;

