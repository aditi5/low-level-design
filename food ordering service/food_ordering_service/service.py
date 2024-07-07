from models import UserDB, RestaurantDB, OrderDB, RatingDB
from typing import List, Dict, Optional


class UserService:
    def __init__(self):
        self.user_db = UserDB()
        self.current_user_id = None

    def register_user(self, name: str, gender: str, phone_number: str, pincode: str) -> None:
        self.user_db.add_user(name, gender, phone_number, pincode)

    def login_user(self, phone_number: str) -> bool:
        user = self.user_db.get_user_by_phone(phone_number)
        if user:
            self.current_user_id = user['id']
            return True
        return False


class RestaurantService:
    def __init__(self):
        self.restaurant_db = RestaurantDB()

    def register_restaurant(self, name: str, serviceable_pincodes: str, food_item_name: str, food_item_price: float,
                            initial_quantity: int) -> None:
        self.restaurant_db.add_restaurant(name, serviceable_pincodes, food_item_name, food_item_price, initial_quantity)

    def update_quantity(self, name: str, quantity_to_add: int) -> None:
        self.restaurant_db.update_quantity(name, quantity_to_add)

    def get_serviceable_restaurants(self, pincode: str, sort_by: str) -> List[Dict]:
        restaurants = self.restaurant_db.get_restaurants_by_pincode(pincode)
        if sort_by == 'rating':
            restaurants.sort(key=lambda x: x['rating'], reverse=True)
        elif sort_by == 'price':
            restaurants.sort(key=lambda x: x['food_item_price'], reverse=True)
        return restaurants


class OrderService:
    def __init__(self):
        self.order_db = OrderDB()

    def place_order(self, user_id: int, restaurant_id: int, quantity: int) -> bool:
        self.order_db.place_order(user_id, restaurant_id, quantity)
        return True


class RatingService:
    def __init__(self):
        self.rating_db = RatingDB()

    def rate_restaurant(self, user_id: int, restaurant_id: int, rating: int, comment: Optional[str] = None) -> None:
        self.rating_db.add_rating(user_id, restaurant_id, rating, comment)
