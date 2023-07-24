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
                if row["Product ID"] == product_id:
                    current_quantity = int(row["Quantity in stock"])
                    new_quantity = current_quantity + quantity_bought
                    row["Quantity in stock"] = str(new_quantity)
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


    parser.add_argument(
    "--update_stock",
    action="store_true",
    help="Update stock quantity in current inventory",
)