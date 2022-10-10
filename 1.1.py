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


def input_with_type(value : str) -> str:
    value_type = get_type(value)
    if value_type is bool:
        return f'{parse_bool(value)} ({value_type.__name__})'
    return f'{value} ({value_type.__name__})'


outputs = ["Введите название вакансии: ",
           "Введите описание вакансии: ",
           "Введите требуемый опыт работы (лет): ",
           "Введите нижнюю границу оклада вакансии: ",
           "Введите верхнюю границу оклада вакансии: ",
           "Есть ли свободный график (да / нет): ",
           "Является ли данная вакансия премиум-вакансией (да / нет): "]

inputs = [input(output) for output in outputs]
for inp in inputs:
    print(input_with_type(inp))
