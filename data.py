"""Модуль для работы с данными."""

import json
from datetime import datetime, timedelta


class ReadWriteData:
    """Класс содержит методы для чтения и записи данных."""

    @staticmethod
    def read_race_data(path_to_file: str) -> list[dict]:
        """Функция для чтения json файла с данными о соревновании.
        Возвращает список словарей с данными."""
        with open(path_to_file, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def read_prizes_list(path_to_file: str) -> list[str]:
        """Функция для чтения txt файла с призами.
        Возвращает список строк с призами."""
        with open(path_to_file, "r", encoding="utf-8") as file:
            return [line.strip().split(" место ")[1] for line in file.readlines()]

    @staticmethod
    def write_data(dict_data: dict[str, dict]) -> None:
        """Функция для записи словаря c итоговым набором данных в json файлы.
        На вход подается словарь с данными"""
        for key in dict_data.keys():
            with open(key.lower() + ".json", "w", encoding="utf-8") as file:
                json.dump(dict_data[key], file, indent=2, ensure_ascii=False)


class CalculateTime:
    """Класс содержит метод для вычисления времени забега."""

    @staticmethod
    def calculate_time(start_time: str, finish_time: str) -> datetime:
        """Функция для вычисления времени забега.
        На вход подается время старта и время финиша в виде строки.
        Возвращает время забега в типе datetime."""
        finish_t = datetime.strptime(finish_time, "%H:%M:%S")
        start_t = datetime.strptime(start_time, "%H:%M:%S")
        if start_t > finish_t:
            finish_t += timedelta(days=1)
        return finish_t - start_t


class SortFillingData:
    """Класс содержит методы для сортировки и заполнения данными."""

    @staticmethod
    def sort_by_time(race_data: list[dict]) -> dict[str, list[dict]]:
        """Функция создает словарь с данными по категориям спортсменов.
        На вход принимает считанный список словарей.
        Груупирует все словари по категориям и складыввает в списки
        по соответствующему ключу. После каждый из списоков сортируется по времени
        забега и нагрудному номеру(в случае если время совпадает).
        Возвращает словарь с данными по категориям спортсменов."""
        dict_result = {"M15": [], "M16": [], "M18": [], "W15": [], "W16": [], "W18": []}
        for runner in race_data:
            time_start = runner["Время старта"]
            time_finish = runner["Время финиша"]
            time_run = CalculateTime.calculate_time(time_start, time_finish)
            dict_result[runner["Категория"]].append(
                {
                    "Нагрудный номер": runner["Нагрудный номер"],
                    "Имя и Фамилия": runner["Имя"] + " " + runner["Фамилия"],
                    "Время": str(time_run),
                }
            )
        for category in dict_result:
            dict_result[category] = sorted(
                dict_result[category], key=lambda x: (x["Время"], x["Нагрудный номер"])
            )
        return dict_result

    @staticmethod
    def result_data(dict_data: dict[str, list[dict]]) -> None:
        """Функция дополняет результурющий словарь данными о призах и месте в забеге.
        На вход подается словарь с данными по категориям спортсменов."""
        for key in dict_data.keys():
            count = 1
            list_with_prizes = ReadWriteData.read_prizes_list(
                f"data/prizes_list_{key.lower()}.txt"
            )
            for data in dict_data[key]:
                data["Место"] = count
                if count < 50:
                    data["Приз"] = list_with_prizes[count - 1]
                count += 1
