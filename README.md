# Buying Frenzy

* a [task](https://gist.github.com/seahyc/97b154ce5bfd4f2b6e3a3a99a7b93f69) from Glinits for skill assessment.

# Fresh start service
* First have psql running at `postgresql://lance:lance123@localhost:5432/glinits`
* CWD, current work dir, should be at project root
* Drop all tables and restart service will recreate the tables
```sh 
flask drop-all
flask run
```
* ETL: import restaurant data to database
```sh
flask etl data/restaurant_with_menu.json
```

### Todo list (kept updating)
* ETL

### Notes
* [READM_dev.md]((README_dev.md)) is my personal notes while developing