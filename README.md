# Buying Frenzy
* a [task](https://gist.github.com/seahyc/97b154ce5bfd4f2b6e3a3a99a7b93f69) from Glinits for skill assessment.

### Prerequisites
* linux, docker, docker-compose

### Start service with docker
* `docker build -t glinits_app .` to build docker image `glinits_app` locally
* `docker-compose up -d` to init the services accordingly
* (Optional) for clean up & restart
    * `docker exec -it glinits_app flask drop-all` to clean up old data if any
    * `docker-compose restart app` is necessary for flask app to recreate the tables
* (Monitoring)    
    * `docker-compose logs -f --tail=10` to check the services are healthy    
* `docker exec -it glinits_app flask pre-etl` to ETL (~ 30 s on my PC)

### API documentations
* Swagger UI: `http://localhost/v1/doc/`

### Test
* Prerequisites: poetry

* `poetry shell` then `poetry install` to setup local testing environment
* `pytest --cov=buying_frenzy` to test and report coverage

### Notes
* [READM_dev.md](./doc/README_dev.md) is my personal notes while developing