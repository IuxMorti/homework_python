from Salary import Salary

class Vacancy:
    def __init__(self, name, salary, area_name, published_at):
        self.__name = name
        self.__salary = salary
        self.__area_name = area_name
        self.__published_at = published_at

    @property
    def name(self):
        return self.__name

    @property
    def salary(self):
        return self.__salary

    @property
    def area_name(self):
        return self.__area_name

    @property
    def published_at(self):
        return self.__published_at

    @staticmethod
    def parse_from_csv_row(row):
        name = row["name"]
        salary = Salary(row["salary_from"], row["salary_to"], row["salary_currency"])
        area_name = row["area_name"]
        published_at = row["published_at"]
        return Vacancy(name, salary, area_name, published_at)