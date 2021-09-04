# glinits-restful

## Todo list

1. [flask configuration best practice](https://flask.palletsprojects.com/en/2.0.x/config/#configuration-best-practices)
1. setup Ngnix and WSGI server in front of the Flask server



## RESTful API with Postgresql support

* While preparing the interview for Glints, I decided to refresh basic web skills with the most up-to-date technology. 
* So I kept as many comments in my code as possible

* ingredients:
1. Python3.9
1. Poetry
1. Flask
1. uwsgi
1. Postgresql
1. docker
1. redis? 
1. Celery

### Dev environment setup
1. install latest stable [python version](https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz) on Ubuntu20.04 in WSL2 with this [article](https://linuxize.com/post/how-to-install-python-3-9-on-ubuntu-20-04/).
1. bind the latest installed python version to the python executable with this [article](https://stackoverflow.com/a/50331137)
    * `[sudo] update-alternatives --install /usr/bin/python python /bin/python3.9 10`
    * showed this message:
    * update-alternatives: using /bin/python3.9 to provide /usr/bin/python (python) in auto mode
    * `python -V`
    * Python 3.9.6
1. install [poetry](https://python-poetry.org/docs/)
    * `poetry --version`
    * Poetry version 1.1.8
1. enable tab completion for Oh-My-Zsh with this [article](https://python-poetry.org/docs/#enable-tab-completion-for-bash-fish-or-zsh)

### Project setup
1. `poetry new glinits-restful` (this should be done before setting up the git repo)
    * or you can do `poetry init` instead from pre-existing project 
1. specify the python verison for poetry to use
    * `poetry env use /usr/bin/python` (Python 3.9.6)
    * I choose use docker base image `python:3.9.7-slim` 

### Docker image
* docker build --no-cache -t test .
* docker build --no-cache -t test --progress=plain .
* docker build -t test --progress=plain .
* docker build --no-cache -t glinits_app .

### Docker container
* docker exec -it glinits_app bash
* docker logs -f -n 10 glinits_app
* docker-compose logs -f --tail=10 glinits_app

* clean up & initiate app
```sh
docker rm glinits_app
docker rmi glinits_app
docker-compose up app
```

### start the Flask app
1. while at local dev env
```sh
# requried env vars were set in .env and .flaskenv
flask run
```

### Debug
* Always make sure you are using the same `poetry` version at local and while docker build!

* connect to psql with command
```sh
# access container
docker exec -it glinits_psql bash
psql glinits lance
# list tables in current db
\dt+
# describe table
\d [tablename]
```

1. to drop database (failed, but I have flask cli solution)
```sql
-- try
DROP DATABASE glinits;

-- if failed do below
SELECT *
FROM pg_stat_activity
WHERE datname = 'glinits';

SELECT pg_terminate_backend (pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'glinits';

DROP DATABASE glinits;
```

* try clean up db with docker command
```sh
# remove volume
docker-compose down -v

docker-compose up -d
# confirmed that db was gone
```

### Reference
1. [Dockerfile example](https://www.mktr.ai/the-data-scientists-quick-guide-to-dockerfiles-with-examples/)
1. [Flask custom commands](https://flask.palletsprojects.com/en/2.0.x/cli/#custom-commands)
1. [Environment variables from dotenv](https://flask.palletsprojects.com/en/2.0.x/cli/#environment-variables-from-dotenv)
1. [create database if not exists with sqlalchemy](https://stackoverflow.com/a/30971098)
1. [Using foreign key ON DELETE cascade with ORM relationships](https://docs.sqlalchemy.org/en/14/orm/cascades.html#using-foreign-key-on-delete-cascade-with-orm-relationships)
1. [__str__ vs __repr__ in TW version](https://ithelp.ithome.com.tw/articles/10194593)
1. [list comprehension & generator expression](https://www.learncodewithmike.com/2020/01/python-comprehension.html)
1. [how to implement generator & `yield from` in TW version](https://ithelp.ithome.com.tw/articles/10196328)
1. [static, class, instance method](https://www.learncodewithmike.com/2020/01/python-method.html)
1. [basic relationship pattern](https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html)
1. [breakpoint()](https://www.journaldev.com/22695/python-breakpoint)
1. [how to modify a specific commit](https://stackoverflow.com/a/1186549)

### Issues with solutions
1. [sqlalchemy create all does not create tables](https://stackoverflow.com/a/20749534)
    * In short, put models code before create_all() 
1. [sqlalchemy tables with relationship & Alembic example](https://blog.techbridge.cc/2017/08/12/python-web-flask101-tutorial-sqlalchemy-orm-database-models/)
1. [sqlalchemy ORM query guide](https://docs.sqlalchemy.org/en/14/orm/queryguide.html)
1. [relationship loading technique](https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html)
1. [sqlalchemy session rollback](https://docs.sqlalchemy.org/en/14/orm/tutorial.html#rolling-back)
1. [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/)
1. [convert postman collection format from v1 to v2](https://learning.postman.com/docs/getting-started/importing-and-exporting-data/#converting-postman-collections-from-v1-to-v2)
    * `flask postman`
    * `postman-collection-transformer convert -i data/glinits.json -o data/glinits_v2.json -j 1.0.0 -p 2.0.0 -P`
    * `cp data/glinits_v2.json /mnt/c/Users/lance/Downloads`

## Wish list
1. come up with a FAST API solution    