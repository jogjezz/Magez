{{ config(materialized='table') }}

WITH confirmed AS (
    SELECT * FROM {{ ref('stg_covid19_confirmed') }}
),
recovered AS (
    SELECT * FROM {{ ref('stg_covid19_recovered') }}
),
deaths AS (
    SELECT * FROM {{ ref('stg_covid19_deaths') }}
),
clean_data AS (
    SELECT
        COALESCE(c.province_state, r.province_state, d.province_state) AS province_state,
        COALESCE(c.country_region, r.country_region, d.country_region) AS country_region,
        COALESCE(c.lats, r.lats, d.lats) AS lats,
        COALESCE(c.longs, r.longs, d.longs) AS longs,
        COALESCE(c.date, r.date, d.date) AS date,
        c.confirmed,
        r.recovered,
        d.deaths
    FROM confirmed c
    FULL OUTER JOIN recovered r
        ON c.province_state = r.province_state
        AND c.country_region = r.country_region
        AND c.lats = r.lats
        AND c.longs = r.longs
        AND c.date = r.date
    FULL OUTER JOIN deaths d
        ON c.province_state = d.province_state
        AND c.country_region = d.country_region
        AND c.lats = d.lats
        AND c.longs = d.longs
        AND c.date = d.date                                                                                                                              
)
SELECT * FROM clean_data
