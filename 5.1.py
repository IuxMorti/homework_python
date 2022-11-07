import csv
import re

from var_dump import var_dump


class DataSet:
    def __init__(self, file_name, vacancies_objects):
        self.file_name = file_name
        self.vacancies_objects = vacancies_objects


class Vacancy:
    def __init__(self, name: str, description: str, key_skills: list, experience_id: str, premium: str,
                 employer_name: str, salary: object, area_name: str, published_at: str):
        self.name = name
        self.description = description
        self.key_skills = key_skills
        self.experience_id = experience_id
        self.premium = premium
        self.employer_name = employer_name
        self.salary = salary
        self.area_name = area_name
        self.published_at = published_at

    @staticmethod
    def parse_from_row_csv(row):
        name = strip_tags(row[0])
        description = strip_tags(row[1])
        key_skills = list(map(strip_tags, row[2].split('\n')))
        experience_id = strip_tags(row[3])
        premium = strip_tags(row[4])
        employer_name = strip_tags(row[5])
        salary = Salary(row[6], row[7], row[8], row[9])
        area_name = strip_tags(row[10])
        published_at = strip_tags(row[11])
        return Vacancy(name, description, key_skills, experience_id, premium, employer_name,
                       salary, area_name, published_at)


class Salary:
    def __init__(self, salary_from, salary_to, salary_gross, salary_currency):
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency


def strip_tags(string: str) -> str:
    return ' '.join(re.sub(re.compile("<.*?>"), "", string).split())


def csv_reader(file_name):
    with open(file_name, encoding='utf-8-sig') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        for row in file_reader:
            yield row


def csv_filer(rows, columns):
    for row in rows:
        if len(row) != len(columns) or "" in row:
            continue
        yield Vacancy.parse_from_row_csv(row)


def validate_reader(reader):
    counter = 0
    for row in reader:
        yield row
        counter += 1

    if counter == 0:
        print("Пустой файл")
        exit(0)


csv_file_name = input("Введите название файла: ")
filter_key = input("Введите параметр фильтрации: ")
sort_key = input("Введите параметр сортировки: ")
is_reverse_sorting = input("Обратный порядок сортировки (Да / Нет): ")
inp_bounds = input("Введите диапазон вывода: ")
list_columns = input("Введите требуемые столбцы: ")

reader_ = validate_reader(csv_reader(csv_file_name))

var_dump(DataSet(csv_file_name, [v for v in csv_filer(reader_, next(reader_))]))
