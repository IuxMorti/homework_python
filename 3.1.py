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
           "area_name": "Название региона",
           "published_at": "Дата и время публикации вакансии"}


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
        for name, value in vacancy.items():
            if name not in dic_naming:
                print(f'{name}: {", ".join(map(parse_value,value))}')
            else:
                print(f'{dic_naming[name]}: {", ".join(map(parse_value,value))}')
        print()


def parse_value(value: str):
    d = {"False": "Нет", "True": "Да"}
    if value in d:
        return d[value]
    return value


reader = csv_reader(input())

print_vacancies(csv_filer(reader[1], reader[0]), ru_name)
