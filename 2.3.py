import csv
import re


class City:
    def __init__(self, name_city):
        self.__name_city = name_city
        self.__count = 0
        self.__sum_salary = 0

    @property
    def name_city(self):
        return self.__name_city

    @property
    def count(self):
        return self.__count

    def append(self, avg_salary):
        self.__sum_salary += avg_salary
        self.__count += 1

    @property
    def average_salary(self):
        return self.__sum_salary / self.__count


declension_ru = {"ruble": ["рублей", "рубль", "рубля"],
                 "vacancy": ["вакансий", "вакансия", "вакансии"],
                 "once": ["раз", "раз", "раза"],
                 "skill": ["скиллов", "скилла", "скиллов"],
                 "city": ["городов", "города", "городов"]
                 }


def parse_csv(file_name):
    dicts = []
    columns = []
    with open(file_name, encoding='utf-8-sig') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        is_first = True
        for row in file_reader:
            if is_first:
                columns = row
                is_first = False
                continue
            if len(row) != len(columns) or "" in row:
                continue

            temp_dict = dict()
            for index, column in enumerate(columns):
                temp_dict[column] = strip_tags(row[index]) \
                    if column != "key_skills" \
                    else list(map(strip_tags, row[index].split('\n')))
            dicts.append(temp_dict)
    return dicts


def strip_tags(string: str) -> str:
    return ' '.join(re.sub(re.compile("<.*?>"), "", string).split())


def declension(word: str, number: int) -> str:
    ru_word = declension_ru[word]
    if 10 <= number % 100 < 20:
        return ru_word[0]
    if number % 10 == 1:
        return ru_word[1]
    if 1 < number % 10 < 5:
        return ru_word[2]
    return ru_word[0]


def avg_sum(*args):
    a = list(map(float, args))
    return int(sum(a)) // len(a)


def average_salary(vacancy: dict):
    return avg_sum(vacancy["salary_from"], vacancy["salary_to"])


def print_salary(salaries):
    for i, vacancy in enumerate(salaries):
        s = average_salary(vacancy)
        print(f"    {i + 1}) {vacancy['name']} в компании \"{vacancy['employer_name']}\""
              + f" - {s} {declension('ruble',s)} (г. {vacancy['area_name']})")
    print()


parse_dict = parse_csv(input())

rur_vacancies = list(filter(lambda d: d["salary_currency"] == "RUR", parse_dict))

skills = dict()
cities = dict()
for rur_vacancy in rur_vacancies:
    for skill in rur_vacancy["key_skills"]:
        if skill not in skills:
            skills[skill] = 0
        skills[skill] += 1

    if rur_vacancy["area_name"] not in cities:
        cities[rur_vacancy["area_name"]] = City(rur_vacancy["area_name"])
    cities[rur_vacancy["area_name"]].append(average_salary(rur_vacancy))

print("Самые высокие зарплаты:")
print_salary(list(map(lambda tup: tup[1], sorted(enumerate(rur_vacancies),
                                                 key=lambda tup: (-average_salary(tup[1]), tup[0]))))[:10])

print("Самые низкие зарплаты:")
print_salary(list(map(lambda tup: tup[1], sorted(enumerate(rur_vacancies),
                                                 key=lambda tup: (average_salary(tup[1]), tup[0]))))[:10])

print(f"Из {len(skills)} {declension('skill',len(skills))}, самыми популярными являются:")
for counter, item in enumerate(sorted(skills.items(), key=lambda x: x[1], reverse=True)[:10]):
    skill, count = item
    print(f"    {counter + 1}) {skill} - упоминается {count} {declension('once', count)}")

print()

print(f"Из {len(cities)} {declension('city', len(cities))}, самые высокие средние ЗП:")
for counter, city in enumerate(sorted(
        filter(lambda city: city.count * 100 / len(rur_vacancies) >= 0.9, cities.values()),
        key=lambda city: city.average_salary, reverse=True)[:10]):

    print(f"    {counter + 1}) {city.name_city} - средняя зарплата {int(city.average_salary)}",
          f"{declension('ruble', int(city.average_salary))}",
          f"({city.count} {declension('vacancy',city.count)})")