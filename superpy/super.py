# Imports
import argparse
import csv
import datetime
from uuid import uuid4
from tabulate import tabulate
import re
import os
import random
import matplotlib.pyplot as plt

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.


class Personel:
    def __init__(self, manager_id_csv):
        self.manager_id_csv = manager_id_csv
        self.manager_id = None

    # Generate a new manager ID consisting of 6 random digits, save it in the "manager_id" CSV file and record the current date
    def generate_manager_id(self):
        self.manager_id = "".join(str(random.randint(0, 9)) for _ in range(6))
        print(f"New manager ID created: {self.manager_id}")
        self.write_to_csv()

    def get_last_manager_id(self):
        try:
            with open(self.manager_id_csv, "r", newline="") as file:
                reader = csv.reader(file)
                next(reader, None)
                last_row = None
                for row in reader:
                    last_row = row
                if last_row:
                    return last_row[0]
        except FileNotFoundError:
            return None

    def write_to_csv(self):
        with open(self.manager_id_csv, "a", newline="") as file:
            fieldnames = ["Manager ID", "Date created"]
            current_date = datetime.date.today()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
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
        # Read the "current_inventory" CSV file and print its contents in the form of a table
        csv_file = "current_inventory.csv"
        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            data = [list(row.values()) for row in reader]
        print("Current Inventory:")
        inventory_table = tabulate(data, fieldnames, tablefmt="grid")
        print(inventory_table)

    def validate_product_id(self, product_id):
        return re.match(r"^(NF|FP)\d{3}[A-Za-z]{2}$", product_id) is not None

    def print_product_by_id(self):
        # Print product details read from the "current_inventory" CSV file based on product ID
        csv_file = "current_inventory.csv"
        product_id = input("Enter product ID:")

        if not self.validate_product_id(product_id):
            print(
                "Invalid input. Product ID must be in the format NF/FP + 3 digits + 2 letters."
            )
            return

        if product_id:
            with open(csv_file, "r") as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
                found_product = False
                data = []
                for row in reader:
                    if row["Product ID"].lower() == product_id.lower():
                        found_product = True
                        data.append(list(row.values()))

                if found_product:
                    print("Product details:")
                    product_table = tabulate(data, fieldnames, tablefmt="grid")
                    print(product_table)
                else:
                    print(f"No product found with ID {product_id}")

    def add_product_to_inventory(self):
        # Open current_inventory CSV file, input details of new product and append it
        csv_file = "current_inventory.csv"
        new_product = {}

        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames

            # Check if product ID is inputted in the correct format (otherwise print feedback),
            # and give user the option of exiting without making changes
            while True:
                product_id_input = input(
                    "Enter product ID (type 'q' or 'quit' to cancel product addition):"
                )
                if product_id_input.lower() in ["q", "quit"]:
                    print("No product added.")
                    return

                if not self.validate_product_id(product_id_input):
                    print(
                        "Invalid input. Product ID must be in the format NF/FP + 3 digits + 2 letters."
                    )
                    continue

                new_product_name = ""

                while not new_product_name.strip():
                    new_product_name = input("Enter product name:")
                    if not new_product_name.strip():
                        print("Product name cannot be empty.")

                new_product["Product ID"] = product_id_input
                new_product["Product Name"] = new_product_name
                new_product["Quantity in stock"] = int(0)

                # Check that Cost price is inputted in the correct format (otherwise print feedback)
                while True:
                    cost_price = input("Enter cost price:")
                    try:
                        float_cost_price = float(cost_price)
                        if (
                            not re.match(r"^\d+\.\d{2}$", cost_price)
                            or float_cost_price <= 0
                        ):
                            raise ValueError(
                                "Invalid input. Cost price must be a positive float with two decimals."
                            )
                        formatted_cost_price = "{:.2f}".format(float_cost_price)
                        new_product["Cost price"] = formatted_cost_price
                        break
                    except ValueError:
                        print(
                            "Invalid input. Cost price must be a positive float with two decimals."
                        )

                # Set restock date to current date automatically
                new_product["Restock date"] = "-"
                new_product["Quantity bought for restock"] = int(0)

                # Check that Retail price and quantity is inputted in the correct format (otherwise print feedback)
                while True:
                    retail_price = input("Enter retail price:")
                    try:
                        float_retail_price = float(retail_price)
                        if (
                            not re.match(r"^\d+\.\d{2}$", retail_price)
                            or float_retail_price <= 0
                        ):
                            raise ValueError(
                                "Invalid input. Retail price must be a positive float with two decimals."
                            )
                        formatted_retail_price = "{:.2f}".format(float_retail_price)
                        new_product["Retail price"] = formatted_retail_price
                        break
                    except ValueError:
                        print(
                            "Invalid input. Cost price must be a positive float with two decimals."
                        )

                # Set the "Sold since restock" value to 0
                new_product["Sold since restock"] = int(0)

                # Define different behaviour if the new product's ID starts with FP (Food Product) or NF (Non-Food),
                # so that the user is only required to input an expiration date for Food Products
                if product_id_input.startswith("FP"):
                    while True:
                        expiration_date = input("Enter expiration date (YYYY-MM-DD):")
                        if not re.match(r"\d{4}-\d{2}-\d{2}$", expiration_date):
                            print(
                                "Invalid input. Expiration date must be in the format YYYY-MM-DD."
                            )
                            continue
                        new_product["Expiration date"] = expiration_date
                        break
                elif product_id_input.startswith("NF"):
                    new_product["Expiration date"] = "-"
                else:
                    print("Invalid input. Product ID must start with NF or FP.")
                    continue

                product_exists = False
                with open(csv_file, "r") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row["Product ID"] == product_id_input:
                            product_exists = True
                            # Check if the rest of the fields match
                            if (
                                row["Product Name"] == new_product["Product Name"]
                                and row["Cost price"] == new_product["Cost price"]
                                and row["Retail price"] == new_product["Retail price"]
                                and row["Expiration date"]
                                == new_product.get("Expiration date", "-")
                            ):
                                # If all fields match, prompt the user to confirm adding a new entry
                                choice = input(
                                    "This product already exists. Do you want to add a new entry anyway? (y/n): "
                                )

                                if choice.lower() != "y":
                                    print("Product not added.")
                                    return
                                else:
                                    break

                if not product_exists:
                    new_product["Product ID"] = product_id_input

                with open(csv_file, "a", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writerow(new_product)

                print("New product added to inventory.")

                break

    def update_inventory_entry(self):
        # Update any field of an existing product in the "current_inventory" CSV file
        csv_file = "current_inventory.csv"
        product_id = input("Enter product ID:")

        if not self.validate_product_id(product_id):
            print(
                "Invalid input. Product ID must be in the format NF/FP + 3 digits + 2 letters."
            )
            return

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
                if row["Product ID"] == product_id:
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

    def delete_inventory_entry(self):
        # Delete a whole inventory entry from the "current_inventory" CSV file
        csv_file = "current_inventory.csv"
        product_id = input("Enter product ID to be deleted:")

        if not self.validate_product_id(product_id):
            print(
                "Invalid input. Product ID must be in the format NF/FP + 3 digits + 2 letters."
            )
            return

        # Check if there are multiple entries with the same product ID,
        # and if there are (e.g multiple entries of the same product but with different expiration dates)
        # specify which entry is to be deleted by expiration date
        matching_entries = []
        with open(csv_file, "r") as input_file:
            reader = csv.DictReader(input_file)
            for row in reader:
                if row["Product ID"] == product_id:
                    if product_id.startswith("FP"):
                        matching_entries.append(row)
                    else:
                        matching_entries = [row]

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

        # Ask for confirmation before deletion by asking for the manager's ID
        manager_id = input("Enter manager's ID for confirmation:")
        personel_instance = Personel("manager_id.csv")
        last_manager_id = personel_instance.get_last_manager_id()
        if manager_id != last_manager_id:
            print("Invalid manager's ID. Deletion cancelled.")
            return

        confirmation = input("Are you sure you want to delete this entry? (y/n):")
        if confirmation.lower() != "y":
            print("Deletion cancelled.")
            return

        # Create a temporary file "temp.csv" to hold the updated inventory data without the selected entry
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

        # Replace the original "current_inventory" CSV file with the temporary file, which does not include the deleted entry
        os.replace(temp_file, csv_file)

        if product_id.startswith("FP"):
            print(
                f"Product with ID {product_id} and expiration date {expiration_date} was deleted from inventory."
            )
        else:
            print(f"Product with ID {product_id} was deleted from inventory.")


class Transactions:
    def __init__(self, csv_file, transactions_bought, transactions_sold, date_manager):
        self.csv_file = csv_file
        self.transactions_bought = transactions_bought
        self.transactions_sold = transactions_sold
        self.date_manager = date_manager

    def validate_product_id(self, product_id):
        return re.match(r"^(NF|FP)\d{3}[A-Za-z]{2}$", product_id) is not None

    def record_transaction_bought(self, current_date):
        # Record an inventory purchase transaction by inputting a product ID
        # update the quantity currently in stock for selected product
        csv_file = "current_inventory.csv"
        transactions_bought_file = "transactions_bought.csv"
        new_transaction = {}

        # Check if product ID is inputted in the correct format (otherwise print feedback),
        # and give user the option of exiting without making changes
        while True:
            product_id_input = input(
                "Enter product ID (type 'q' or 'quit' to cancel transaction):"
            )
            if product_id_input.lower() in ["q", "quit"]:
                print("Transaction recording cancelled.")
                return

            if not self.validate_product_id(product_id_input):
                print(
                    "Invalid input. Product ID must be in the format NF/FP + 3 digits + 2 letters."
                )
                continue

            new_transaction["Product ID"] = product_id_input

            # Define different behaviour if the new product's ID starts with FP (Food Product) or NF (Non-Food),
            # so that the user is only required to input an expiration date for Food Products
            if product_id_input.startswith("FP"):
                while True:
                    expiration_date = input("Enter expiration date (YYYY-MM-DD):")
                    if not re.match(r"\d{4}-\d{2}-\d{2}$", expiration_date):
                        print(
                            "Invalid input. Expiration date must be in the format YYYY-MM-DD."
                        )
                        continue
                    new_transaction["Expiration date"] = expiration_date
                    break
            elif product_id_input.startswith("NF"):
                new_transaction["Expiration date"] = "-"
            else:
                print("Invalid input. Product ID must start with NF or FP.")
                continue

            # Check that the quantity is inputted in the correct format (otherwise print feedback)
            quantity = input("Enter quantity bought:")
            if not quantity.isdigit() or int(quantity) == 0:
                print("Invalid input. Quantity must be a positive number.")
                continue

            new_transaction["Quantity in stock"] = quantity

            # Create a unique transaction ID
            new_transaction["Transaction ID"] = str(uuid4())
            new_transaction["Restock date"] = current_date

            product_id = new_transaction["Product ID"]
            quantity = int(new_transaction["Quantity in stock"])
            date = new_transaction["Restock date"]
            transaction_id = new_transaction["Transaction ID"]
            expiration_date = new_transaction["Expiration date"]

            break

        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            inventory_data = list(reader)

        # Find the product data in the current inventory CSV file
        found_product = False
        for product in inventory_data:
            if (
                product["Product ID"] == product_id
                and product["Expiration date"] == expiration_date
            ):
                current_quantity = int(product["Quantity in stock"])
                new_quantity = current_quantity + int(quantity)
                product["Quantity in stock"] = str(new_quantity)
                product["Restock date"] = date
                product["Quantity bought for restock"] = quantity
                found_product = True
                print("Recorded transaction bought on:", current_date)
                break

        # Get original product's data
        original_product = None
        for product in inventory_data:
            if product["Product ID"] == product_id:
                original_product = product
                break

            if original_product is not None:
                # Append new entry of product if it has a different expiration date
                new_product = {
                    "Product ID": product_id,
                    "Product Name": original_product["Product Name"],
                    "Quantity in stock": quantity,
                    "Cost price": original_product["Cost price"],
                    "Restock date": date,
                    "Quantity bought for restock": quantity,
                    "Retail price": original_product["Retail price"],
                    "Sold since restock": int(0),
                    "Expiration date": expiration_date,
                }
                inventory_data.append(new_product)

        if not found_product:
            print(
                f"No product found with ID {product_id} and expiration date {expiration_date}."
                "Use add_new_product command to add a new product entry to the current inventory."
            )
            return

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

    def record_transaction_sold(self, current_date):
        # Record an inventory sale transaction by inputting a product ID
        # update the quantity currently in stock for selected product
        csv_file = "current_inventory.csv"
        transactions_sold_file = "transactions_sold.csv"
        new_transaction = {}

        # Check if product ID is inputted in the correct format (otherwise print feedback),
        # and give user the option of exiting without making changes
        while True:
            product_id_input = input(
                "Enter product ID (type 'q' or 'quit' to cancel transaction):"
            )
            if product_id_input.lower() in ["q", "quit"]:
                print("Transaction recording cancelled.")
                return

            if not self.validate_product_id(product_id_input):
                print(
                    "Invalid input. Product ID must be in the format NF/FP + 3 digits + 2 letters."
                )
                continue

            new_transaction["Product ID"] = product_id_input

            # Check if quantity is inputted in the correct format (otherwise print feedback)
            quantity = input("Enter quantity sold:")
            if not quantity.isdigit() or int(quantity) == 0:
                print("Invalid input. Quantity must be a positive number.")
                continue

            new_transaction["Quantity in stock"] = quantity
            new_transaction["Transaction ID"] = str(uuid4())

            product_id = new_transaction["Product ID"]
            quantity = int(new_transaction["Quantity in stock"])
            date = current_date
            transaction_id = new_transaction["Transaction ID"]

            break

        transaction_sold_data = []
        found_product = False
        expiration_date = None

        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            for row in reader:
                if row["Product ID"] == product_id:
                    found_product = True
                    transaction_sold_data.append(row)
                    if expiration_date is None:
                        expiration_date = row["Expiration date"]
                    elif expiration_date != row["Expiration date"]:
                        expiration_date = input(
                            f"Multiple entries found with product ID {product_id}. Enter the specific expiration date (YYYY-MM-DD): "
                        )
                        break

        original_data = []
        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            original_data = [row for row in reader]

        found_product = False

        for row in original_data:
            if (
                row["Product ID"].strip() == product_id
                and row["Expiration date"].strip() == expiration_date
            ):
                current_quantity = int(row["Quantity in stock"])
                new_quantity = current_quantity - int(quantity)
                row["Quantity in stock"] = str(new_quantity)
                current_sold_quantity = int(row["Sold since restock"])
                new_sold_quantity = current_sold_quantity + int(quantity)
                row["Sold since restock"] = str(new_sold_quantity)
                found_product = True
                break

        if not found_product:
            print(
                f"No product found with ID {product_id}. Use add_new_product command to add a new product entry to the current inventory."
            )
            return

        # Update current inventory with new quantity
        with open(csv_file, "w", newline="") as file:
            fieldnames = reader.fieldnames
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(original_data)

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
        date_manager,
    ):
        self.expiring_products_csv = expiring_products_csv
        self.low_inventory_csv = low_inventory_csv
        self.date_manager = date_manager

    def print_expiring_products(self):
        # Generate a report of expiring products within the next 30 days
        csv_file = "current_inventory.csv"
        current_date = self.date_manager
        threshold = current_date + datetime.timedelta(days=30)

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

        # If products are found with an expiration date less than 30 days away,
        # create a report and print the contents
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
        # Generate a report of products with a stock quantity less than 30
        csv_file = "current_inventory.csv"
        threshold = 30

        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames

            # Iterate through products in inventory and check for products with a stock count less than 30
            low_inventory = []
            for row in reader:
                products_in_stock_str = row["Quantity in stock"]
                products_in_stock = int(products_in_stock_str)
                if products_in_stock <= threshold:
                    low_inventory.append(row)

        # If products are found with a stock quantity less than 30,
        # create a report and print the contents
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
        # Generate a report of products with a past expiration date
        csv_file = "current_inventory.csv"
        current_date = self.date_manager
        expired_products = []

        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames + ["Total expired"]

            # Iterate through products in inventory and check for products with a past expiration date
            for row in reader:
                expiration_date = row["Expiration date"]
                if (
                    expiration_date != "-"
                    and datetime.datetime.strptime(expiration_date, "%Y-%m-%d").date()
                    < current_date
                ):
                    row["Total expired"] = row["Quantity in stock"]
                    expired_products.append(row)
        with open("expired_products.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(expired_products)

        # If products are found with a past expiration date,
        # create a report and print the contents
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
        # Print a report with all sale transactions
        with open("transactions_sold.csv", "r") as file:
            reader = csv.reader(file)
            transactions_sold_data = list(reader)
            transactions_sold_table = tabulate(transactions_sold_data, tablefmt="grid")

            print("Sale transactions data:")
            print(transactions_sold_table)

    def print_transactions_bought(self):
        # Print a report with all inventory purchase transactions
        with open("transactions_bought.csv", "r") as file:
            reader = csv.reader(file)
            transactions_bought_data = list(reader)
            transactions_bought_table = tabulate(
                transactions_bought_data, tablefmt="grid"
            )

            print("Buying transactions data:")
            print(transactions_bought_table)

    def report_revenue_profit(self):
        # Calculate revenue and profit for a specific period of time
        start_date_str = input("Enter start date (YYYY-MM-DD):")
        end_date_str = input("Enter end date (YYYY-MM-DD):")

        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()

        transactions_bought = "transactions_bought.csv"
        transactions_sold = "transactions_sold.csv"
        csv_file = "current_inventory.csv"
        revenue_list = []
        profit_list = []
        dates = []

        # Read transactions_bought.csv into memory
        with open(transactions_bought, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            transactions_bought_data = list(reader)

        for row in transactions_bought_data:
            transaction_date = datetime.datetime.strptime(row[3], "%Y-%m-%d").date()
            if start_date <= transaction_date <= end_date:
                product_id = row[1]
                quantity = int(row[2])
                cost_price = 0

                # Get the product's price from the current inventory
                with open(csv_file, "r") as inventory_file:
                    inventory_reader = csv.DictReader(inventory_file)
                    for inventory_row in inventory_reader:
                        if inventory_row["Product ID"] == product_id:
                            cost_price = float(inventory_row["Cost price"])
                            break
                expenses = cost_price * quantity
                dates.append(transaction_date)
                profit_list.append(0)
                revenue_list.append(-expenses)

        # Read transactions_sold.csv into memory
        with open(transactions_sold, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            transactions_sold_data = list(reader)

        for row in transactions_sold_data:
            transaction_date = datetime.datetime.strptime(row[3], "%Y-%m-%d").date()
            if start_date <= transaction_date <= end_date:
                product_id = row[1]
                quantity = int(row[2])
                retail_price = 0

                # Get the product's price from the current inventory
                with open(csv_file, "r") as inventory_file:
                    inventory_reader = csv.DictReader(inventory_file)
                    for inventory_row in inventory_reader:
                        if inventory_row["Product ID"] == product_id:
                            retail_price = float(inventory_row["Retail price"])
                            break
                revenue = retail_price * quantity
                profit = revenue - expenses
                dates.append(transaction_date)
                profit_list.append(revenue)
                revenue_list.append(revenue)

        # Calculate cumulative revenue and profit
        for i in range(1, len(revenue_list)):
            revenue_list[i] += revenue_list[i - 1]
            profit_list[i] += profit_list[i - 1]

        total_revenue = revenue_list[-1]
        total_profit = profit_list[-1]

        total_revenue_rounded = round(total_revenue, 2)
        total_profit_rounded = round(total_profit, 2)

        print(f"Total Revenue: {total_revenue_rounded}")
        print(f"Total Profit: {total_profit_rounded}")
        return revenue_list, profit_list, dates

    def plot_revenue_profit_line_chart(self, revenue_list, profit_list, dates):
        plt.plot(dates, revenue_list, label="Revenue")
        plt.plot(dates, profit_list, label="Profit")
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.title("Revenue and Profit Over Time")
        plt.legend()
        plt.show()


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
        # Advance date for the whole program
        self.current_date += datetime.timedelta(days=days)
        self.save_current_date()

    def reset_date(self):
        # Reset the advanced date back to the current date
        today = datetime.date.today()
        with open(self.date_file, "w") as file:
            file.write(today.strftime("%Y-%m-%d"))

        print(
            f"The date has been reset to the original current date: {today.strftime('%Y-%m-%d')}."
        )

    def get_current_date(self):
        return self.current_date


class BackupData:
    def __init__(self):
        self.backup_filename = self.get_backup_filename()

    def create_backup_directory(self):
        backup_dir = "backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

    def get_backup_filename(self):
        backup_dir = "backups"
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return os.path.join(backup_dir, f"backup_{current_time}.csv")

    def backup_data(self):
        current_inventory_csv = "current_inventory.csv"
        transactions_bought_csv = "transactions_bought.csv"
        transactions_sold_csv = "transactions_sold.csv"
        backup_filename = os.path.join("backups", self.backup_filename)

        backup_filename = self.backup_filename

        # Write data to the backup file
        with open(backup_filename, "w", newline="") as backup_csv_file:
            writer = csv.writer(backup_csv_file)

            # Read data from the current inventory CSV file
            with open(current_inventory_csv, "r") as current_inventory_file:
                current_inventory_reader = csv.reader(current_inventory_file)
                current_inventory_data = list(current_inventory_reader)

                writer.writerow(["Current Inventory Data"])
                writer.writerows(current_inventory_data)

                # Add a separator between different data sections
                writer.writerow([])

            # Read data from the transactions_bought CSV file
            with open(transactions_bought_csv, "r") as transactions_bought_file:
                transactions_bought_reader = csv.reader(transactions_bought_file)
                transactions_bought_data = list(transactions_bought_reader)

                writer.writerow(["Buying Transactions Data"])
                writer.writerows(transactions_bought_data)

                # Add a separator between different data sections
                writer.writerow([])

            # Read data from the transactions_sold CSV file
            with open(transactions_sold_csv, "r") as transactions_sold_file:
                transactions_sold_reader = csv.reader(transactions_sold_file)
                transactions_sold_data = list(transactions_sold_reader)

                writer.writerow(["Sale Transactions Data"])
                writer.writerows(transactions_sold_data)

        print("Backup complete.")

    def restore_data(self):
        backup_filename = input("Enter name of backup to be restored:")

        try:
            backup_file_path = os.path.join("backups", backup_filename)

            # Read the data from the backup CSV file and restore it
            with open(backup_file_path, "r", newline="") as backup_file:
                reader = csv.reader(backup_file)

                current_inventory_data = []
                transactions_bought_data = []
                transactions_sold_data = []
                current_section = None

                for row in reader:
                    if not row:  # Skip data section separator lines
                        continue

                    if row[0] == "Current Inventory Data":
                        current_section = "current_inventory"
                        continue
                    elif row[0] == "Buying Transactions Data":
                        current_section = "transactions_bought"
                        continue
                    elif row[0] == "Sale Transactions Data":
                        current_section = "transactions_sold"
                        continue

                    if current_section == "current_inventory":
                        current_inventory_data.append(row)
                    elif current_section == "transactions_bought":
                        transactions_bought_data.append(row)
                    elif current_section == "transactions_sold":
                        transactions_sold_data.append(row)

            # Write data back to their respective files
            current_inventory_csv = "current_inventory.csv"
            transactions_bought_csv = "transactions_bought.csv"
            transactions_sold_csv = "transactions_sold.csv"

            with open(current_inventory_csv, "w", newline="") as current_inventory_file:
                writer = csv.writer(current_inventory_file)
                writer.writerows(current_inventory_data)

            with open(
                transactions_bought_csv, "w", newline=""
            ) as transactions_bought_file:
                writer = csv.writer(transactions_bought_file)
                writer.writerows(transactions_bought_data)

            with open(transactions_sold_csv, "w", newline="") as transactions_sold_file:
                writer = csv.writer(transactions_sold_file)
                writer.writerows(transactions_sold_data)

            print("Data restored.")
        except FileNotFoundError:
            print("Backup file not found.")


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
            "update_inventory_entry",
            "delete_inventory_entry",
            "generate_manager_id",
            "advance",
            "reset_date",
            "record_transaction_bought",
            "record_transaction_sold",
            "report_profit",
            "print_product_details",
            "backup_data",
            "restore_data",
        ],
        help=(
            "Specify commands: add_new product, print current inventory, print expiring products, "
            " print low inventory, print expired products, print transactions sold, print transactions bought, "
            "update inventory entry, delete inventory entry, generate manager id, advance date, reset_date, "
            "record transaction bought, record transaction sold, report profit, print product details, "
            "backup data, restore data"
        ),
    )

    parser.add_argument(
        "--advance",
        type=int,
        help="Number of days to advance the current date",
    )
    parser.add_argument(
        "--reset_date",
        action="store_true",
        help="Reset the advanced date back to the current date",
    )
    parser.add_argument(
        "days",
        type=int,
        nargs="?",
        default=0,
        help="Number of days to advance (or reset_date to reset)",
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
        "--update_inventory_entry",
        action="store_true",
        help="Print the updated inventory",
    )
    parser.add_argument(
        "--delete_inventory_entry",
        action="store_true",
        help="Delete a whole inventory entry",
    )
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
    parser.add_argument(
        "--backup_data",
        action="store_true",
        help="Back up all data in current_inventory.csv, transactions_bought.csv and transactions_sold.csv",
    )
    parser.add_argument(
        "--restore_data",
        action="store_true",
        help="Restore data from the back up CSV file",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()
    # Create a DateManager object to manage the current date used throughout the whole program
    date_manager = DateManager("current_date.txt")

    inventory = Inventory(args.current_inventory_csv)

    transactions = Transactions(
        args.current_inventory_csv,
        args.transactions_bought,
        args.transactions_sold,
        date_manager.get_current_date(),
    )

    report_creation = ReportCreation(
        args.expiring_products_csv,
        args.low_inventory_csv,
        date_manager.get_current_date(),
    )

    personel = Personel("manager_id.csv")
    backup_data_manager = BackupData()
    backup_data_manager.create_backup_directory()

    if args.command == "advance":
        date_manager.advance_time(args.days)
        print(
            f"The date in {args.days} days will be {date_manager.get_current_date()}. Program now operates with this date. Use command reset_date to return to current date."
        )

    elif args.command == "reset_date":
        date_manager.reset_date()
    elif args.command == "add_new_product":
        inventory.add_product_to_inventory()
    elif args.command == "print_current_inventory":
        inventory.print_current_inventory()
    elif args.command == "update_inventory_entry":
        inventory.update_inventory_entry()
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
        revenue_list, profit_list, dates = report_creation.report_revenue_profit()
        report_creation.plot_revenue_profit_line_chart(revenue_list, profit_list, dates)
    elif args.command == "print_product_details":
        inventory.print_product_by_id()
    elif args.command == "backup_data":
        backup_data_manager.backup_data()
    elif args.command == "restore_data":
        backup_data_manager.restore_data()


if __name__ == "__main__":
    main()
