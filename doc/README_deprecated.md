
* Less important than the `README` in the project root

### Deprecated commands
* For uploading the raw data directly into database without preprocessing
    * ETL: import restaurant data to database
    ```sh
    flask etl data/restaurant_with_menu.json
    ```
    * ETL: import user data to database
    ```sh
    flask etl data/users_with_purchase_history.json
    ```