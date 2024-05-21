import requests
import psycopg2


def get_hh_json(employers: list[str]) -> list[dict]:
    """
    Получает данные: информация о работодателях и их вакансиях. Формат json
    """
    data = []
    for emp in employers:
        url = f'https://api.hh.ru/employers/{emp}'
        data_company = requests.get(url).json()
        data_vacancy = requests.get(data_company['vacancies_url']).json()
        data.append({'employers': data_company, 'vacancies': data_vacancy['items']})
    return data


def create_database(db_name: str, params: dict) -> None:
    """создание базы данных по вокансиям с HeadHanter"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")
    conn.close()

    conn = psycopg2.connect(dbname=db_name, ** params)
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE employers (
            employer_id SERIAL PRIMARY KEY,
            employer_name VARCHAR UNIQUE,
            url TEXT
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE vacancies (
            vacancy_id SERIAL PRIMARY KEY,
            employer_name text REFERENCES employers(employer_name),
            city VARCHAR(50),
            title VARCHAR(200),
            schedule TEXT,
            requirement TEXT,
            responsibility TEXT,
            salary INT,
            url VARCHAR(200),
            FOREIGN KEY(employer_name) REFERENCES employers(employer_name)
            )
        """)
        conn.commit()
        conn.close()


def save_data_to_database(data: list[dict], dn_name: str, params: dict) -> None:
    """Сохранение данных о вакансиях в БД"""
    conn = psycopg2.connect(dbname=dn_name, **params)
    with conn.cursor() as cur:
        for emp in data:
            cur.execute("""
            INSERT INTO employers (employer_name, url)
            VALUES (%s, %s)
            RETURNING employer_name""",
                        (emp['employers']['name'], emp['employers']['alternate_url'])
                        )
            employer_name = cur.fetchone()[0]
            for vacancy in emp['vacancies']:
                salary = vacancy['salary']['from'] if vacancy['salary'] else None
                cur.execute("""
                INSERT INTO vacancies (employer_name, city, title, schedule, requirement,
                responsibility, salary, url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                            (employer_name, vacancy['area']['name'], vacancy['name'],
                             vacancy['schedule']['name'], vacancy['snippet']['requirement'],
                             vacancy['snippet']['responsibility'], salary, vacancy['alternate_url'])
                            )
    conn.commit()
    conn.close()