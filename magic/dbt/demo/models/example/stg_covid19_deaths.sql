WITH raw AS (
    SELECT * FROM {{ source('postgres', 'covid19_deaths') }}
),
transformed AS (
   SELECT 
        key AS date,
        province_state,
        country_region,
        lats,
        longs,
        value::INTEGER AS deaths
    FROM raw, jsonb_each(cases)
)
SELECT * FROM transformed
