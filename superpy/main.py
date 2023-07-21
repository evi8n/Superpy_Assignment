# Imports
import argparse
import csv
import datetime
from uuid import uuid4
from tabulate import tabulate
import re
import os
import random

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.


class ProductDetails:
    def __init__(self):
        pass

    def print_product_by_id(self):
        csv_file = "current_inventory.csv"
        product_id = input("Enter product ID:")
        if product_id:
            with open(csv_file, "r") as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
                found_product = False
                data = []
                for row in reader:
                    if row["ID"].lower() == product_id.lower():
                        found_product = True
                        data.append(list(row.values()))

                if found_product:
                    print("Product details:")
                    product_table = tabulate(data, fieldnames, tablefmt="grid")
                    print(product_table)
                else:
                    print(f"No product found with ID {product_id}")


class Personel:
    def __init__(self, manager_id_csv):
        self.manager_id_csv = manager_id_csv
        self.manager_id = None

    def generate_manager_id(self):
        self.manager_id = "".join(str(random.randint(0, 9)) for _ in range(6))
        print(f"New manager ID created: {self.manager_id}")
        self.write_to_csv()

    def write_to_csv(self):
        with open(self.manager_id_csv, "a", newline="") as file:
            fieldnames = ["Manager ID", "Date created"]
            current_date = datetime.date.today()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(
                {
                    "Manager ID": self.manager_id,
                    "Date created": current_date,
                }
            )


class Inventory:
    def __init__(self, csv_file):
        self.csv_file = csv_file

    def print_current_inventory(self):
        csv_file = "current_inventory.csv"
        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            data = [list(row.values()) for row in reader]
        print("Current Inventory:")
        inventory_table = tabulate(data, fieldnames, tablefmt="grid")
        print(inventory_table)

    def add_product_to_inventory(self):
        csv_file = "current_inventory.csv"
        new_product = {}

        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames

            while True:
                user_input_id = input(
                    "Enter product ID (type 'q' or 'quit' to cancel product addition):"
                )
                if user_input_id.lower() in ["q", "quit"]:
                    print("Addition of new product cancelled.")
                    return

                if not user_input_id:
                    print("Invalid input. Please enter a product ID.")
                    continue

                new_product["ID"] = user_input_id

                new_product_name = str(input("Enter product name:"))
                new_product["Name"] = new_product_name

                while True:
                    buy_price = input("Enter buy price:")
                    try:
                        buy_price = float(buy_price)
                        if buy_price != 0.0:
                            new_product["Buy price"] = buy_price
                            break
                        else:
                            print("Buy price cannot be zero.")
                    except ValueError:
                        print("Invalid input. Buy price must be a positive float.")

                while True:
                    sell_price = input("Enter sell price:")
                    try:
                        sell_price = float(sell_price)
                        if sell_price != 0.0:
                            new_product["Sell price"] = sell_price
                            break
                        else:
                            print("Sell price cannot be zero.")
                    except ValueError:
                        print("Invalid input. Sell price must be a positive float.")

                quantity = input("Enter quantity:")
                if not quantity.isdigit() or int(quantity) == 0:
                    print("Invalid input. Quantity must be a positive number.")
                    continue

                new_product["In stock"] = quantity
                # Set restock date to current date automatically
                new_product["Restock date"] = datetime.date.today().isoformat()

                new_product["Bought for restock"] = quantity

                # Set the "Sold since restock" value to 0
                new_product["Sold since restock"] = 0

                if user_input_id.startswith("FP"):
                    while True:
                        expiration_date = input("Enter expiration date (YYYY-MM-DD):")
                        if not re.match(r"\d{4}-\d{2}-\d{2}$", expiration_date):
                            print(
                                "Invalid input. Expiration date must be in the format YYYY-MM-DD."
                            )
                            continue
                        new_product["Expiration date"] = expiration_date
                        break
                elif user_input_id.startswith("NF"):
                    new_product["Expiration date"] = "-"
                else:
                    print("Invalid input. Product ID must start with NF or FP.")
                    continue

                with open(csv_file, "a", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writerow(new_product)

                print(f"Product {new_product['ID']} added to inventory.")

                break

    def update_inventory(self):
        csv_file = "current_inventory.csv"
        product_id = input("Enter product ID:")
        field_to_update = input("Enter field to be updated:").strip('"')
        new_value = input("Enter the new value:")

        inventory_data = []
        found_product = False

        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            while field_to_update not in fieldnames:
                print(f"Field {field_to_update} not found.")
                field_to_update = input("Please enter field to be updated again:")
            for row in reader:
                if row["ID"] == product_id:
                    row[field_to_update.strip()] = new_value
                    found_product = True
                inventory_data.append(row)

        if not found_product:
            print(f"No product found with ID {product_id}")
            return

        with open(csv_file, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(inventory_data)

            print(
                f"Field {field_to_update} for product {product_id} updated to {new_value}."
            )

    def update_stock_quantity(self):
        csv_file = "current_inventory.csv"
        product_id = input("Enter product ID:")

        while True:
            try:
                quantity_bought = int(input("Enter quantity bought:"))
                break
            except ValueError:
                print("Invalid input. Please enter an integer.")

        inventory_data = []
        found_product = False
        new_quantity = 0

        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["ID"] == product_id:
                    current_quantity = int(row["In stock"])
                    new_quantity = current_quantity + quantity_bought
                    row["In stock"] = str(new_quantity)
                    found_product = True
                inventory_data.append(row)

        if not found_product:
            print(f"No product found with ID {product_id}")

        with open(csv_file, "w", newline="") as file:
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(inventory_data)

            print(
                f"Inventory updated. New quantity of product {product_id} currently in stock: {new_quantity}"
            )

    def delete_inventory_entry(self):
        csv_file = "current_inventory.csv"
        product_id = input("Enter product ID to be deleted:")

        matching_entries = []
        with open(csv_file, "r") as input_file:
            reader = csv.DictReader(input_file)
            for row in reader:
                if row["ID"] == product_id:
                    matching_entries.append(row)

        if not matching_entries:
            print(f"No product found with ID {product_id}.")
            return

        if len(matching_entries) == 1:
            matching_entry = matching_entries[0]
        else:
            print(f"Multiple entries found with ID {product_id}.")
            expiration_date = input(
                "Please specify expiration date of the entry to delete (YYYY-MM-DD):"
            )
            matching_entry = None
            for entry in matching_entries:
                if entry["Expiration date"] == expiration_date:
                    matching_entry = entry
                    break

        if not matching_entry:
            print(
                f"No product found with ID {product_id} and expiration date {expiration_date}."
            )
            return

        print("Product details:")
        print(matching_entry)

        manager_id = input("Enter manager's ID for confirmation:")
        id_of_manager = Personel.generate_manager_id()
        if manager_id != id_of_manager:
            print("Invalid manager's ID. Deletion cancelled.")
            return

        confirmation = input("Are you sure you want to delete this entry? (y/n):")
        if confirmation.lower() != "y":
            print("Deletion cancelled.")
            return

        temp_file = "temp.csv"
        rows_to_write = []
        with open(csv_file, "r") as input_file:
            reader = csv.DictReader(input_file)
            for row in reader:
                if row != matching_entry:
                    rows_to_write.append(row)

        with open(temp_file, "w", newline="") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(rows_to_write)

        os.replace(temp_file, csv_file)
        print(
            f"Product with ID {product_id} and expiration date {expiration_date} was deleted from inventory."
        )


class Transactions:
    def __init__(self, csv_file, transactions_bought, transactions_sold):
        self.csv_file = csv_file
        self.transactions_bought = transactions_bought
        self.transactions_sold = transactions_sold

    def record_transaction_bought(self):
        csv_file = "current_inventory.csv"
        transactions_bought_file = "transactions_bought.csv"
        new_transaction = {}

        while True:
            user_input_id = input(
                "Enter product ID (type 'q' or 'quit' to cancel transaction):"
            )
            if user_input_id.lower() in ["q", "quit"]:
                print("Transaction recording cancelled.")
                return

            if not user_input_id:
                print("Invalid input. Please enter a product ID.")
                continue

            new_transaction["ID"] = user_input_id

            quantity = input("Enter quantity bought:")
            if not quantity.isdigit() or int(quantity) == 0:
                print("Invalid input. Quantity must be a positive number.")
                continue

            new_transaction["In stock"] = quantity
            new_transaction["Transaction ID"] = str(uuid4())
            new_transaction["Restock date"] = datetime.date.today().isoformat()

            expiration_date = input("Enter expiration date (YYYY-MM-DD):")
            if not re.match(r"\d{4}-\d{2}-\d{2}$", expiration_date):
                print(
                    "Invalid input. Expiration date must be in the format YYYY-MM-DD."
                )
                continue

            new_transaction["Expiration date"] = expiration_date

            product_id = new_transaction["ID"]
            quantity = int(new_transaction["In stock"])
            date = new_transaction["Restock date"]
            transaction_id = new_transaction["Transaction ID"]

            break

        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            inventory_data = list(reader)

        # Find the product data in the current inventory CSV file
        found_product = False
        for product in inventory_data:
            if (
                product["ID"] == product_id
                and product["Expiration date"] == expiration_date
            ):
                current_quantity = int(product["In stock"])
                new_quantity = current_quantity + int(quantity)
                product["In stock"] = str(new_quantity)
                product["Restock date"] = date
                found_product = True
                break

        if not found_product:
            print(f"No product found with ID {product_id}")
            return
            # Get original product's data
        original_product = None
        for product in inventory_data:
            if product["ID"] == product_id:
                original_product = product
                break

            if original_product is not None:
                # Append new entry of product if it has a different expiration date
                new_product = {
                    "ID": product_id,
                    "Name": original_product["Name"],
                    "In stock": quantity,
                    "Buy price": original_product["Buy price"],
                    "Restock date": date,
                    "Bought for restock": quantity,
                    "Sell price": original_product["Sell price"],
                    "Sold since restock": "0",
                    "Expiration date": expiration_date,
                }
                inventory_data.append(new_product)

        with open(csv_file, "w", newline="") as file:
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(inventory_data)

        # Add the transaction to the transactions bought CSV file
        with open(transactions_bought_file, "a", newline="") as file:
            writer = csv.writer(file)
            fieldnames = [transaction_id, product_id, quantity, date]
            writer.writerow(fieldnames)
        print("Transaction recorded.")

    def record_transaction_sold(self):
        csv_file = "current_inventory.csv"
        transactions_sold_file = "transactions_sold.csv"
        new_transaction = {}

        while True:
            user_input_id = input(
                "Enter product ID (type 'q' or 'quit' to cancel transaction):"
            )
            if user_input_id.lower() in ["q", "quit"]:
                print("Transaction recording cancelled.")
                return

            if not user_input_id:
                print("Invalid input. Please enter a product ID.")
                continue

            new_transaction["ID"] = user_input_id

            quantity = input("Enter quantity sold:")
            if not quantity.isdigit() or int(quantity) == 0:
                print("Invalid input. Quantity must be a positive number.")
                continue

            new_transaction["In stock"] = quantity
            new_transaction["Transaction ID"] = str(uuid4())

            product_id = new_transaction["ID"]
            quantity = int(new_transaction["In stock"])
            date = datetime.date.today().isoformat()
            transaction_id = new_transaction["Transaction ID"]

            break

        transaction_sold_data = []
        found_product = False

        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            for row in reader:
                if row["ID"] == product_id:
                    current_quantity = int(row["In stock"])
                    new_quantity = current_quantity - int(quantity)
                    row["In stock"] = str(new_quantity)
                    current_sold_quantity = int(row["Sold since restock"])
                    new_sold_quantity = current_sold_quantity + int(quantity)
                    row["Sold since restock"] = str(new_sold_quantity)
                    found_product = True
                transaction_sold_data.append(row)

        if not found_product:
            print(f"No product found with ID {product_id}")
            return

        # Update current inventory with new quantity
        with open(csv_file, "w", newline="") as file:
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(transaction_sold_data)

        # Add the transaction to the transactions bought CSV file
        with open(transactions_sold_file, "a", newline="") as file:
            writer = csv.writer(file)
            fieldnames = [transaction_id, product_id, quantity, date]
            writer.writerow(fieldnames)

        # Print the transaction details
        transaction_data = [fieldnames]
        transaction_table = tabulate(transaction_data, tablefmt="grid")
        print("Transaction recorded.")
        print(transaction_table)


class ReportCreation:
    def __init__(
        self,
        expiring_products_csv,
        low_inventory_csv,
    ):
        self.expiring_products_csv = expiring_products_csv
        self.low_inventory_csv = low_inventory_csv

    def print_expiring_products(self):
        csv_file = "current_inventory.csv"
        current_date = datetime.date.today()
        threshold = current_date + datetime.timedelta(days=30)

        # Open and read csv file
        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames + ["Days to expire:"]

            # Iterate through products in inventory and check for expiration dates 30 days or less away
            expiring_products = []
            for row in reader:
                expiration_date_str = row["Expiration date"]
                if expiration_date_str and expiration_date_str != "-":
                    expiration_date = datetime.datetime.strptime(
                        expiration_date_str, "%Y-%m-%d"
                    ).date()
                    if current_date <= expiration_date <= threshold:
                        days_to_expire = (expiration_date - current_date).days
                        row["Days to expire:"] = days_to_expire
                        expiring_products.append(row)

        if expiring_products:
            with open("expiring_products.csv", "w", newline="") as expiring_file:
                writer = csv.DictWriter(expiring_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(expiring_products)

                print("Expiring products report created.")
                print("Expiring products:")
                expiring_products_table = tabulate(
                    expiring_products, headers="keys", tablefmt="grid"
                )
                print(expiring_products_table)
        else:
            print("No products expiring in the next 30 days.")

    def print_low_inventory(self):
        csv_file = "current_inventory.csv"
        threshold = 30

        # Open and read csv file
        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames

            # Iterate through products in inventory and check for products with a stock count less than 30
            low_inventory = []
            for row in reader:
                products_in_stock_str = row["In stock"]
                products_in_stock = int(products_in_stock_str)
                if products_in_stock <= threshold:
                    low_inventory.append(row)

        if low_inventory:
            with open("low_inventory.csv", "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(low_inventory)

                print("Low inventory report created.")
                print("Low inventory products:")
                low_inventory_table = tabulate(
                    low_inventory, headers="keys", tablefmt="grid"
                )
                print(low_inventory_table)

    def print_expired_products(self):
        csv_file = "current_inventory.csv"
        current_date = datetime.date.today()
        expired_products = []
        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames + ["Total expired"]
            for row in reader:
                expiration_date = row["Expiration date"]
                if (
                    expiration_date != "-"
                    and datetime.datetime.strptime(expiration_date, "%Y-%m-%d").date()
                    < current_date
                ):
                    row["Total expired"] = row["In stock"]
                    expired_products.append(row)
        with open("expired_products.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(expired_products)

        if expired_products:
            print("Expired products report created.")
            print("Expired products:")
            expired_products_table = tabulate(
                expired_products, headers="keys", tablefmt="grid"
            )
            print(expired_products_table)
        else:
            print("No expired products.")

    def print_transactions_sold(self):
        with open("transactions_sold.csv", "r") as file:
            reader = csv.reader(file)
            transactions_sold_data = list(reader)
            transactions_sold_table = tabulate(transactions_sold_data, tablefmt="grid")

            print("Sale transactions data:")
            print(transactions_sold_table)

    def print_transactions_bought(self):
        with open("transactions_bought.csv", "r") as file:
            reader = csv.reader(file)
            transactions_bought_data = list(reader)
            transactions_bought_table = tabulate(
                transactions_bought_data, tablefmt="grid"
            )

            print("Buying transactions data:")
            print(transactions_bought_table)

    def report_revenue_profit(self):
        start_date_str = input("Enter start date (YYYY-MM-DD):")
        end_date_str = input("Enter end date (YYYY-MM-DD):")

        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()

        transactions_bought = "transactions_bought.csv"
        transactions_sold = "transactions_sold.csv"
        csv_file = "current_inventory.csv"
        revenue = 0
        expenses = 0

        with open(transactions_bought, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                transaction_date = datetime.datetime.strptime(row[3], "%Y-%m-%d").date()
                if start_date <= transaction_date <= end_date:
                    product_id = row[1]
                    quantity = int(row[2])
                    buy_price = 0

            # Get the product's price from the current inventory
            with open(csv_file, "r") as inventory_file:
                inventory_reader = csv.DictReader(inventory_file)
                for inventory_row in inventory_reader:
                    if inventory_row["ID"] == product_id:
                        buy_price = float(inventory_row["Buy price"])
                        break
            expenses += buy_price * quantity

        with open(transactions_sold, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                transaction_date = datetime.datetime.strptime(row[3], "%Y-%m-%d").date()
                if start_date <= transaction_date <= end_date:
                    product_id = row[1]
                    quantity = int(row[2])
                    sell_price = 0

                # Get the product's price from the current inventory
                with open(csv_file, "r") as inventory_file:
                    inventory_reader = csv.DictReader(inventory_file)
                    for inventory_row in inventory_reader:
                        sell_price = float(inventory_row["Sell price"])
                        break
                revenue += sell_price * quantity

        profit = revenue - expenses
        print(f"Revenue: {revenue}")
        print(f"Profit: {profit}")
        return revenue, profit


class DateManager:
    def __init__(self, date_file):
        self.date_file = date_file
        self.current_date = self.load_current_date()

    def load_current_date(self):
        if os.path.exists(self.date_file):
            with open(self.date_file, "r") as file:
                date_str = file.read()
                try:
                    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                except ValueError:
                    pass
        return datetime.date.today()

    def save_current_date(self):
        with open(self.date_file, "w") as file:
            file.write(self.current_date.strftime("%Y-%m-%d"))

    def advance_time(self, days):
        self.current_date += datetime.timedelta(days=days)
        self.save_current_date()

    def get_current_date(self):
        return self.current_date


def main():
    args = parse_arguments()
    inventory = Inventory(args.current_inventory_csv)
    transactions = Transactions(
        args.current_inventory_csv,
        args.transactions_bought,
        args.transactions_sold,
    )
    product_details = ProductDetails()
    date_manager = DateManager(args.date_file)
    report_creation = ReportCreation(
        args.expiring_products_csv,
        args.low_inventory_csv,
    )
    personel = Personel("manager_id.csv")

    if args.command == "add_new_product":
        inventory.add_product_to_inventory()
    elif args.command == "print_current_inventory":
        inventory.print_current_inventory()
    elif args.command == "update_stock":
        inventory.update_stock_quantity()
    elif args.command == "update_inventory":
        inventory.update_inventory()
    elif args.command == "delete_inventory_entry":
        inventory.delete_inventory_entry()
    elif args.command == "generate_manager_id":
        personel.generate_manager_id()
    elif args.command == "print_expiring_products":
        report_creation.print_expiring_products()
    elif args.command == "print_low_inventory":
        report_creation.print_low_inventory()
    elif args.command == "print_expired_products":
        report_creation.print_expired_products()
    elif args.command == "print_transactions_sold":
        report_creation.print_transactions_sold()
    elif args.command == "print_transactions_bought":
        report_creation.print_transactions_bought()
    elif args.command == "record_transaction_bought":
        transactions.record_transaction_bought(date_manager.get_current_date())
    elif args.command == "record_transaction_sold":
        transactions.record_transaction_sold(date_manager.get_current_date())
    elif args.command == "report_profit":
        report_creation.report_revenue_profit()
    elif args.command == "print_product_details":
        product_details.print_product_by_id()
    elif args.command == "advance_date":
        date_manager.advance_time(args.days)
        print(
            f"The date in {args.days} days will be {date_manager.get_current_date()}."
        )


# Define command-line-arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Superpy")

    parser.add_argument(
        "command",
        choices=[
            "add_new_product",
            "print_current_inventory",
            "print_expiring_products",
            "print_low_inventory",
            "print_expired_products",
            "print_transactions_sold",
            "print_transactions_bought",
            "update_stock",
            "update_inventory",
            "delete_inventory_entry",
            "generate_manager_id",
            "advance_date",
            "record_transaction_bought",
            "record_transaction_sold",
            "report_profit",
            "print_product_details",
        ],
        help="Specify commands: add_new product, print current inventory, print expiring products, print low inventory, print expired products, print_transactions_sold, print_transactions_bought, update_stock, update inventory, delete inventory entry, generate manager id, advance date, record transaction bought, record transaction sold, report profit, print product details",
    )

    parser.add_argument(
        "--advance_date",
        default="current_date.txt",
        help="Path to the current date file",
    )
    parser.add_argument(
        "--current_inventory_csv",
        nargs="?",
        help="Path to the current_inventory CSV file",
    )
    parser.add_argument("--product_id", nargs="?", help="ID of product to be printed")

    parser.add_argument(
        "--expiring_products_csv",
        nargs="?",
        help="Path to the products_expiring CSV file",
    )
    parser.add_argument(
        "--low_inventory_csv",
        nargs="?",
        help="Path to the low inventory products CSV file",
    )
    parser.add_argument(
        "--print_expired_products",
        action="store_true",
        help="Print a list of expired products",
    )
    parser.add_argument(
        "--print_transactions_sold",
        action="store_true",
        help="Print all the sale transactions",
    )
    parser.add_argument(
        "--print_transactions_bought",
        action="store_true",
        help="Print all the buying transactions",
    )
    parser.add_argument(
        "--update_stock",
        action="store_true",
        help="Update stock quantity in current inventory",
    )
    parser.add_argument(
        "--update_inventory", action="store_true", help="Print the updated inventory"
    )
    parser.add_argument(
        "--delete_inventory_entry",
        action="store_true",
        help="Delete a whole inventory entry",
    )
    parser.add_argument("--advance_time", type=int, help="Number of days to advance")
    parser.add_argument(
        "--transactions_bought",
        nargs="?",
        help="Path to the transactions bought CSV file",
    )
    parser.add_argument(
        "--transactions_sold", nargs="?", help="Path to the transactions sold CSV file"
    )
    parser.add_argument(
        "--report_profit", action="store_true", help="Print the revenue and profit"
    )
    parser.add_argument(
        "--quantity", nargs="?", help="Quantity of product sold or bought"
    )
    parser.add_argument("days", type=int, nargs="?", help="Number of days to advance")
    parser.add_argument(
        "--date_file", default="current_date.txt", help="Path to the current date file"
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
