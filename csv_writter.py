import csv

def write_csv(file, data):
    with open(file, "w", newline="") as csv_file:

        header = data[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()

        writer.writerows(data)

# f = open("sample.csv", "w")
# writer = csv.DictWriter(
#     f, fieldnames=["fruit", "count"])
# writer.writeheader()
# writer.writerow({"fruit": "apple", "count": "1"})
# writer.writerow({"fruit": "banana", "count": "2"})


# writer.writerows(
#     [{"fruit": "apple", "count": "1"},
#     {"fruit": "banana", "count": "2"}])
# f.close()
# Output
# sample.csv
# fruit,count
# apple,1
# banana,2

