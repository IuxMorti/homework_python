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


def is_bool(string: str) -> bool:
    return string == "да" or string == "нет"


def parse_bool(string: str) -> bool:
    return string == "Да"


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


temp_inputs = []
expected_input_types = [str, str, int, int, int, bool, bool]
for i in range(len(output_on_user_input)):
    inp = input(output_on_user_input[i])
    while len(inp) == 0 or expected_input_types[i] != str and get_type(inp) != expected_input_types[i]:
        inp = input("Данные некорректны, повторите ввод" +
                    "\n" + output_on_user_input[i])
    temp_inputs.append(inp)


inputs = dict(zip(name_input, temp_inputs))


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
