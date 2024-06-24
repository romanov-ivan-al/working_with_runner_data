"""
Это основной модуль программы.
Содержит точку входа - main.
"""
from timer import timer
from data import ReadWriteData as rd, SortFillingData as sd


@timer(5)  # декоратор для замера времени работы программы
def main() -> None:
    """Функция для запуска программы."""
    race_data_dict = rd.read_race_data("data/race_data.json")
    dict_data = sd.sort_by_time(race_data_dict)
    sd.result_data(dict_data)
    rd.write_data(dict_data)


if __name__ == "__main__":
    main()
