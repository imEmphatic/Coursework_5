import psycopg2
from typing import Any


class DataBase:
    """
    Класс, который из списка (JSON) заполняет созданные
    в БД PostgreSQL таблицы данными о работодателях и их вакансиях
    """

    @staticmethod
    def create_database(database_name: str, params: dict) -> None:
        """
        Метод для создания Базы Данных и создания таблиц в БД
        """
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()

        try:
            cur.execute(f'DROP DATABASE {database_name}')
        except:
            pass

        cur.execute(f'CREATE DATABASE {database_name}')

        cur.close()
        conn.close()

        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                    CREATE TABLE company (
                        company_id SERIAL PRIMARY KEY,
                        company_name VARCHAR(255) not null,
                        company_area VARCHAR(255) not null,
                        url TEXT,
                        open_vacancies INTEGER
                    )
                """)

        with conn.cursor() as cur:
            cur.execute("""
                    CREATE TABLE vacancy (
                        vacancy_id SERIAL PRIMARY KEY,
                        vacancy_name VARCHAR(255),
                        vacancy_area VARCHAR(255),
                        salary INTEGER,
                        company_id INT REFERENCES company(company_id),
                        vacancy_url VARCHAR(255)
                    )
                """)

        conn.commit()
        conn.close()

    @staticmethod
    def save_data_to_database_company(data_company: list[dict[str, Any]], database_name: str, params: dict) -> None:
        """
        Метод для заполнения таблицы компаний в БД
        """
        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            for emp in data_company:
                cur.execute("""
                    INSERT INTO company (company_id, company_name, company_area, url, open_vacancies)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                            (emp['id'], emp['name'], emp['area']['name'], emp['alternate_url'], emp['open_vacancies']))

        conn.commit()
        conn.close()

    @staticmethod
    def save_data_to_database_vac(data_vac: list[dict[str, Any]], database_name: str, params: dict) -> None:
        """
        Метод для заполнения таблицы вакансий в БД
        """

        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            for vac_company in data_vac:
                for vac in vac_company:
                    if vac['salary'] is None:
                        cur.execute("""
                           INSERT INTO vacancy (
                           vacancy_id, vacancy_name, vacancy_area, salary, company_id, vacancy_url
                           )
                           VALUES (%s, %s, %s, %s, %s, %s)
                           """,
                                    (vac['id'], vac['name'], vac['area']['name'], 0, vac['employer']['id'],
                                     vac['alternate_url']))
                    elif vac['salary']['from'] is None:
                        cur.execute("""
                           INSERT INTO vacancy (
                           vacancy_id, vacancy_name, vacancy_area, salary, company_id, vacancy_url
                           )
                           VALUES (%s, %s, %s, %s, %s, %s)
                           """,
                                    (vac['id'], vac['name'], vac['area']['name'], vac['salary']['to'], vac['employer']['id'],
                                     vac['alternate_url']))
                    else:
                        cur.execute("""
                            INSERT INTO vacancy (vacancy_id, vacancy_name, vacancy_area, salary, company_id, vacancy_url)
                            VALUES (%s, %s, %s, %s, %s, %s)
                            """,
                                    (vac.get('id'), vac['name'], vac['area']['name'], vac['salary']['from'],
                                     vac['employer']['id'], vac['alternate_url']))

        conn.commit()
        conn.close()