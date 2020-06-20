import csv
import sys


def write_csv(file, data):
    with open(file + ".csv", "w", newline="") as csv_file:

        header = data[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=header)

        try:
            writer.writeheader()
            writer.writerows(data)
        except csv.Error as e:
            sys.exit(f"CSV Error: {e}")
