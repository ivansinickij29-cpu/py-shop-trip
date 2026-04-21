import json
import datetime
import math
import os
from typing import List, Dict, Tuple, Any, Optional

from app.shop import Shop
from app.customer import Customer
from app.car import Car


def calculate_distance(
    location1: List[int],
    location2: List[int]
) -> float:
    return math.sqrt(
        (location1[0] - location2[0]) ** 2
        + (location1[1] - location2[1]) ** 2
    )


def calculate_trip_cost(
    customer: Customer,
    shop: Shop,
    fuel_price: float
) -> Tuple[float, float]:
    distance: float = calculate_distance(
        customer.location,
        shop.location,
    )

    fuel_needed: float = (
        distance / 100
    ) * customer.car.fuel_consumption * 2

    fuel_cost: float = fuel_needed * fuel_price

    products_cost: float = sum(
        shop.products[name] * qty
        for name, qty in customer.products.items()
    )

    return fuel_cost + products_cost, products_cost


def shop_trip() -> None:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "config.json")

    with open(config_path, "r") as f:
        data: Dict[str, Any] = json.load(f)

    fuel_price: float = data["FUEL_PRICE"]

    shop_list: List[Shop] = [
        Shop(
            shop_data["name"],
            shop_data["location"],
            shop_data["products"],
        )
        for shop_data in data["shops"]
    ]

    customer_list: List[Customer] = []

    for customer_data in data["customers"]:
        car = Car(
            customer_data["car"]["brand"],
            customer_data["car"]["fuel_consumption"],
        )

        customer = Customer(
            customer_data["name"],
            customer_data["location"],
            customer_data["money"],
            car,
            customer_data["product_cart"],
        )

        customer_list.append(customer)

    for customer in customer_list:
        print(f"{customer.name} has {customer.money:g} dollars")

        home_location: List[int] = customer.location.copy()
        cheapest_shop: Optional[Shop] = None
        min_full_cost: float = float("inf")
        final_products_cost: float = 0.0

        for shop in shop_list:
            full_cost, prod_cost = calculate_trip_cost(
                customer,
                shop,
                fuel_price,
            )

            print(
                f"{customer.name}'s trip to the {shop.name} "
                f"costs {full_cost:.2f}"
            )

            if full_cost < min_full_cost:
                min_full_cost = full_cost
                final_products_cost = prod_cost
                cheapest_shop = shop

        if cheapest_shop and customer.money >= min_full_cost:
            print(f"{customer.name} rides to {cheapest_shop.name}\n")

            date_str = datetime.datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S"
            )

            print(f"Date: {date_str}")
            print(f"Thanks, {customer.name}, for your purchase!")
            print("You have bought:")

            for name, qty in customer.products.items():
                price = cheapest_shop.products[name]

                print(
                    f"{qty} {name}s for "
                    f"{price * qty:g} dollars"
                )

            print(
                f"Total cost is "
                f"{final_products_cost:g} dollars"
            )

            print("See you again!\n")

            customer.money -= min_full_cost
            customer.location = home_location

            print(f"{customer.name} rides home")

            if customer != customer_list[-1]:
                print(
                    f"{customer.name} now has "
                    f"{customer.money:.2f} dollars\n"
                )
            else:
                print(
                    f"{customer.name} now has "
                    f"{customer.money:.2f} dollars"
                )
        else:
            message = (
                f"{customer.name} doesn't have enough money "
                f"to make a purchase in any shop"
            )

            if customer != customer_list[-1]:
                print(f"{message}\n")
            else:
                print(message)


if __name__ == "__main__":
    shop_trip()
