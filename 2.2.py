import csv
import re


def strip_tags(string: str):
    clean = re.compile("<.*?>")
    return ' '.join(re.sub(clean, "", string).split())


column = []
vacancies = []
file_name = input()

with open(file_name, encoding='utf-8-sig') as r_file:
    file_reader = csv.reader(r_file, delimiter=",")
    is_first = True
    for row in file_reader:
        if is_first:
            column = row
            is_first = False
            continue

        if len(row) != len(column) or "" in row:
            continue

        d = {column[i]: list(map(strip_tags, row[i].split('\n'))) for i in range(len(column))}
        vacancies.append(d)

for vacancy in vacancies:
    for name_column, value in vacancy.items():
        print(f"{name_column}: {', '.join(value)}")
    print()
