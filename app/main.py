import json
import os
from typing import Dict, Any, List, Optional

from app.shop import Shop
from app.customer import Customer
from app.car import Car


def shop_trip() -> None:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "config.json")

    with open(config_path, "r") as file:
        data: Dict[str, Any] = json.load(file)

    fuel_price: float = data["FUEL_PRICE"]

    shops: List[Shop] = [
        Shop(shop["name"], shop["location"], shop["products"])
        for shop in data["shops"]
    ]

    customers: List[Customer] = []

    for customer_data in data["customers"]:
        car = Car(
            customer_data["car"]["brand"],
            customer_data["car"]["fuel_consumption"]
        )

        customer = Customer(
            customer_data["name"],
            customer_data["location"],
            customer_data["money"],
            car,
            customer_data["product_cart"]
        )

        customers.append(customer)

    for customer in customers:
        print(f"{customer.name} has {customer.money:g} dollars")

        home_location = customer.location.copy()
        cheapest_shop: Optional[Shop] = None
        min_full_cost = float("inf")
        final_products_cost = 0.0

        for shop in shops:
            distance = (
                (customer.location[0] - shop.location[0]) ** 2
                + (customer.location[1] - shop.location[1]) ** 2
            ) ** 0.5

            fuel_needed = (
                distance / 100
            ) * customer.car.fuel_consumption * 2

            fuel_cost = fuel_needed * fuel_price

            products_cost = sum(
                shop.products[name] * qty
                for name, qty in customer.products.items()
            )

            full_cost = fuel_cost + products_cost

            print(
                f"{customer.name}'s trip to the {shop.name} "
                f"costs {full_cost:.2f}"
            )

            if full_cost < min_full_cost:
                min_full_cost = full_cost
                final_products_cost = products_cost
                cheapest_shop = shop

        if cheapest_shop and customer.money >= min_full_cost:
            print(f"{customer.name} rides to {cheapest_shop.name}\n")

            # 🔥 ВАЖЛИВО (з рев’ю)
            customer.location = cheapest_shop.location

            cheapest_shop.print_receipt(
                customer,
                customer.products,
                final_products_cost
            )

            print()

            customer.money -= min_full_cost
            customer.location = home_location

            print(f"{customer.name} rides home")

            if customer != customers[-1]:
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

            if customer != customers[-1]:
                print(f"{message}\n")
            else:
                print(message)


if __name__ == "__main__":
    shop_trip()