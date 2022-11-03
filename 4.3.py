import csv
import re
import prettytable
import datetime


class NameValue:
    def __init__(self, name: str, value: str):
        self.__name = name
        self.__value = value

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value


en_ru_names = {
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

en_ru_value = {
    "": "",
    "False": "Нет",
    "True": "Да",
    "noExperience": "Нет опыта",
    "between1And3": "От 1 года до 3 лет",
    "between3And6": "От 3 до 6 лет",
    "moreThan6": "Более 6 лет",
    "AZN": "Манаты",
    "BYR": "Белорусские рубли",
    "EUR": "Евро",
    "GEL": "Грузинский лари",
    "KGS": "Киргизский сом",
    "KZT": "Тенге",
    "RUR": "Рубли",
    "UAH": "Гривны",
    "USD": "Доллары",
    "UZS": "Узбекский сум"
}

sort_key_experience = {
    "noExperience": 1,
    "between1And3": 2,
    "between3And6": 3,
    "moreThan6": 4,
}

currency_to_rub = {
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

filter_keys = {
    "": "",
    "name": lambda name: lambda vacancy: name == vacancy["name"][0],
    "description": lambda name: lambda vacancy: name == vacancy["description"][0],
    "key_skills": lambda skill: lambda vacancy: skill in vacancy["key_skills"],
    "experience_id": lambda experience: lambda vacancy: experience == vacancy["experience_id"][0],
    "premium": lambda premium: lambda vacancy: premium == vacancy["premium"][0].capitalize(),
    "employer_name": lambda name: lambda vacancy: name == vacancy["employer_name"][0],
    "salary_from": lambda salary: lambda vacancy: float(salary) >= float(vacancy["salary_from"][0]),
    "salary_to": lambda salary: lambda vacancy: float(salary) <= float(vacancy["salary_to"][0]),
    "salary_gross": lambda gross: lambda vacancy: gross == vacancy["salary_gross"][0],
    "salary_currency": lambda currency: lambda vacancy: currency == vacancy["salary_currency"][0],
    "area_name": lambda name: lambda vacancy: name == vacancy["area_name"][0],
    "published date": lambda date:
    lambda vacancy: parse_date(date).date() == parse_date(vacancy["published_at"][0]).date(),
    "salary": lambda salary:
    lambda vacancy: float(vacancy["salary_from"][0]) <= float(salary) <= float(vacancy["salary_to"][0]),
}

sort_keys = {
    "": "",
    "name": lambda vacancy: vacancy["name"],
    "description": lambda vacancy: vacancy["description"],
    "key_skills": lambda vacancy: len(vacancy["key_skills"]),
    "experience_id": lambda vacancy: sort_key_experience[vacancy["experience_id"][0]],
    "premium": lambda vacancy: vacancy["premium"][0].capitalize(),
    "employer_name": lambda vacancy: vacancy["employer_name"][0],
    "salary_from": lambda vacancy: float(vacancy["salary_from"][0]),
    "salary_to": lambda vacancy: float(vacancy["salary_to"][0]) * currency_to_rub[vacancy["salary_currency"][0]],
    "salary_gross": lambda vacancy: vacancy["salary_gross"][0] * currency_to_rub[vacancy["salary_currency"][0]],
    "salary_currency": lambda vacancy: vacancy["salary_currency"][0] * currency_to_rub[vacancy["salary_currency"][0]],
    "area_name": lambda vacancy: vacancy["area_name"][0],
    "published date": lambda vacancy: parse_date(vacancy["published_at"][0]),
    "salary": lambda vacancy: average_salary(vacancy) * currency_to_rub[vacancy["salary_currency"][0]]
}

ru_en_names = dict(zip(en_ru_names.values(), en_ru_names.keys()))
ru_en_values = dict(zip(en_ru_value.values(), en_ru_value.keys()))


def avg_sum(*args):
    a = list(map(float, args))
    return int(sum(a)) // len(a)


def average_salary(vacancy: dict):
    return avg_sum(vacancy["salary_from"][0], vacancy["salary_to"][0])


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
        vacancy = dict()
        for index, name in enumerate(columns):
            values = row[index].split('\n')
            vacancy[name] = list(map(strip_tags, values))
        yield vacancy


def formatter(vacancy: dict, naming) -> dict:
    functions = {
        "published_at": lambda v: NameValue("published date", formatter_date(parse_date(v[0]))),
        "key_skills": lambda v: NameValue("key_skills", '\n'.join(v)),
    }
    result = dict()
    for name, value in vacancy.items():
        if name.startswith("salary") and "salary" not in result:
            s = formatter_salary(vacancy)
            result['salary'] = s
        elif name in functions:
            r = functions[name](value)
            result[r.name] = r.value
        elif name not in functions and not name.startswith("salary"):
            result[name] = ", ".join(map(parse_value, value))
    return rename_keys(result, naming)


def rename_keys(vacancy: dict, naming: dict) -> dict:
    return dict(map(lambda item: (naming[item[0]] if item[0] in naming else item[0], item[1]), vacancy.items()))


def formatter_salary(vacancy: dict) -> str:
    gross = {"True": "Без вычета налогов", "False": "С вычетом налогов"}
    salary_from = '{:,}'.format(int(float(vacancy["salary_from"][0]))).replace(',', ' ')
    salary_to = '{:,}'.format(int(float(vacancy["salary_to"][0]))).replace(',', ' ')
    salary_currency = en_ru_value[vacancy["salary_currency"][0]]
    salary_gross = gross[vacancy["salary_gross"][0].capitalize()]
    return f"{salary_from} - {salary_to} ({salary_currency}) ({salary_gross})"


def parse_date(date: str):
    if '-' in date:
        return datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
    return datetime.datetime.strptime(date, "%d.%m.%Y")


def formatter_date(date):
    return '.'.join(reversed(str(date.date()).split('-')))


def parse_value(value: str):
    if value in en_ru_value:
        return en_ru_value[value]
    return value


def cuter(string: str) -> str:
    return string[:100] + ('' if len(string) < 100 else '...')


def cuter_list(arr: list) -> list:
    return [cuter(string) for string in arr]


def filter_vacancy(name_key, list_vacancies, *values):
    if name_key == "" or len(values) == 0:
        return list_vacancies
    result = list_vacancies
    for value in values:
        result = list(filter(filter_keys[name_key](value), result))
    return result


def sort_vacancies(name_key, list_vacancies, reverse=False):
    if name_key == "":
        return list_vacancies
    return sorted(list_vacancies, key=sort_keys[name_key], reverse=reverse)


def print_table(columns, required_field, rows, *bounds):
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


def validate_filter_keys(keys: str):
    if keys == "":
        return "", ""
    result = list(map(str.strip, keys.split(':')))
    if len(result) != 2:
        print("Формат ввода некорректен")
        exit(0)
    if result[0] not in ru_en_names:
        print("Параметр поиска некорректен")
        exit(0)
    key, value = result
    value = list(map(str.strip, value.split(',')))

    if len(value) == 1 and value[0] in ru_en_values:
        value[0] = ru_en_values[value[0]]

    return ru_en_names[key], value


def validate_sort_keys(sorted_name, reverse_sorted):
    if sorted_name not in ru_en_names:
        print("Параметр сортировки некорректен")
        exit(0)
    if reverse_sorted not in ru_en_values or reverse_sorted != "" and not is_bool(ru_en_values[reverse_sorted]):
        print("Порядок сортировки задан некорректно")
        exit(0)

    return ru_en_names[sorted_name], parse_bool(ru_en_values[reverse_sorted])


def validate_required_columns(columns):
    result = list(filter(lambda string: len(string) != 0, map(str.strip, columns.split(','))))
    return ['№'] + result if len(result) > 0 else result


def formatter_vacancies(vacancies):
    result = map(lambda vacancy: formatter(vacancy, en_ru_names), vacancies)
    return map(lambda tup: [tup[0] + 1] + tup[1],
               enumerate(
                   map(lambda value: cuter_list(value),
                       map(lambda vacancy: vacancy.values(), result))))


"""*****************************************************************************************************************"""

csv_file_name = input("Введите название файла: ")
filter_key = input("Введите параметр фильтрации: ")
sort_key = input("Введите параметр сортировки: ")
is_reverse_sorting = input("Обратный порядок сортировки (Да / Нет): ")
inp_bounds = input("Введите диапазон вывода: ")
list_columns = input("Введите требуемые столбцы: ")

reader_ = validate_reader(csv_reader(csv_file_name))
filter_name_key, filter_values = validate_filter_keys(filter_key)
sort_name_key, is_reverse_sorting = validate_sort_keys(sort_key, is_reverse_sorting)

bound = list(map(int, inp_bounds.split()))

required_columns = validate_required_columns(list_columns)

vacancies_from_csv = csv_filer(reader_, next(reader_))

sorted_vacancies = sort_vacancies(
    sort_name_key,
    filter_vacancy(filter_name_key, vacancies_from_csv, *filter_values),
    is_reverse_sorting)

vacancies = formatter_vacancies(sorted_vacancies)

all_columns = (['№'] +
               list(map(lambda key: en_ru_names[key],
                        ["name", "description", "key_skills", "experience_id",
                         "premium", "employer_name", "salary", "area_name", "published date"])))
print_table(all_columns, required_columns, vacancies, *bound)
