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
import argcomplete


# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.


class ProductDetails:
    def __init__(self):
        pass

    def print_product_by_id(self):
        # Print product details read from the "current_inventory" CSV file based on product ID
        csv_file = "current_inventory.csv"
        product_id = input("Enter product ID:")
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


class Personel:
    def __init__(self, manager_id_csv):
        self.manager_id_csv = manager_id_csv
        self.manager_id = None

    # Generate a new manager ID consisting of 6 random digits, save it in the "manager_id" CSV file and record the current date
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
        # Read the "current_inventory" CSV file and print its contents in the form of a table
        csv_file = "current_inventory.csv"
        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            data = [list(row.values()) for row in reader]
        print("Current Inventory:")
        inventory_table = tabulate(data, fieldnames, tablefmt="grid")
        print(inventory_table)

    def add_product_to_inventory(self):
        # Open "current_inventory" CSV file, input details of new product and append it
        csv_file = "current_inventory.csv"
        new_product = {}

        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames

            # Check if product ID is inputted in the correct format (otherwise print feedback),
            # and give user the option of exiting without making changes
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

                new_product["Product ID"] = user_input_id

                new_product_name = str(input("Enter product name:"))
                new_product["Product Name"] = new_product_name

                # Check that Cost price is inputted in the correct format (otherwise print feedback)
                while True:
                    buy_price = input("Enter buy price:")
                    try:
                        buy_price = float(buy_price)
                        if buy_price != 0.0:
                            new_product["Cost price"] = buy_price
                            break
                        else:
                            print("Buy price cannot be zero.")
                    except ValueError:
                        print("Invalid input. Buy price must be a positive float.")

                # Check that Retail price and quantity is inputted in the correct format (otherwise print feedback)
                while True:
                    sell_price = input("Enter sell price:")
                    try:
                        sell_price = float(sell_price)
                        if sell_price != 0.0:
                            new_product["Cost price"] = sell_price
                            break
                        else:
                            print("Sell price cannot be zero.")
                    except ValueError:
                        print("Invalid input. Sell price must be a positive float.")

                quantity = input("Enter quantity:")
                if not quantity.isdigit() or int(quantity) == 0:
                    print("Invalid input. Quantity must be a positive number.")
                    continue

                # Update the rest of the fields automatically

                # Set restock date to current date
                new_product["Restock date"] = datetime.date.today().isoformat()
                # Set the "Sold since restock" value to 0
                new_product["Sold since restock"] = 0
                new_product["Quantity bought for restock"] = quantity
                new_product["Quantity in stock"] = quantity

                # Define different behaviour if the new product's ID starts with FP (Food Product) or NF (Non-Food),
                # so that the user is only required to input an expiration date for Food Products
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
        # Update any field of an existing product in the "current_inventory" CSV file
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

        # Check if there are multiple entries with the same product ID,
        # and if there are (e.g multiple entries of the same product but with different expiration dates)
        # specify which entry is to be deleted by expiration date
        matching_entries = []
        with open(csv_file, "r") as input_file:
            reader = csv.DictReader(input_file)
            for row in reader:
                if row["Product ID"] == product_id:
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

        # Ask for confirmation before deletion by asking for the manager's ID
        manager_id = input("Enter manager's ID for confirmation:")
        id_of_manager = Personel.generate_manager_id()
        if manager_id != id_of_manager:
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
        print(
            f"Product with ID {product_id} and expiration date {expiration_date} was deleted from inventory."
        )


class Transactions:
    def __init__(self, csv_file, transactions_bought, transactions_sold, date_manager):
        self.csv_file = csv_file
        self.transactions_bought = transactions_bought
        self.transactions_sold = transactions_sold
        self.date_manager = date_manager

    def record_transaction_bought(self):
        # Record an inventory purchase transaction by inputting a product ID
        # update the quantity currently in stock for selected product
        csv_file = "current_inventory.csv"
        transactions_bought_file = "transactions_bought.csv"
        new_transaction = {}

        # Check if product ID is inputted in the correct format (otherwise print feedback),
        # and give user the option of exiting without making changes
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

            new_transaction["Product ID"] = user_input_id

            # Check that the quantity is inputted in the correct format (otherwise print feedback)
            quantity = input("Enter quantity bought:")
            if not quantity.isdigit() or int(quantity) == 0:
                print("Invalid input. Quantity must be a positive number.")
                continue

            new_transaction["Quantity in stock"] = quantity
            # Create a unique transaction ID
            new_transaction["Transaction ID"] = str(uuid4())
            new_transaction["Restock date"] = self.date_manager

            # Check if expiration date is inputted in the correct format (otherwise print feedback)
            # Check if the expiration date of the purchased product matches possible entries with the same product ID
            expiration_date = input("Enter expiration date (YYYY-MM-DD):")
            if not re.match(r"\d{4}-\d{2}-\d{2}$", expiration_date):
                print(
                    "Invalid input. Expiration date must be in the format YYYY-MM-DD."
                )
                continue

            new_transaction["Expiration date"] = expiration_date

            product_id = new_transaction["Product ID"]
            quantity = int(new_transaction["Quantity in stock"])
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
                product["Product ID"] == product_id
                and product["Expiration date"] == expiration_date
            ):
                current_quantity = int(product["Quantity in stock"])
                new_quantity = current_quantity + int(quantity)
                product["Quantity in stock"] = str(new_quantity)
                product["Restock date"] = date
                found_product = True
                break

        if not found_product:
            print(f"No product found with ID {product_id}")
            return
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
                    "Cost price": original_product["Cost price"],
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
        # Record an inventory sale transaction by inputting a product ID
        # update the quantity currently in stock for selected product
        csv_file = "current_inventory.csv"
        transactions_sold_file = "transactions_sold.csv"
        new_transaction = {}

        # Check if product ID is inputted in the correct format (otherwise print feedback),
        # and give user the option of exiting without making changes
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

            new_transaction["Product ID"] = user_input_id

            # Check if quantity is inputted in the correct format (otherwise print feedback)
            quantity = input("Enter quantity sold:")
            if not quantity.isdigit() or int(quantity) == 0:
                print("Invalid input. Quantity must be a positive number.")
                continue

            new_transaction["Quantity in stock"] = quantity
            new_transaction["Transaction ID"] = str(uuid4())

            product_id = new_transaction["Product ID"]
            quantity = int(new_transaction["Quantity in stock"])
            date = self.date_manager
            transaction_id = new_transaction["Transaction ID"]

            break

        transaction_sold_data = []
        found_product = False

        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            for row in reader:
                if row["Product ID"] == product_id:
                    current_quantity = int(row["Quantity in stock"])
                    new_quantity = current_quantity - int(quantity)
                    row["Quantity in stock"] = str(new_quantity)
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

        # Read transactions_sold.csv into memory
        with open(transactions_sold, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            transactions_sold_data = list(reader)

        for row in transactions_bought_data:
            transaction_date = datetime.datetime.strptime(row[3], "%Y-%m-%d").date()
            if start_date <= transaction_date <= end_date:
                product_id = row[1]
                quantity = int(row[2])
                buy_price = 0

                # Get the product's price from the current inventory
                with open(csv_file, "r") as inventory_file:
                    inventory_reader = csv.DictReader(inventory_file)
                    for inventory_row in inventory_reader:
                        if inventory_row["Product ID"] == product_id:
                            buy_price = float(inventory_row["Cost price"])
                            break
                expenses = buy_price * quantity
                dates.append(transaction_date)
                profit_list.append(0)
                revenue_list.append(-expenses)

        for row in transactions_sold_data:
            transaction_date = datetime.datetime.strptime(row[3], "%Y-%m-%d").date()
            if start_date <= transaction_date <= end_date:
                product_id = row[1]
                quantity = int(row[2])
                sell_price = 0

                # Get the product's price from the current inventory
                with open(csv_file, "r") as inventory_file:
                    inventory_reader = csv.DictReader(inventory_file)
                    for inventory_row in inventory_reader:
                        if inventory_row["Product ID"] == product_id:
                            sell_price = float(inventory_row["Cost price"])
                            break
                revenue = sell_price * quantity
                dates.append(transaction_date)
                profit_list.append(revenue)
                revenue_list.append(revenue)

        # Calculate cumulative revenue and profit
        for i in range(1, len(revenue_list)):
            revenue_list[i] += revenue_list[i - 1]
            profit_list[i] += profit_list[i - 1]

        return revenue_list, profit_list, dates

    def plot_revenue_profit_line_chart(self, revenue_list, profit_list, dates):
        plt.plot(dates, revenue_list, label="Revenue")
        plt.plot(dates, profit_list, label="Profit")
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.title("Revenue and Profit Over Time")
        plt.legend()
        plt.show()

    def plot_revenue_profit_line_chart(self, revenue_list, profit_list, dates):
        # Plot a line chart for revenue and profit
        plt.plot(dates, revenue_list, label="Revenue", marker="o", linestyle="-")
        plt.plot(dates, profit_list, label="Profit", marker="o", linestyle="-")

        plt.title("Revenue and Profit Over Time")
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
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

    product_details = ProductDetails()
    report_creation = ReportCreation(
        args.expiring_products_csv,
        args.low_inventory_csv,
        date_manager.get_current_date(),
    )

    personel = Personel("manager_id.csv")

    if args.command == "advance":
        date_manager.advance_time(args.days)
        print(
            f"The date in {args.days} days will be {date_manager.get_current_date()}. Program now operates with this date. Use the reset_date command to return back to the current date."
        )
        return

    elif args.command == "reset_date":
        date_manager.reset_date()
        return

    elif args.command == "add_new_product":
        inventory.add_product_to_inventory()
    elif args.command == "print_current_inventory":
        inventory.print_current_inventory()
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
        revenue_list, profit_list, dates = report_creation.report_revenue_profit()
        report_creation.plot_revenue_profit_line_chart(revenue_list, profit_list, dates)
    elif args.command == "print_product_details":
        product_details.print_product_by_id()


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
            "update_inventory",
            "delete_inventory_entry",
            "generate_manager_id",
            "advance",
            "reset_date",
            "record_transaction_bought",
            "record_transaction_sold",
            "report_profit",
            "print_product_details",
        ],
        help=(
            "Specify commands: add_new product, print current inventory, print expiring products, "
            " print low inventory, print expired products, print transactions sold, print transactions bought, "
            "update inventory, delete inventory entry, generate manager id, advance date, reset_date, "
            "record transaction bought, record transaction sold, report profit, print product details"
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
        "--update_inventory", action="store_true", help="Print the updated inventory"
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

    argcomplete.autocomplete(parser)

    return parser.parse_args()


if __name__ == "__main__":
    main()
