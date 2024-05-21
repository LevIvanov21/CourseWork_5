from Config import config
from src.db_manager import DBManager
from src.utils import get_hh_json, create_database, save_data_to_database


def main():
    params = config()  # параметр для БД
    employers = ['906557', '84585', '2624085', '2523', '10317521',
                 '15478', '78638', '2537115', '10492215', '588914']
    data = get_hh_json(employers)
    create_database('hh_vacancies', params)
    save_data_to_database(data, 'hh_vacancies', params)
    db_manager = DBManager('hh_vacancies', params)

    print("Представляю вам 10 компаний для осуществления выборки:\n"
          "'SberTech', 'avito', 'вкусно и точка', 'М.Видео', 'Додо Пицца',\n"
          "'VK', 'Тинькофф', 'МТС', 'Дом.ру', 'Aviasales'\n")
    input('Для продолжения нажмите "Enter"')

    print("Список компаний и количество их вакансий:")
    for row in db_manager.get_companies_and_vacancies_count():
        print(f"{row[0]} - {row[1]}")
    input('\nДля продолжения нажмите "Enter"\n')

    print("Назавание компании, зарплата, вакансия, ссылка на вакансию")
    for row in db_manager.get_all_vacancies():
        print(f"{row[0]} - {row[1]} - Минимальная заработная плата: {row[2]} - Ссылка: {row[3]}'")
    input('\nДля продолжения нажмите "Enter"\n')

    print("Средняя зарплата по вакансиям:")
    for row in db_manager.get_avg_salary():
        print(f"{row[0]} - {row[1]}")
    input('\nДля продолжения нажмите "Enter"\n')

    print("Вакансии с зарплатой вышего средней:")
    for row in db_manager.get_vacancies_with_higher_salary():
        print(f'{row[1]} - {row[3]} - {row[7]} - {row[8]}')
    input('\nДля продолжения нажмите "Enter"\n')

    keyword = input("Введите ключевое слово для получения вакансий в названии которых оно указано: ")
    for row in db_manager.get_vacancies_with_keyword(keyword):
        print(f'{row[1]} - {row[3]} - {row[7]} - {row[8]}')


if __name__ == '__main__':
    main()
