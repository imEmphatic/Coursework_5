from src.database_PostgreSQL import DataBase
from src.API_HH import HeadHunterRuAPI
from src.DBManager import DBManager
from config import config


def main():
    params = config()
    database_name = "hh"  #Название базы данных

    hh_api = HeadHunterRuAPI    #Получение данных по API
    companies = hh_api.getting_info_company()   #Получение данных по компаниям
    vacancies = hh_api.getting_vacancy()    #Получение данных по вакансиям

    # Создание базы данных и таблиц
    hh_database = DataBase
    hh_database.create_database(database_name, params)

    # Внесение данных в таблицу "company"
    hh_database.save_data_to_database_company(companies, database_name, params)
    # Внесение данных в таблицу "vacancy"
    hh_database.save_data_to_database_vac(vacancies, database_name, params)

    # Работа с БД
    db_manager = DBManager(database_name, params)

    print(f"Выберите запрос: \n"
          f"1 - Список всех компаний и количество вакансий у каждой компании\n"
          f"2 - Cписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию\n"
          f"3 - Средняя зарплата по вакансиям\n"
          f"4 - Список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
          f"5 - Список всех вакансий, в названии которых содержатся запрашиваемое слово\n"
          f"0 - Выход из программы")

    while True:
        user_input = int(input('\nВведите цифру запроса\n'))
        if user_input == 1:
            companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
            print(f"Список всех компаний и количество вакансий у каждой компании:")
            for company in companies_and_vacancies_count:
                print(f'{company[0]} - количество полученных вакансий {company[1]}')
        elif user_input == 2:
            all_vacancies = db_manager.get_all_vacancies()
            print(f"Cписок всех вакансий: {all_vacancies}")
            for vacancy in all_vacancies:
                print(f'Компания - {vacancy[0]}')
                print(f'Вакансия - {vacancy[1]}')
                print(f'ЗП - {vacancy[2]}')
                print(f'Ссылка на вакансию - {vacancy[3]}\n')

        elif user_input == 3:
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата по вакансиям: {round(avg_salary[0][0],2)}\n")

        elif user_input == 4:
            vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
            print(f"Список всех вакансий, у которых зарплата выше средней:\n")
            for vacancy in vacancies_with_higher_salary:
                print(f'Вакансия - {vacancy[0]}')
                print(f'ЗП - {vacancy[1]}')
                print(f'Ссылка на вакансию - {vacancy[2]}\n')

        elif user_input == 5:
            user_input_keyword = input('Введите ключевое слово ')
            vacancies_with_keyword = db_manager.get_vacancies_with_keyword(user_input_keyword)
            print(f"Список всех вакансий, в названии которых содержатся запрашиваемое слово:")
            for vacancy in vacancies_with_keyword:
                print(f'Вакансия - {vacancy[1]}')
                print(f'Город - {vacancy[2]}')
                print(f'ЗП - {vacancy[3]}')
                print(f'Ссылка на вакансию - {vacancy[5]}\n')

        elif user_input == 0:
            break

        else:
            print("Нет такой команды")


if __name__ == '__main__':
    main()