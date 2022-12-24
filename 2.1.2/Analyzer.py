from DataSet import DataSet


class Analyzer:
    def __init__(self, file: str, profession: str):
        self.__file = file
        self.__profession = profession
        self.__is_analyzed = False

    def __analyze(self):
        self.__all_salaries_years = dict()
        self.__profession_salaries_years = dict()
        self.__cities = dict()
        self.__count_vacancies = 0
        for vacancy in DataSet(self.__file).csv_filer():
            self.__count_vacancies += 1
            year = int(vacancy.published_at[:4])
            if year not in self.__all_salaries_years:
                self.__all_salaries_years[year] = [0, 0]
                self.__profession_salaries_years[year] = [0, 0]
            self.__all_salaries_years[year][0] += vacancy.salary.avg_salary
            self.__all_salaries_years[year][1] += 1

            if self.__profession in vacancy.name:
                self.__profession_salaries_years[year][0] += vacancy.salary.avg_salary
                self.__profession_salaries_years[year][1] += 1

            if vacancy.area_name not in self.__cities:
                self.__cities[vacancy.area_name] = [0, 0]
            self.__cities[vacancy.area_name][0] += vacancy.salary.avg_salary
            self.__cities[vacancy.area_name][1] += 1

        self.__cities = dict(filter(lambda salary: salary[1][1] / self.__count_vacancies > 0.01, self.__cities.items()))
        self.__is_analyzed = True

    def get_dynamics_salary_levels_by_years(self):
        if not self.__is_analyzed:
            self.__analyze()
        return dict(zip(self.__all_salaries_years.keys(),
                        map(lambda salary: int(salary[0] / salary[1] if salary[1] != 0 else 0),
                            self.__all_salaries_years.values())))

    def get_dynamics_number_vacancies_by_years(self):
        if not self.__is_analyzed:
            self.__analyze()
        return dict(zip(self.__all_salaries_years.keys(),
                        map(lambda salary: salary[1],
                            self.__all_salaries_years.values())))

    def get_dynamics_salaries_years_chosen_profession(self):
        if not self.__is_analyzed:
            self.__analyze()
        return dict(zip(self.__profession_salaries_years.keys(),
                        map(lambda salary: int(
                            salary[0] / salary[1] if salary[1] != 0 else 0),
                            self.__profession_salaries_years.values())))

    def get_dynamics_number_vacancies_years_chosen_profession(self):
        if not self.__is_analyzed:
            self.__analyze()
        return dict(zip(self.__profession_salaries_years.keys(),
                        map(lambda salary: salary[1],
                            self.__profession_salaries_years.values())))

    def get_salary_levels_by_city(self):
        if not self.__is_analyzed:
            self.__analyze()
        return dict(sorted(zip(self.__cities.keys(),
                               map(lambda salary: int(salary[0] / salary[1] if salary[1] != 0 else 0),
                                   self.__cities.values())),
                           key=lambda tup: tup[1],
                           reverse=True)[:10])

    def get_share_vacancies_by_city(self):
        if not self.__is_analyzed:
            self.__analyze()
        return dict(sorted(zip(self.__cities.keys(),
                               map(lambda salary: round(
                                   salary[1] / self.__count_vacancies if self.__count_vacancies != 0 else 0, 4),
                                   self.__cities.values())), key=lambda tup: tup[1],
                           reverse=True)[:10])