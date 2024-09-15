from service import UserService, RestaurantService, OrderService, RatingService


def main():
    user_service = UserService()
    restaurant_service = RestaurantService()
    order_service = OrderService()
    rating_service = RatingService()

    # Register Users
    user_service.register_user("Pralove", "M", "phoneNumber-1", "HSR")
    user_service.register_user("Nitesh", "M", "phoneNumber-2", "BTM")
    user_service.register_user("Vatsal", "M", "phoneNumber-3", "BTM")

    # Login User
    if user_service.login_user("phoneNumber-1"):
        # Register Restaurants
        restaurant_service.register_restaurant("Food Court-1", "BTM/HSR", "NI Thali", 100, 5)
        restaurant_service.register_restaurant("Food Court-2", "BTM", "Burger", 120, 2)

        # List Restaurants
        serviceable_restaurants = restaurant_service.get_serviceable_restaurants("BTM", "price")
        print("Serviceable Restaurants: ", serviceable_restaurants)

        # Place Orders
        order_service.place_order(user_service.current_user_id, 1, 2)

        # Rate Restaurants
        rating_service.rate_restaurant(user_service.current_user_id, 1, 5, "Good food")
    else:
        print("User login failed")


if __name__ == "__main__":
    main()
