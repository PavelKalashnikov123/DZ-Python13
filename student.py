"""
Создайте класс студента.
* Используя дескрипторы проверяйте ФИО на первую заглавную букву и наличие только букв.
* Названия предметов должны загружаться из файла CSV при создании экземпляра. Другие предметы в экземпляре недопустимы.
* Для каждого предмета можно хранить оценки (от 2 до 5) и результаты тестов (от 0 до 100).
* Также экземпляр должен сообщать средний балл по тестам для каждого предмета и по оценкам всех предметов вместе взятых.
"""
import csv
from functools import reduce
from pathlib import Path
from user_exceptions import UserTypeStrError, UserTypeTextError, UserLessonsError, UserEstimateError


class Validate:
    """Валидация ФИО на первую заглавную букву и наличие только букв"""

    def __set_name__(self, owner, name):
        self.param_name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.param_name)

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.param_name, value)

    def __delete__(self, instance):
        raise AttributeError(f'Свойство "{self.param_name}" нельзя удалять')

    @staticmethod
    def validate(value):
        """проверяйте ФИО на первую заглавную букву и наличие только букв"""
        if not isinstance(value, str):
            raise UserTypeStrError(f'Значение {value} должно быть текстом')
        if not value.isalpha():
            raise UserTypeTextError(f'Значение {value} должно содержать только буквы')
        if not value.istitle():
            raise UserTypeTextError(f'Значение {value} должно начинаться с заглавной буквы')


class Student:
    """Класс студент"""
    name = Validate()
    second_name = Validate()
    surname = Validate()
    _lessons = None

    def __init__(self, name: str, second_name: str, surname: str, lessons: Path):
        """Инициализация ФИО и файла CSV"""
        self.name = name
        self.second_name = second_name
        self.surname = surname
        self.lessons = lessons

    @property
    def lessons(self):
        """getter список предметов из файла CSV при создании экземпляра другие предметы в экземпляре недопустимы"""
        return self._lessons

    @lessons.setter
    def lessons(self, less: Path):
        """setter список предметов из файла CSV при создании экземпляра другие предметы в экземпляре недопустимы"""
        if self.lessons is not None:
            raise UserLessonsError(f'Список предметов уже определён')
        self._lessons = {"уроки": {}}
        with open(less, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                self._lessons["уроки"][row[0]] = {"оценки": [],
                                                  "тесты": [],
                                                  "средний_оценочный_тест": None}
        self._lessons["средняя_оценка"] = None

    def new_estimate(self, name_of_lesson: str, number: int, type_est: str = "меньше"):
        """новая оценка Для каждого предмета можно хранить оценки (от 2 до 5) и результаты тестов (от 0 до 100)"""
        if name_of_lesson not in self.lessons["уроки"].keys():
            raise UserLessonsError(name_of_lesson)
        if type_est == "меньше":
            if number < 2 or number > 5:
                raise UserEstimateError(number, 2, 5)
            self.lessons["уроки"][name_of_lesson]["оценки"].append(number)
            self.lessons["средняя_оценка"] = self.middle_estimate(self.lessons)
        elif type_est == "тест":
            if number < 0 or number > 100:
                raise UserEstimateError(number, 0, 100)
            self.lessons["уроки"][name_of_lesson]["тесты"].append(number)
            """
            Функция reduce() модуля functools кумулятивно применяет функцию function к элементам итерируемой iterable 
            последовательности, сводя её к единственному значению.
            """
            self.lessons["уроки"][name_of_lesson]["средний_оценочный_тест"] = \
                reduce(lambda x, y: x + y, self.lessons["уроки"][name_of_lesson]["тесты"]) / \
                len(self.lessons["уроки"][name_of_lesson]["тесты"])

    @staticmethod
    def middle_estimate(lessons: dict):
        """статический метод определения средней оценки"""
        all_estimates = []
        [all_estimates.extend(lessons["уроки"][name]["оценки"]) for name in lessons["уроки"]]
        """
            Функция reduce() модуля functools кумулятивно применяет функцию function к элементам итерируемой iterable 
            последовательности, сводя её к единственному значению.
            """
        return reduce(lambda x, y: x + y, all_estimates) / len(all_estimates)

    def __repr__(self):
        """представление сущности или объекта сообщает средний балл по тестам для каждого предмета и по оценкам всех
        предметов вместе взятых"""
        result = f'''Студент
полное_имя="{self.name} {self.second_name} {self.surname}",
средняя_оценка={self.lessons["средняя_оценка"]}\n'''
        for key, value in self.lessons["уроки"].items():
            result += f'{key}={value["средний_оценочный_тест"]}\n'

        return result


if __name__ == '__main__':
    ber = Student("Березовский", "Виктор", "Викторович", Path('lessons.csv'))
    print(ber)
    ber.new_estimate("русский язык", 3)
    ber.new_estimate("химия", 5)
    ber.new_estimate("физика", 3)
    ber.new_estimate("физика", 4)
    ber.new_estimate("математика", 5)
    ber.new_estimate("русский язык", 5)
    ber.new_estimate("химия", 3)
    ber.new_estimate("физика", 5)
    ber.new_estimate("физика", 4)
    ber.new_estimate("математика", 4)
    ber.new_estimate("математика", 69, "тест")
    ber.new_estimate("математика", 99, "тест")
    ber.new_estimate("русский язык", 49, "тест")
    ber.new_estimate("русский язык", 100, "тест")
    ber.new_estimate("обществоведение", 78, "тест")
    ber.new_estimate("обществоведение", 74, "тест")
    ber.new_estimate("химия", 58, "тест")
    ber.new_estimate("химия", 95, "тест")
    print(ber)
    # help(ber)