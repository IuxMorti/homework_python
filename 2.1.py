import csv

columns = []
rows = []
file_name = input()
with open(file_name, encoding='utf-8-sig') as r_file:
    file_reader = csv.reader(r_file, delimiter=",")
    is_first = True
    for row in file_reader:
        if is_first:
            columns = row
            is_first = False
        else:
            if len(row) == len(columns) and "" not in row:
                rows.append(row)

print(columns)
print(rows)