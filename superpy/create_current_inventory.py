import csv

# Specify the fieldnames
fieldnames = [
    "Product ID",
    "Product Name",
    "Quantity in stock",
    "Cost price",
    "Restock date",
    "Quantity bought for restock",
    "Retail price",
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
