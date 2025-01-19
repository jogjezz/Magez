-- Docs: https://docs.mage.ai/guides/sql-blocks
-- Metric change over time (confirmed cases)
SELECT
    date,
    SUM(confirmed) AS total_confirmed
FROM
    mrt_covid19_clean_data
GROUP BY
    date
ORDER BY
    date;



