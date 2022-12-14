declension_ru = {
    'ruble': ["рублей", "рубль", "рубля"],
    'year': ["лет", "год", "года"]
}

name_input = ["Title", "Description", "Experience", "Lower_bound", "Upper_bound", "Free_schedule", "Is_premium"]

output_on_user_input = \
    ["Введите название вакансии: ",
     "Введите описание вакансии: ",
     "Введите требуемый опыт работы (лет): ",
     "Введите нижнюю границу оклада вакансии: ",
     "Введите верхнюю границу оклада вакансии: ",
     "Есть ли свободный график (да / нет): ",
     "Является ли данная вакансия премиум-вакансией (да / нет): "]

outputs = dict(zip(name_input[1:],
                   ["Описание", "Требуемый опыт работы", "Средний оклад", "Средний оклад", "Свободный график",
                    "Премиум-вакансия"]))

inputs = dict(zip(name_input, [input(out) for out in output_on_user_input]))


def is_bool(string: str) -> bool:
    return string == "да" or string == "нет"


def parse_bool(string: str) -> bool:
    return string == "да"


def get_type(string: str) -> type:
    if is_bool(string):
        return bool
    if string.isnumeric():
        return int
    return str


def declension(word: str, number: int) -> str:
    ru_word = declension_ru[word]
    if 10 <= number % 100 < 20:
        return ru_word[0]
    if number % 10 == 1:
        return ru_word[1]
    if 1 < number % 10 < 5:
        return ru_word[2]
    return ru_word[0]


print(inputs['Title'])
is_salary_printed = False
for name in name_input[1:]:
    if name == 'Experience':
        print(f"{outputs[name]}: {inputs[name]} {declension('year',int(inputs[name]))}")

    elif not is_salary_printed and outputs[name] == 'Средний оклад':
        avg = (int(inputs['Lower_bound']) + int(inputs['Upper_bound'])) // 2
        print(f"{outputs[name]}: {avg} {declension('ruble', avg)}")
        is_salary_printed = True

    elif is_salary_printed and outputs[name] == 'Средний оклад':
        continue
    else:
        print(f"{outputs[name]}: {inputs[name]}")
