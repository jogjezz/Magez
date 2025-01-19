# Magez
Implement Mage.AI to Ingest, Transform, Store, Analysis Data Test


## Create network

docker network create magez

RUN docker compose up -d

Launch mage http://localhost:6789

# DBT

go to magic>terminal or open http://localhost:6789/terminal

cd demo_project/dbt
dbt init -s demo
touch demo/profiles.yml


03:12:55  Running with dbt=1.7.4

03:12:55  

Your new dbt project "demo" was created!