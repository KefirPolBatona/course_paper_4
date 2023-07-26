import requests
import json
import os

from abc import ABC, abstractmethod

SJ_API_KEY = os.getenv('SJ_API_KEY')


class Api(ABC):
    """
    Базовый класс для создания подклассов под разные интернет-платформы с вакансиями.
    """

    @abstractmethod
    def api(self):
        """
        Получает список вакансий с сайта.
        """
        pass


class HeadHunterAPI(Api):
    """
    Класс для подключения к API и получения вакансий с сайта HeadHunter.

    Свойства экземпляра класса:
        self.page - номер страницы поиска,
        self.user_vacancy - принимает от пользователя фразу для поиска вакансии,
        self.params - параметры запроса вакансии:
            'text' - фраза для поиска вакансии,
            'only_with_salary' - показывает вакансии только с указанием зарплаты (True),
            'area' - регион (113 - Россия),
            'page' - индекс страницы поиска (0 - первая),
            'per_page' - rол-во вакансий на 1 странице.
    """

    def __init__(self, page, user_vacancy):
        """
        Инициализирует экземпляр класса.
        """

        self.page = page
        self.user_vacancy = user_vacancy
        self.params = {
                       'text': f'NAME:{self.user_vacancy}',
                       'only_with_salary': True,
                       'area': 113,
                       'page': self.page,
                       'per_page': 100
                       }

    def api(self) -> dict:
        """
        Подключается к API HeadHunter.
        Получает список вакансий в json.
        Возвращает список вакансий в dict.
        """

        req = requests.get('https://api.hh.ru/vacancies', self.params)
        data = req.content.decode()
        req.close()
        obj_dict = json.loads(data)

        return obj_dict


class SuperJobAPI(Api):
    """
    Класс для подключения к API и получения вакансий с сайта SuperJob.
    Свойства экземпляра класса:
        self.page - номер страницы поиска,
        self.user_vacancy - принимает от пользователя фразу для поиска вакансии,
        self.headers - токен,
        self.params - параметры запроса вакансии:
            'keyword' - фраза для поиска вакансии,
            'page' - индекс страницы поиска (0 - первая),
            'count' - rол-во вакансий на 1 странице.
    """

    def __init__(self, page, user_vacancy):
        """
        Инициализирует экземпляр класса.
        """



        self.page = page
        self.user_vacancy = user_vacancy

        self.headers = {'X-Api-App-Id': SJ_API_KEY}
        self.params = {
                       'keyword': self.user_vacancy,
                       'page': self.page,
                       'count': 100
                      }

    def api(self) -> dict:
        """
        Подключается к API SuperJob.
        Получает список вакансий в json формате.
        Возвращает список вакансий в dict.
        """

        req = requests.get("https://api.superjob.ru/2.0/vacancies/", params=self.params, headers=self.headers)
        data = req.content.decode()
        req.close()
        obj_dict = json.loads(data)

        return obj_dict
