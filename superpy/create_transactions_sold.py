import csv


def create_transactions_sold_csv(file_path):
    fieldnames = [
        "Transaction ID",
        "Product ID",
        "Quantity",
        "Date",
    ]
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(fieldnames)


transactions_sold_file_path = "transactions_sold.csv"
create_transactions_sold_csv(transactions_sold_file_path)
