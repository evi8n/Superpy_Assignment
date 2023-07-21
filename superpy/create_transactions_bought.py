import csv


def create_transactions_bought_csv(file_path):
    fieldnames = [
        "Transaction ID",
        "Product ID",
        "Quantity",
        "Date",
    ]
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(fieldnames)


transactions_bought_file_path = "transactions_bought.csv"
create_transactions_bought_csv(transactions_bought_file_path)
