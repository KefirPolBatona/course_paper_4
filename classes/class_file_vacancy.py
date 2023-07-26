from abc import ABC, abstractmethod

import json
import os


class FileVacancy(ABC):
    """
    Базовый класс для работы с файлом вакансий.
    """

    @abstractmethod
    def file_vacancy(self, page):
        """
        Сохраняет вакансии в файл.
        """
        pass

    @staticmethod
    @abstractmethod
    def import_file_vacancy() -> list:
        """
        Возвращает список вакансий с определенными параметрами.
        """
        pass

    @staticmethod
    @abstractmethod
    def clear_file_vacancy():
        """
        Удаляет информацию о вакансиях.
        """
        pass


class JsonFileVacancy(FileVacancy):
    """
    Класс для сохранения информации о вакансиях в файл JSON.
    """
    def __init__(self, dict_obj):
        """
        Инициализирует экземпляр класса.
        """
        self.dict_obj = dict_obj

    def file_vacancy(self, page):
        """
        Сохраняет вакансии в файл JSON.
        """

        file_name = './vacancy/{}.json'.format(page)
        with open(file_name, 'w', encoding="utf-8") as f:
            f.write(json.dumps(self.dict_obj, ensure_ascii=False, indent=4))

    @staticmethod
    def import_file_vacancy() -> list:
        """
        Формирует перечень ранее созданных файлов со списком вакансий.
        Реализует цикл по файлам перечня, открывает каждый и считывает его содержимое.
        Преобразует полученный текст в объект справочника и реализует цикл по вакансиям.
        Сохраняет вакансии с определенными параметрами в список и возвращает его.
        """

        result = []

        for fl in os.listdir('./vacancy'):
            with open('./vacancy/{}'.format(fl), encoding='utf8') as f:
                json_text = f.read()
            json_obj = json.loads(json_text)

            # a = json_obj.keys()
            # print(json_obj)
            if 'items' in json_obj:
                for vac in json_obj['items']:
                    vac_dict = {}
                    vac_dict.update(name_vacancy=vac['name'],
                                    url=vac['alternate_url'],
                                    payment=vac['salary']['from'],
                                    equirements=vac['snippet']['requirement'],
                                    area=vac['area']['name'])
                    result.append(vac_dict)

            elif 'objects' in json_obj:
                for vac in json_obj['objects']:
                    vac_dict = {}
                    vac_dict.update(name_vacancy=vac['profession'],
                                    url=vac['link'],
                                    payment=vac['payment_from'],
                                    equirements=vac['candidat'],
                                    area=vac['town']['title'])
                    result.append(vac_dict)

        return result

    @staticmethod
    def clear_file_vacancy():
        """
        Очищает каталог от файлов с вакансиями, полученными в результате прежней работы программы.
        """
        clear_vacancy = './vacancy'
        for f in os.listdir(clear_vacancy):
            os.remove(os.path.join(clear_vacancy, f))
