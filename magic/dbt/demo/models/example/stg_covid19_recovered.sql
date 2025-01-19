WITH raw AS (
    SELECT * FROM {{ source('postgres', 'covid19_recovered') }}
),
transformed AS (
   SELECT 
        key AS date,
        province_state,
        country_region,
        lats,
        longs,
        value::INTEGER AS recovered
    FROM raw, jsonb_each(cases)
)
SELECT * FROM transformed
