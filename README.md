# Buying Frenzy
* a [task](https://gist.github.com/seahyc/97b154ce5bfd4f2b6e3a3a99a7b93f69) from Glinits for skill assessment.

### Start service with docker
* `docker build -t glinits_app .` to build docker image `glinits_app` locally
* `docker-compose up -d` to init the services accordingly
* (Optional) for clean up & restart
    * `docker exec -it glinits_app flask drop-all` to clean up old data if any
    * `docker-compose down; docker-compose up -d` is necessary for flask app to recreate the tables
* (Monitoring)    
    * `docker-compose logs -f --tail=10` to check the services are healthy    
* `docker exec -it glinits_app flask pre-etl` to ETL (~ 30 s on my PC)

# API documentations
* Swagger UI: `http://127.0.0.1:5000/v1/doc/`

### Notes
* [READM_dev.md](./doc/README_dev.md) is my personal notes while developing