# file organization
* models denote tables
* entity denotes all others 
* dto denotes http request/response (not used yet)

# the API call sequence (top to bottom)
1. route function here: `buying_frenzy/api/v1/restaurant.py`
1. `view.py` handles complex logic
1. `service.py` interacts with database

