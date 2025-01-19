# Magez
Implement Mage.AI to Ingest, Transform, Store, Analysis Data Test


## COVID-19 Data Pipeline and Analysis

This project involves transforming COVID-19 data, storing it in a PostgreSQL database, and performing complex data analysis. Below are the steps to set up the environment, load data, transform it, and run the analysis.

## Dataset
Use COVID-19 Data Repository by Johns Hopkins University. https://github.com/CSSEGISandData/COVID-19/tree/master/archived_data/archived_time_series

## Setup Instructions

### Prerequisites

- Docker
- Docker Compose

### Step 1: Clone the Repository

Clone this repository to your local machine:

```sh
git clone https://github.com/jogjezz/Magez.git
cd Magez
```
### Run Docker Compose

Run the Docker containers using Docker Compose

```sh
docker-compose up
```

open a browser to http://localhost:6789. 
From the pipelines page, select **dbt_demo** and open the notebook view by selecting **Edit pipeline** from the left side nav.
Select the first block by clicking it and select the “play” icon in the top right to run the block. You’ve just ran your first Mage block & loaded data from a dataset!


There are several blocks in this pipeline, it includes load data covid19 , store data to postgres, transforming using DBT and analyze using SQL block
these are example of analyze queries :

#### Top 5 most common values in country_region:

```sql
SELECT country_region, COUNT(*) AS frequency
FROM mrt_covid19_clean_data
GROUP BY country_region
ORDER BY frequency DESC
LIMIT 5;

```

#### Metric change over time (confirmed cases): 
```sql

SELECT
    date,
    SUM(confirmed) AS total_confirmed
FROM
    mrt_covid19_clean_data
GROUP BY
    date
ORDER BY
    date;
```

#### Correlation between confirmed cases and deaths:
```sql

SELECT CORR(confirmed, deaths) AS correlation
FROM mrt_covid19_clean_data;
```