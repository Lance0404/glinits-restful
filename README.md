# glinits-restful

## Todo list
1. setup Ngnix and WSGI server in front of the Flask server
1. setup Psql db and connect with sqlalchemy from the python app
1. create RESTful APIs that CRUD against db

## RESTful API with Postgresql support

* while preparing the interview for Glints, I decided to refresh basic web skills with the most up-to-date technology. 

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
    * `poetry env use /usr/bin/python`

### install dependencies
1. `poetry add flask`
    

### Issues
1. The poetry installed from the `python:3.9.6-slim` image failed to support complete poetry installation. Shows error like below:
    ```sh
    => ERROR [builder-base 5/5] RUN poetry install --no-dev                                                                                0.4s
    ------                                                                                                                                       
    > [builder-base 5/5] RUN poetry install --no-dev:                                                                                           
    #10 0.370 Traceback (most recent call last):                                                                                                 
    #10 0.370   File "/opt/poetry/bin/poetry", line 17, in <module>
    #10 0.370     from poetry.console import main
    #10 0.370   File "/opt/poetry/lib/poetry/console/__init__.py", line 1, in <module>
    #10 0.370     from .application import Application
    #10 0.370   File "/opt/poetry/lib/poetry/console/application.py", line 1, in <module>
    #10 0.370     from cleo import Application as BaseApplication
    #10 0.370 ModuleNotFoundError: No module named 'cleo'
    ```
    * so I downgraded the image to `python:3.8-slim` and modified `pyproject.toml` to `python = "^3.8"`. 
    * [WARNING] This could cause trouble while I was developing with python3.9 by run with python3.8. 
### Reference
1. [Dockerfile example](https://www.mktr.ai/the-data-scientists-quick-guide-to-dockerfiles-with-examples/)
1. [Flask custom commands](https://flask.palletsprojects.com/en/2.0.x/cli/#custom-commands)

