import csv
import datetime
import re
from dataclasses import dataclass
import prettytable


class RuNames:

    @staticmethod
    def en_ru_names():
        return {
            "": "",
            "name": "Название",
            "description": "Описание",
            "key_skills": "Навыки",
            "experience_id": "Опыт работы",
            "premium": "Премиум-вакансия",
            "employer_name": "Компания",
            "salary_from": "Нижняя граница вилки оклада",
            "salary_to": "Верхняя граница вилки оклада",
            "salary_gross": "Оклад указан до вычета налогов",
            "salary_currency": "Идентификатор валюты оклада",
            "salary": "Оклад",
            "area_name": "Название региона",
            "published_at": "Дата и время публикации вакансии",
            "published date": "Дата публикации вакансии"
        }

    @staticmethod
    def en_ru_currency():
        return {
            "AZN": "Манаты",
            "BYR": "Белорусские рубли",
            "EUR": "Евро",
            "GEL": "Грузинский лари",
            "KGS": "Киргизский сом",
            "KZT": "Тенге",
            "RUR": "Рубли",
            "UAH": "Гривны",
            "USD": "Доллары",
            "UZS": "Узбекский сум"}

    @staticmethod
    def en_ru_gross():
        return {"True": "Без вычета налогов", "False": "С вычетом налогов"}

    @staticmethod
    def en_ru_value() -> dict:
        return {
            "": "",
            "False": "Нет",
            "True": "Да",
            "noExperience": "Нет опыта",
            "between1And3": "От 1 года до 3 лет",
            "between3And6": "От 3 до 6 лет",
            "moreThan6": "Более 6 лет"
        }

    @staticmethod
    def ru_en_names():
        return dict(zip(RuNames.en_ru_names().values(), RuNames.en_ru_names().keys()))

    @staticmethod
    def ru_en_values():
        return dict(zip(RuNames.en_ru_value().values(), RuNames.en_ru_value().keys()))

    @staticmethod
    def ru_en_currency():
        return dict(zip(RuNames.en_ru_currency().values(), RuNames.en_ru_currency().keys()))


sort_key_experience = {
    "noExperience": 1,
    "between1And3": 2,
    "between3And6": 3,
    "moreThan6": 4,
}

filter_keys = {
    "": "",
    "name": lambda name: lambda vacancy: name == vacancy.name,
    "description": lambda name: lambda vacancy: name == vacancy.description,
    "key_skills": lambda skill: lambda vacancy: skill in vacancy.key_skills,
    "experience_id": lambda experience: lambda vacancy: experience == vacancy.experience_id,
    "premium": lambda premium: lambda vacancy: premium.lower() == vacancy.premium.lower(),
    "employer_name": lambda name: lambda vacancy: name == vacancy.employer_name,
    "salary_from": lambda salary: lambda vacancy: float(salary) >= float(vacancy.salary.salary_from),
    "salary_to": lambda salary: lambda vacancy: float(salary) <= float(vacancy.salary.salary_to),
    "salary_gross": lambda gross: lambda vacancy: gross == vacancy.salary.salary_gross,
    "salary_currency": lambda currency: lambda vacancy: currency == vacancy.salary.salary_currency,
    "area_name": lambda name: lambda vacancy: name == vacancy.area_name,
    "published date": lambda date: lambda vacancy: parse_date(date).date() == parse_date(vacancy.published_at).date(),
    "salary": lambda salary:
    lambda vacancy: float(vacancy.salary.salary_from) <= float(salary) <= float(vacancy.salary.salary_to),
}

sort_keys = {
    "": "",
    "name": lambda vacancy: vacancy["name"],
    "description": lambda vacancy: vacancy["description"],
    "key_skills": lambda vacancy: len(vacancy["key_skills"]),
    "experience_id": lambda vacancy: sort_key_experience[vacancy["experience_id"]],
    "premium": lambda vacancy: vacancy["premium"],
    "employer_name": lambda vacancy: vacancy["employer_name"],
    "salary_gross": lambda vacancy: vacancy["salary_gross"],
    "salary_currency": lambda vacancy: vacancy["salary_currency"],
    "area_name": lambda vacancy: vacancy["area_name"],
    "published date": lambda vacancy: parse_date(vacancy["published_at"]),
    "salary": lambda vacancy: vacancy.salary.avg_salary * Salary.currency_to_rub()[vacancy.salary.salary_currency]
}


class DataSet:
    def __init__(self, file_name, filter_key, filter_value, sort_key, reverse, validator_reader=None):
        self.filter_value = filter_value
        self.validator_reader = validator_reader
        self.reverse = reverse
        self.sort_key = sort_key
        self.filter_key = filter_key
        self.file_name = file_name

    def filter_vacancy(self, list_vacancies):
        if self.filter_key == "" or len(self.filter_value) == 0:
            return list_vacancies
        result = list_vacancies
        for value in self.filter_value:
            result = list(filter(filter_keys[self.filter_key](value), result))
        return result

    def sort_vacancies(self, list_vacancies):
        if self.sort_key == "":
            return list_vacancies
        return sorted(list_vacancies, key=sort_keys[self.sort_key], reverse=self.reverse)

    def csv_reader(self):
        with open(self.file_name, encoding='utf-8-sig') as r_file:
            file_reader = csv.reader(r_file, delimiter=",")
            for row in file_reader:
                yield row

    def csv_filer(self, rows, columns):
        for row in rows:
            if len(row) != len(columns) or "" in row:
                continue
            yield Vacancy.parse_from_csv_row(row)

    def formatter(self, vacancy):
        result = []
        for column in Vacancy.all_columns():
            if column == "published at":
                result.append(formatter_date(parse_date(vacancy.published_at)))
            elif column == "key_skills":
                result.append('\n'.join(vacancy.key_skills))
            else:
                result.append(RuNames.en_ru_value()[str(vacancy[column])]
                              if str(vacancy[column]) in RuNames.en_ru_value()
                              else str(vacancy[column]))
        return result

    def formatter_vacancies(self, vacancies):
        result = map(lambda vacancy: self.formatter(vacancy), vacancies)
        return list(map(lambda tup: [tup[0] + 1] + tup[1],
                        enumerate(
                            map(lambda value: cuter_list(value), result))))

    def get_list_field_vacancies(self):
        reader = self.validator_reader(self.csv_reader()
                                       if self.validator_reader is not None
                                       else self.csv_reader())

        return self.formatter_vacancies(
            self.sort_vacancies(
                self.filter_vacancy(
                    self.csv_filer(reader, next(reader))
                )))


def cuter(string: str) -> str:
    return string[:100] + ('' if len(string) < 100 else '...')


def cuter_list(arr: list) -> list:
    return [cuter(string) for string in arr]


@dataclass
class Vacancy:
    name: str
    description: str
    key_skills: list
    experience_id: str
    premium: str
    employer_name: str
    salary: object
    area_name: str
    published_at: str

    @staticmethod
    def all_columns():
        return ["name", "description", "key_skills", "experience_id",
                "premium", "employer_name", "salary", "area_name", "published at"]

    @staticmethod
    def parse_from_csv_row(row):
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

    def __getitem__(self, item):
        if item == 'name':
            return self.name
        if item == 'description':
            return self.description
        if item == 'key_skills':
            return self.key_skills
        if item == 'experience_id':
            return self.experience_id
        if item == 'premium':
            return self.premium
        if item == 'employer_name':
            return self.employer_name
        if item == 'salary':
            return self.salary
        if item == 'area_name':
            return self.area_name
        if item == 'published_at':
            return self.published_at


@dataclass
class Salary:
    salary_from: str
    salary_to: str
    salary_gross: str
    salary_currency: str

    @staticmethod
    def currency_to_rub():
        return {
            "": "",
            "AZN": 35.68,
            "BYR": 23.91,
            "EUR": 59.90,
            "GEL": 21.74,
            "KGS": 0.76,
            "KZT": 0.13,
            "RUR": 1,
            "UAH": 1.64,
            "USD": 60.66,
            "UZS": 0.0055,
        }

    @property
    def avg_salary(self):
        return (float(self.salary_from) + float(self.salary_to)) / 2

    # в целом, чтобы поддерживать не только русский язык, можно будет добавить поле с языком и обращаться к его полям
    # но пока пусть так будет

    def __str__(self):
        salary_from = '{:,}'.format(int(float(self.salary_from))).replace(',', ' ')
        salary_to = '{:,}'.format(int(float(self.salary_to))).replace(',', ' ')
        salary_currency = RuNames.en_ru_currency()[self.salary_currency]
        salary_gross = RuNames.en_ru_gross()[self.salary_gross.capitalize()]
        return f"{salary_from} - {salary_to} ({salary_currency}) ({salary_gross})"

    def __lt__(self, other):
        return self.avg_salary < other.avg_salary

    def __gt__(self, other):
        return self.avg_salary > other.avg_salary

    def __eq__(self, other):
        return abs(self.avg_salary - other.avg_salary) < 1e-6


"""*****************************************************************************************************************"""


class InputConnect:

    def all_columns(self):
        return ['№'] + ["name", "description", "key_skills", "experience_id",
                        "premium", "employer_name", "salary", "area_name", "published date"]

    def __init__(self, file_name: str, filter_key: str, sort_key: str, reverse: str, bounds: str, columns: str):
        self.file_name = file_name
        self.columns = InputConnect.validate_required_columns(columns)
        self.bounds = tuple(map(int, bounds.split()))
        self.reverse = InputConnect.validate_reverse(reverse)
        self.sort_key = InputConnect.validate_sort_key(sort_key)
        self.filter_key, self.filter_value = InputConnect.validate_filter_keys(filter_key)

    @staticmethod
    def validate_filter_keys(keys: str):
        if keys == "":
            return "", ""
        result = list(map(str.strip, keys.split(':')))
        if len(result) != 2:
            print("Формат ввода некорректен")
            exit(0)
        if result[0] not in RuNames.ru_en_names():
            print("Параметр поиска некорректен")
            exit(0)
        key, value = result
        value = list(map(str.strip, value.split(',')))

        if len(value) == 1 and value[0] in RuNames.ru_en_values():
            value[0] = RuNames.ru_en_values()[value[0]]
        if len(value) == 1 and value[0] in RuNames.ru_en_currency():
            value[0] = RuNames.ru_en_currency()[value[0]]

        return RuNames.ru_en_names()[key], value

    @staticmethod
    def validate_sort_key(sorted_name):
        if sorted_name not in RuNames.ru_en_names():
            print("Параметр сортировки некорректен")
            exit(0)

        return RuNames.ru_en_names()[sorted_name]

    @staticmethod
    def validate_reverse(sort_is_reverse):
        if (sort_is_reverse not in RuNames.ru_en_values()
                or sort_is_reverse != "" and not is_bool(RuNames.ru_en_values()[sort_is_reverse])):
            print("Порядок сортировки задан некорректно")
            exit(0)
        return parse_bool(RuNames.ru_en_values()[sort_is_reverse])

    @staticmethod
    def validate_required_columns(columns):
        result = list(filter(lambda string: len(string) != 0, map(str.strip, columns.split(','))))
        return ['№'] + result if len(result) > 0 else result

    @staticmethod
    def validate_reader(reader):
        counter = 0
        for row in reader:
            yield row
            counter += 1

        if counter == 0:
            print("Пустой файл")
            exit(0)
        elif counter == 1:
            print("Нет данных")
            exit(0)

    def print(self):
        data_set = DataSet(self.file_name, self.filter_key, self.filter_value,
                           self.sort_key, self.reverse, self.validate_reader)

        Table.print_table(map(lambda c: c if c not in RuNames.en_ru_names() else RuNames.en_ru_names()[c],
                              self.all_columns()),
                          self.columns,
                          data_set.get_list_field_vacancies(),
                          self.bounds)


class Table:

    @staticmethod
    def print_table(columns, required_field, rows, bounds):
        my_table = prettytable.PrettyTable()
        for row in rows:
            my_table.add_row(row)

        if len(my_table.rows) == 0:
            print("Ничего не найдено")
            return

        my_table.field_names = columns
        my_table.max_width = 20
        my_table.hrules = prettytable.ALL
        my_table.align = 'l'
        if len(bounds) == 0:
            print(my_table.get_string(fields=required_field))
        elif len(bounds) == 1:
            print(my_table.get_string(fields=required_field, start=bounds[0] - 1))
        elif len(bounds) == 2:
            print(my_table.get_string(fields=required_field, start=bounds[0] - 1, end=bounds[1] - 1))


def parse_date(date: str):
    if '-' in date:
        return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
    return datetime.datetime.strptime(date, "%d.%m.%Y")


def formatter_date(date):
    return '.'.join(reversed(str(date.date()).split('-')))


def is_bool(string: str) -> bool:
    return string == "True" or string == "False"


def parse_bool(string: str) -> bool:
    return string == "True"


def validate_reader(reader):
    counter = 0
    for row in reader:
        yield row
        counter += 1

    if counter == 0:
        print("Пустой файл")
        exit(0)
    elif counter == 1:
        print("Нет данных")
        exit(0)


def strip_tags(string: str) -> str:
    return ' '.join(re.sub(re.compile("<.*?>"), "", string).split())


"""*****************************************************************************************************************"""

csv_file_name = input("Введите название файла: ").strip()
filter_k = input("Введите параметр фильтрации: ").strip()
sort_k = input("Введите параметр сортировки: ").strip()
is_reverse_sorting = input("Обратный порядок сортировки (Да / Нет): ").strip()
inp_bounds = input("Введите диапазон вывода: ").strip()
list_columns = input("Введите требуемые столбцы: ").strip()

InputConnect(csv_file_name, filter_k, sort_k, is_reverse_sorting, inp_bounds, list_columns).print()

"""
vacancies.csv  
Опыт работы: От 3 до 6 лет  
Опыт работы  
Нет  
10 20  
Название, Навыки, Опыт работы, Компания
"""
