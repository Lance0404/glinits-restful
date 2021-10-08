from buying_frenzy.cli import pre_etl
from buying_frenzy.service import RestaurantService, CustomerService

def test_pre_etl(runner, app):
    ret = runner.invoke(pre_etl, ['--dir', 'tests/data'])
    assert ret.output == ''
    with app.app_context():
        user = CustomerService.get_user_by_id(id=150)
        assert user.name == 'Tomas Brown'
        assert user.cash_balance == 933.92
        restaurant = RestaurantService.get_restaurant_by_id(id=1)
        assert restaurant.cash_balance == 4497.34
        assert restaurant.name == "'Ulu Ocean Grill and Sushi Lounge"
        menu = RestaurantService.get_menu_by_restaurant_id(id=1)
        assert len(menu) == 14

def test_ListOpeningRestaurant_get(test_client):
    resp = test_client.get('/v1/restaurant/list', query_string={'datetime': '08/31/2021 10:37 PM'})   
    assert resp.status_code == 200
    assert resp.get_json()['counts'] == 1
    assert len(resp.get_json()['open_restaurants']) == 1


def test_ListTopRestaurantByDishAndPrice_get(test_client):
    resp = test_client.get('/v1/restaurant/list/3/dish/more/3/price', query_string={'min': 13, 'max': 15})
    assert len(resp.get_json()) == 1
    assert resp.get_json()[0] == {'dish_count': 4, 'restaurant_name': "'Ulu Ocean Grill and Sushi Lounge"}

    resp = test_client.get('/v1/restaurant/list/3/dish/less/3/price', query_string={'min': 11, 'max': 12})
    assert resp.get_json() == [{'dish_count': 3, 'restaurant_name': '024 Grille'},
        {'dish_count': 2, 'restaurant_name': "'Ulu Ocean Grill and Sushi Lounge"}]

def test_SearchBy(test_client):
    resp = test_client.get('/v1/restaurant/search/restaurant/rill')
    assert len(resp.get_json()) == 2
    assert resp.get_json() == [["'Ulu Ocean Grill and Sushi Lounge", 1], ['024 Grille', 2]]

    resp = test_client.get('/v1/restaurant/search/dish/wine')
    assert len(resp.get_json()) == 2
    assert resp.get_json() == [['Coffee Cocktail (Port Wine', 3], ['DRY LIGHT IMPORTED WINE', 5]]

def test_Buy_successful_1(test_client):
    user = CustomerService.get_user_by_id(id=150)  
    restaurant = RestaurantService.get_restaurant_by_id(id=1)
    dish = RestaurantService.get_dish_by_restaurant_id_and_dish_id(1, 2)
    assert user.cash_balance == 933.92  
    assert restaurant.cash_balance == 4497.34
    assert dish.dish_name == 'GAI TOM KA: CHICKEN IN COCONUT CREAM SOUP WITH LIME JUICE GALANGA AND CHILI'
    assert dish.price == 10.64

    resp = test_client.put('/v1/user/150/buy/1/2')
    assert resp.get_data() == b'"transaction successful"\n'

    user = CustomerService.get_user_by_id(id=150)  
    restaurant = RestaurantService.get_restaurant_by_id(id=1)
    assert user.cash_balance == 923.28
    assert restaurant.cash_balance == 4507.9800000000005

def test_Buy_successful_2(test_client):
    user = CustomerService.get_user_by_id(id=616)  
    restaurant = RestaurantService.get_restaurant_by_id(id=2)
    dish = RestaurantService.get_dish_by_restaurant_id_and_dish_id(2, 15)
    assert user.cash_balance == 299.58  
    assert restaurant.cash_balance == 4894.81
    assert dish.dish_name == 'Sweetbreads'
    assert dish.price == 13.57

    resp = test_client.put('/v1/user/616/buy/2/15')
    user = CustomerService.get_user_by_id(id=616)
    restaurant = RestaurantService.get_restaurant_by_id(id=2)
    assert resp.get_data() == b'"transaction successful"\n'
    assert user.cash_balance == 286.01
    assert restaurant.cash_balance == 4908.38

def test_Buy_failed(test_client):
    resp = test_client.put('/v1/user/151/buy/1/2')
    assert resp.get_data() == b'User not found'
