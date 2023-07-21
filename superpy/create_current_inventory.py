import csv

# Specify the fieldnames
fieldnames = [
    "ID",
    "Name",
    "In stock",
    "Buy price",
    "Restock date",
    "Bought for restock",
    "Sell price",
    "Sold since restock",
    "Expiration date",
]

# Specify what the file will be called
file_path = "current_inventory.csv"

# Write the data to the csv file
with open(file_path, "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Write header row
    writer.writeheader()

    # Write the data rows
    for product in products:
        writer.writerow(product)
