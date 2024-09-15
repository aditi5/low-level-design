import sqlite3
from sqlite3 import Connection, Cursor


class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._connection = sqlite3.connect('food_ordering.db')
            cls._instance._create_tables()
        return cls._instance

    def _create_tables(self):
        cursor = self._connection.cursor()
        cursor.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gender TEXT NOT NULL,
            phone_number TEXT UNIQUE NOT NULL,
            pincode TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            serviceable_pincodes TEXT NOT NULL,
            food_item_name TEXT NOT NULL,
            food_item_price REAL NOT NULL,
            quantity INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            restaurant_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(restaurant_id) REFERENCES restaurants(id)
        );

        CREATE TABLE IF NOT EXISTS ratings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            restaurant_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT,
            rating_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(restaurant_id) REFERENCES restaurants(id)
        );
        ''')
        self._connection.commit()

    def get_connection(self) -> Connection:
        return self._connection

    def close_connection(self):
        if self._connection:
            self._connection.close()
            self._instance = None

# Usage example:
# db = DatabaseConnection().get_connection()
