-- Docs: https://docs.mage.ai/guides/sql-blocks
-- Top 5 most common values in country_region
SELECT country_region, COUNT(*) AS frequency
FROM mrt_covid19_clean_data
GROUP BY country_region
ORDER BY frequency DESC
LIMIT 5;
