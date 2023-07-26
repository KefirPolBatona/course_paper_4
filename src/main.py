from operator import itemgetter
from classes.class_file_vacancy import JsonFileVacancy
from classes.class_vacancy import Vacancy
from classes.class_api import HeadHunterAPI, SuperJobAPI


def site_selection(iteration=0, input_user=None) -> int:
    """
    Проверяет корректность ввода данных пользователем (str "1" или "2").
    Определяет на каком сайте будет осуществляться поиск вакансий.
    При ошибочности введенных данных предлагает повторить.
    В случае 3-х повторов ошибки закрывает программу.
    """

    if input_user.isdigit() and int(input_user) in [1, 2]:
        return int(input_user)
    elif iteration < 3:
        iteration += 1
        site_selection(iteration, input_user=input('Неверно указан номер, необходимо: 1 - HeadHunter, 2 - SuperJob \n'))
    else:
        print('Попробуй в другой раз :)')
        quit()


def request_vacancy(site_user):
    """
    Принимает номер сайта.
    Принимает от пользователя фразу для поиска.
    Проверяет, удалось ли найти вакансии, удовлетворяющие запросу.
    В случае успешного поиска:
        - создает экземпляр подкласса класса Api(ABC) в зависимости от выбранного сайта,
        - формирует найденные на сайте вакансии (dict) постранично,
        - под каждую стр. создает экземпляр класса JsonFileVacancy,
        - вызывает функцию file_vacancy() для сохранения стр. в отдельный файл.
    """

    vacancy_user = input('Введи слово или фразу для поиска вакансий: \n')

    if site_user == 1:
        check = HeadHunterAPI(0, vacancy_user)
        check_api = check.api()
        pages = 10
        if check_api["found"] == 0:
            print('Не удалось ничего найти, необходимо изменить критерии поиска')
            quit()
        elif check_api["pages"] < pages:
            pages = check_api["pages"]
        else:
            pass

        for page in range(0, pages):
            headhunter_api = HeadHunterAPI(page, vacancy_user)
            obj_dict = headhunter_api.api()
            json_file = JsonFileVacancy(obj_dict)
            json_file.file_vacancy(page+1)

    elif site_user == 2:
        check = SuperJobAPI(0, vacancy_user)
        check_api = check.api()
        pages = 5
        if check_api["total"] == 0:
            print('Не удалось ничего найти, необходимо изменить критерии поиска')
            quit()
        elif round(check_api["total"]/100) < pages:
            pages = round(check_api["total"]/100)
        else:
            pass

        for page in range(0, pages):
            superjob_api = SuperJobAPI(page, vacancy_user)
            obj_dict = superjob_api.api()
            json_file = JsonFileVacancy(obj_dict)
            json_file.file_vacancy(page+1)


def create_list_vacancy(iteration=0, user_input=None) -> list:
    """
    Формирует список вакансий с параметрами для вывода пользователю:
        - извлекает список из сохраненных файлов через функцию import_file_vacancy(),
        - проверяет корректность ответа пользователя, при 3-кратной ошибке закрывает программу,
        - в зависимости от ответа пользователя сортирует список, предварительно удалив вакансии без зарплаты.
    Возвращает отсортированный/нет список вакансий.
    """

    result_list_vacancy = []
    list_vacancy = JsonFileVacancy.import_file_vacancy()

    if user_input in ['N', 'n']:
        pass
    elif user_input in ['Y', 'y']:
        for element in reversed(list_vacancy):
            if element['payment'] is None or element['payment'] == 0:
                list_vacancy.remove(element)
            else:
                continue
        list_vacancy.sort(key=itemgetter('payment'))
    elif iteration < 3:
        iteration += 1
        create_list_vacancy(iteration, user_input=input('Набери Y - если да, N - если нет\n'))
    else:
        print('Попробуй в другой раз :)')
        quit()

    for element in list_vacancy:
        vac_list = []
        for key in element.keys():
            vac_list.append(element[key])
        vacancy = Vacancy(*vac_list)
        result_list_vacancy.append(str(vacancy))

    return result_list_vacancy


def vacancy_print(vacancy_list, user_input=None):
    """
    Выводит на экран пользователя итоговый список вакансий.
    """

    if user_input.isdigit() and len(vacancy_list) >= int(user_input) > 0:
        user_input = int(user_input)
    else:
        user_input = len(vacancy_list)

    num_vac = 0
    for vac in reversed(vacancy_list[-user_input:]):
        num_vac += 1
        print("\n", num_vac, sep='')
        print(vac)


if __name__ == '__main__':

    JsonFileVacancy.clear_file_vacancy()

    user_site = site_selection(input_user=input('Привет, где будем искать вакансии: 1 - HeadHunter, 2 - SuperJob?\n'))
    request_vacancy(user_site)
    print('Вакансии найдены')

    list_vacancy_user = create_list_vacancy(user_input=input('Отсортировать список по размеру зарплаты: Y-да N-нет?\n'))
    vacancy_print(list_vacancy_user, user_input=input('Укажите какое кол-во вакансий вывести на экран:\n'))
