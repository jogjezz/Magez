WITH raw AS (
    SELECT * FROM {{ source('postgres', 'covid19_confirmed') }}
),
transformed AS (
    SELECT 
        key AS date,
        province_state,
        country_region,
        lats,
        longs,
        value::INTEGER AS confirmed
    FROM raw, jsonb_each(cases)
)
SELECT * FROM transformed
