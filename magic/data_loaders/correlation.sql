-- Docs: https://docs.mage.ai/guides/sql-blocks
-- Correlation between confirmed cases and deaths
SELECT CORR(confirmed, deaths) AS correlation
FROM mrt_covid19_clean_data;
