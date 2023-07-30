"""
Создайте класс с базовым исключением и дочерние классы-исключения: ошибка уровня, ошибка доступа.
"""


class CustomException(Exception):
    def __init__(self,  message: str):
        self.message = message

    def __str__(self):
        return f'{self.message}'


class LevelError(CustomException):
    def __init__(self, level_needed, level_given):
        super(LevelError, self).__init__(f'Неправильный уровень: {level_given=} меньше, чем {level_needed=}')


class AccessError(CustomException):
    def __init__(self, user_id, name):
        super(AccessError, self).__init__(
            f'Пользователю отказано в доступе({user_id=}, {name=}) не входит в набор разрешенных.')