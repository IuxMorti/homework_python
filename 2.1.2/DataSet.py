import csv
from Vacancy import Vacancy


class DataSet:
    def __init__(self, file: str):
        self.file_name = file

    def csv_reader(self):
        with open(self.file_name, encoding='utf-8-sig') as r_file:
            file_reader = csv.reader(r_file, delimiter=",")
            for row in file_reader:
                yield row

    def csv_filer(self):
        reader = self.csv_reader()
        columns = next(reader)
        for row in reader:
            if len(row) != len(columns) or "" in row:
                continue
            yield Vacancy.parse_from_csv_row(dict(zip(columns, row)))