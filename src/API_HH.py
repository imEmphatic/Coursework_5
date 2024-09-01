import requests
from src.list_companies import companies_data


class HeadHunterRuAPI:
    """
    Подключается к API и получает вакансии по ключевому слову
    """

    @staticmethod
    def getting_info_company():
        """
        Получает данные с HH.ru по компаниям из файла "list_companies.py"
        :return: список словарей с информацией по компаниям
        """

        data_company = []
        url = 'https://api.hh.ru/employers/'

        for company_name, company_id in companies_data.items():
            response = requests.get(f'{url}{company_id}').json()
            data_company.append(response)
        return data_company

    @staticmethod
    def getting_vacancy():
        """
        Получает вакансии по компаниям из файла "list_companies.py" с HH.ru
        :return: список словарей с вакансиями по компаниям
        """

        data_vacancy = []
        url = 'https://api.hh.ru/vacancies?employer_id='

        for company_name, company_id in companies_data.items():
            response = requests.get(f'{url}{company_id}', params={'page': 0, 'per_page': 100}).json()['items']
            data_vacancy.append(response)
        return data_vacancy
