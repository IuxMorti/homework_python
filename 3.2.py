import csv
import re

ru_name = {"name": "Название",
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
           "published_at": "Дата и время публикации вакансии"}

ru_currency = {"AZN": "Манаты",
               "BYR": "Белорусские рубли",
               "EUR": "Евро",
               "GEL": "Грузинский лари",
               "KGS": "Киргизский сом",
               "KZT": "Тенге",
               "RUR": "Рубли",
               "UAH": "Гривны",
               "USD": "Доллары",
               "UZS": "Узбекский сум"}

ru_value = {"False": "Нет", "True": "Да",
            "noExperience": "Нет опыта",
            "between1And3": "От 1 года до 3 лет",
            "between3And6": "От 3 до 6 лет",
            "moreThan6": "Более 6 лет"}


def strip_tags(string: str) -> str:
    clean = re.compile("<.*?>")
    return ' '.join(re.sub(clean, "", string).split())


def csv_reader(file_name):
    columns = []
    rows = []
    with open(file_name, encoding='utf-8-sig') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        is_first = True
        for row in file_reader:
            if is_first:
                columns = row
                is_first = False
            else:
                rows.append(row)
    return columns, rows


def csv_filer(rows, columns) -> list:
    result = []
    for row in rows:
        if len(row) != len(columns) or "" in row:
            continue

        parse_row = dict()
        for index, name in enumerate(columns):
            values = row[index].split('\n')
            parse_row[name] = list(map(strip_tags, values))
        result.append(parse_row)
    return result


def print_vacancies(data_vacancies, dic_naming):
    for vacancy in data_vacancies:
        for name, value in formatter(vacancy, dic_naming).items():
            if name not in dic_naming:
                print(f'{name}: {value}')
        print()


def formatter(vacancy: dict, dic_naming) -> dict:
    result = dict()
    is_salary = False
    for name, value in vacancy.items():
        if not is_salary and name.startswith("salary"):
            salary = formatter_salary(vacancy)
            result[dic_naming[salary[0]]] = salary[1]
            is_salary = True
        elif is_salary and name.startswith("salary"):
            continue
        elif name == "published_at":
            date = reversed(value[0].split('T')[0].split('-'))
            result["Дата публикации вакансии"] = '.'.join(date)
        elif name not in dic_naming:
            result[name] = ", ".join(map(parse_value, value))
        else:
            result[dic_naming[name]] = ", ".join(map(parse_value, value))

    return result


def formatter_salary(vacancy: dict) -> tuple:
    gross = {"True": "Без вычета налогов", "False": "С вычетом налогов"}
    salary_from = '{:,}'.format(int(float(vacancy["salary_from"][0]))).replace(',', ' ')
    salary_to = '{:,}'.format(int(float(vacancy["salary_to"][0]))).replace(',', ' ')
    salary_currency = ru_currency[vacancy["salary_currency"][0]]
    salary_gross = gross[vacancy["salary_gross"][0]]

    return "salary", f"{salary_from} - {salary_to} ({salary_currency}) ({salary_gross})"


def parse_value(value: str):
    if value in ru_value:
        return ru_value[value]
    return value


reader = csv_reader(input())

print_vacancies(csv_filer(reader[1], reader[0]), ru_name)
