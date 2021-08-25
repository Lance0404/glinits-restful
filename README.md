# glinits-restful

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
    


