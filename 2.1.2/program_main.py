from Analyzer import Analyzer
from Report import Report


file_name = input("Введите название файла: ")
prof = input("Введите название профессии: ")

analyzer = Analyzer(file_name, prof)

dynamics_salary_levels_by_years = analyzer.get_dynamics_salary_levels_by_years()
dynamics_number_vacancies_by_years = analyzer.get_dynamics_number_vacancies_by_years()
dynamics_salaries_years_chosen_profession =  analyzer.get_dynamics_salaries_years_chosen_profession()
dynamics_number_vacancies_years_chosen_profession =  analyzer.get_dynamics_number_vacancies_years_chosen_profession()
salary_levels_by_city = analyzer.get_salary_levels_by_city()
share_vacancies_by_city = analyzer.get_share_vacancies_by_city()

report = Report(dynamics_salary_levels_by_years, dynamics_number_vacancies_by_years,
                dynamics_salaries_years_chosen_profession, dynamics_number_vacancies_years_chosen_profession,
                salary_levels_by_city, share_vacancies_by_city, prof)

report.generate_excel()
report.generate_image()
print("Динамика уровня зарплат по годам:",
      dynamics_salary_levels_by_years)

print("Динамика количества вакансий по годам:",
      dynamics_number_vacancies_by_years)

print("Динамика уровня зарплат по годам для выбранной профессии:",
      dynamics_salaries_years_chosen_profession)

print("Динамика количества вакансий по годам для выбранной профессии:",
      dynamics_number_vacancies_years_chosen_profession)

print("Уровень зарплат по городам (в порядке убывания):", salary_levels_by_city)

print("Доля вакансий по городам (в порядке убывания):", share_vacancies_by_city)