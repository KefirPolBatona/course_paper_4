
class Vacancy:
    """
    Класс для работы с вакансиями.
    """

    def __init__(self, name_vacancy, url, payment, requirements, area):
        """
        Инициализирует экземпляр класса.
        """

        self.name_vacancy = name_vacancy
        self.url = url
        self.payment = payment
        self.requirements = requirements
        self.area = area

    def __gt__(self, other):
        """
        Сравнивает зарплаты методом для операции сравнения «больше» (self > other).
        """
        return self.payment > other.payment

    def __str__(self) -> str:
        """
        Возвращает информацию о вакансии для пользователя
        """
        return f"ВАКАНСИЯ - {self.name_vacancy} \nCсылка - {self.url} \nОплата (мин.) - {self.payment} \n" \
               f"Описание - {self.requirements} \nРегион - {self.area}"
