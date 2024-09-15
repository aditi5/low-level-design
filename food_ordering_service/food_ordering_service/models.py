from db_connection import DatabaseConnection
from typing import List, Dict, Optional


class UserDB:
    def __init__(self):
        self.conn = DatabaseConnection().get_connection()
        self.cursor = self.conn.cursor()

    def add_user(self, name: str, gender: str, phone_number: str, pincode: str) -> None:
        self.cursor.execute('''
            INSERT INTO users (name, gender, phone_number, pincode)
            VALUES (?, ?, ?, ?)
        ''', (name, gender, phone_number, pincode))
        self.conn.commit()

    def get_user_by_phone(self, phone_number: str) -> Optional[Dict]:
        self.cursor.execute('''
            SELECT * FROM users WHERE phone_number = ?
        ''', (phone_number,))
        row = self.cursor.fetchone()
        if row:
            return {'id': row[0], 'name': row[1], 'gender': row[2], 'phone_number': row[3], 'pincode': row[4]}
        return None


class RestaurantDB:
    def __init__(self):
        self.conn = DatabaseConnection().get_connection()
        self.cursor = self.conn.cursor()

    def add_restaurant(self, name: str, serviceable_pincodes: str, food_item_name: str, food_item_price: float,
                       quantity: int) -> None:
        self.cursor.execute('''
            INSERT INTO restaurants (name, serviceable_pincodes, food_item_name, food_item_price, quantity)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, serviceable_pincodes, food_item_name, food_item_price, quantity))
        self.conn.commit()

    def update_quantity(self, name: str, quantity_to_add: int) -> None:
        self.cursor.execute('''
            UPDATE restaurants SET quantity = quantity + ? WHERE name = ?
        ''', (quantity_to_add, name))
        self.conn.commit()

    def get_restaurants_by_pincode(self, pincode: str) -> List[Dict]:
        self.cursor.execute('''
            SELECT * FROM restaurants WHERE serviceable_pincodes LIKE ? AND quantity > 0
        ''', ('%' + pincode + '%',))
        rows = self.cursor.fetchall()
        return [{'id': row[0], 'name': row[1], 'serviceable_pincodes': row[2], 'food_item_name': row[3],
                 'food_item_price': row[4], 'quantity': row[5]} for row in rows]


class OrderDB:
    def __init__(self):
        self.conn = DatabaseConnection().get_connection()
        self.cursor = self.conn.cursor()

    def place_order(self, user_id: int, restaurant_id: int, quantity: int) -> None:
        self.cursor.execute('''
            INSERT INTO orders (user_id, restaurant_id, quantity)
            VALUES (?, ?, ?)
        ''', (user_id, restaurant_id, quantity))
        self.conn.commit()


class RatingDB:
    def __init__(self):
        self.conn = DatabaseConnection().get_connection()
        self.cursor = self.conn.cursor()

    def add_rating(self, user_id: int, restaurant_id: int, rating: int, comment: Optional[str] = None) -> None:
        self.cursor.execute('''
            INSERT INTO ratings (user_id, restaurant_id, rating, comment)
            VALUES (?, ?, ?, ?)
        ''', (user_id, restaurant_id, rating, comment))
        self.conn.commit()

    def get_ratings_by_restaurant(self, restaurant_id: int) -> List[Dict]:
        self.cursor.execute('''
            SELECT * FROM ratings WHERE restaurant_id = ?
        ''', (restaurant_id,))
        rows = self.cursor.fetchall()
        return [{'id': row[0], 'user_id': row[1], 'restaurant_id': row[2], 'rating': row[3], 'comment': row[4],
                 'rating_date': row[5]} for row in rows]
