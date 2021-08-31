# file organization
* `model.py` defines table schema
* `entity.py` denotes data objects 
* dto denotes http request/response (not used yet)

# the API call sequence (top to bottom)
1. `buying_frenzy/endpoints/v1/restaurant.py` defines routes
1. `view.py` handles complex logic
1. `service.py` interacts with the database

