import csv
import re
import prettytable

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


def formatter(vacancy: dict, dic_naming: dict) -> dict:
    result = dict()
    salary_is_recorded = False
    for name, value in vacancy.items():
        if not salary_is_recorded and name.startswith("salary"):
            salary = formatter_salary(vacancy)
            result[dic_naming[salary[0]]] = salary[1]
            salary_is_recorded = True
        elif salary_is_recorded and name.startswith("salary"):
            continue
        elif name == "published_at":
            date = reversed(value[0].split('T')[0].split('-'))
            result["Дата публикации вакансии"] = '.'.join(date)
        elif name == "key_skills":
            result[dic_naming[name]] = '\n'.join(value)
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
    salary_gross = gross[vacancy["salary_gross"][0].lower().capitalize()]
    return "salary", f"{salary_from} - {salary_to} ({salary_currency}) ({salary_gross})"


def parse_value(value: str):
    if value in ru_value:
        return ru_value[value]
    return value


def cuter(arr: list) -> list:
    result = []

    for string in arr:
        if len(string) > 100:
            result.append(string[:100] + "...")
        else:
            result.append(string)
    return result


my_table = prettytable.PrettyTable()

reader = csv_reader(input())

if len(reader[0]) == len(reader[1]) == 0:
    print("Пустой файл")
elif len(reader[1]) == 0:
    print("Нет данных")
else:
    a = list(map(lambda d: formatter(d, ru_name), csv_filer(reader[1], reader[0])))
    my_table.field_names = ['№'] + list(a[0].keys())
    my_table.max_width = 20
    my_table.add_rows(map(lambda tup: [tup[0] + 1] + tup[1],
                          enumerate(map(lambda value: cuter(value),
                                        map(lambda d: list(d.values()), a)))))
    my_table.hrules = prettytable.ALL
    my_table.align = 'l'

    print(my_table)
