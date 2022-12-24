class Salary:
    def __init__(self, salary_from: str, salary_to: str, salary_currency: str):
        self.salary_from = float(salary_from)
        self.salary_to = float(salary_to)
        self.salary_currency = salary_currency

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
        return (self.salary_from + self.salary_to) * Salary.currency_to_rub()[self.salary_currency] / 2

    def __lt__(self, other):
        return self.avg_salary < other.avg_salary

    def __gt__(self, other):
        return self.avg_salary > other.avg_salary

    def __eq__(self, other):
        return abs(self.avg_salary - other.avg_salary) < 1e-6