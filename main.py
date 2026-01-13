#КАДРОВОЕ АГЕНТСТВО - ПРОГРАММА ДЛЯ УПРАВЛЕНИЯ БАЗОЙ ВАКАНСИЙ, вариант 8

vacancies_db = []

#Список уровней образования
EDUCATION_LEVELS = ["Без образования", "Среднее", "Среднее специальное", "Высшее"]

#Словарь с номерами для каждого уровня
EDUCATION_RANKS = {
    "Без образования": 1,
    "Среднее": 2,
    "Среднее специальное": 3, 
    "Высшее": 4
}

#ФУНКЦИИ ДЛЯ РАБОТЫ С ФАЙЛАМИ

def load_vacancies():
    """Загрузка вакансий из файла vacancies.txt"""
    global vacancies_db
    try:
        with open("vacancies.txt", 'r', encoding='utf-8') as f:
            next(f)  #Пропускаем заголовок
            vacancies_db = []
            for line in f:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) >= 10:
                        vacancy = {
                            'position': parts[0].strip(),
                            'experience': int(parts[1].strip()),
                            'gender': parts[2].strip(),
                            'education': parts[3].strip(),
                            'min_age': int(parts[4].strip()),
                            'max_age': int(parts[5].strip()),
                            'languages': parts[6].strip() or "Не указано",
                            'min_salary': int(parts[7].strip()),
                            'social_package': parts[8].strip().lower() in ['true', 'да', 'yes', '1'],
                            'probation_period': int(parts[9].strip())
                        }
                        vacancies_db.append(vacancy)
        print(f"Загружено вакансий: {len(vacancies_db)}")
        return True
    except FileNotFoundError:
        print("Ошибка: файл vacancies.txt не найден!")
        return False
    except Exception as e:
        print(f"Ошибка при загрузке файла: {e}")
        return False

def save_vacancies():
    """Сохранение вакансий в файл vacancies.txt"""
    try:
        with open("vacancies.txt", 'w', encoding='utf-8') as f:
            f.write("Должность,Стаж,Пол,Образование,Мин.возраст,Макс.возраст,Языки,Оклад,Соцпакет,Исп.срок\n")
            for v in vacancies_db:
                f.write(f"{v['position']},{v['experience']},{v['gender']},"
                       f"{v['education']},{v['min_age']},{v['max_age']},"
                       f"{v['languages']},{v['min_salary']},"
                       f"{'True' if v['social_package'] else 'False'},"
                       f"{v['probation_period']}\n")
        print(f"Сохранено вакансий: {len(vacancies_db)}")
        return True
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")
        return False

#ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ДЛЯ ВАЛИДАЦИИ

def get_input(prompt, validator=None, default=None):
    """Универсальная функция ввода с валидацией"""
    while True:
        value = input(prompt).strip()
        if not value and default is not None:
            return default
        if validator:
            result, error = validator(value)
            if result:
                return result
            print(f"Ошибка: {error}")
        elif value:
            return value
        else:
            print("Ошибка: поле не может быть пустым!")

def validate_gender(value):
    """Валидация пола"""
    value = value.upper()
    if value in ['М', 'M', 'МУЖ', 'MALE']:
        return 'М', None
    elif value in ['Ж', 'F', 'ЖЕН', 'FEMALE']:
        return 'Ж', None
    return None, "допустимые значения: 'М' или 'Ж'"

def validate_bool(value):
    """Валидация булевого значения"""
    value = value.lower()
    if value in ['да', 'д', 'yes', 'y', 'true', '1']:
        return True, None
    elif value in ['нет', 'н', 'no', 'n', 'false', '0']:
        return False, None
    return None, "введите 'да' или 'нет'"

def validate_int(value, min_val=None, max_val=None):
    """Валидация целого числа"""
    try:
        num = int(value.replace(" ", ""))
        if min_val is not None and num < min_val:
            return None, f"значение не может быть меньше {min_val}"
        if max_val is not None and num > max_val:
            return None, f"значение не может быть больше {max_val}"
        return num, None
    except ValueError:
        return None, "введите целое число"

def validate_str(value, min_len=1, allow_numbers=True):
    """Валидация строки"""
    if len(value) < min_len:
        return None, f"должно быть не менее {min_len} символов"
    if not allow_numbers and any(c.isdigit() for c in value):
        return None, "нельзя использовать цифры"
    return value, None

def validate_education(value):
    """Валидация образования"""
    if value.isdigit() and 1 <= int(value) <= len(EDUCATION_LEVELS):
        return EDUCATION_LEVELS[int(value)-1], None
    for edu in EDUCATION_LEVELS:
        if value.lower() == edu.lower():
            return edu, None
    return None, f"выберите из списка: {', '.join(f'{i+1}.{e}' for i,e in enumerate(EDUCATION_LEVELS))}"

#ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ДЛЯ ПРОВЕРКИ ВВОДА

def check_position(value):
    """Проверка должности"""
    return validate_str(value, 2, False)

def check_experience(value):
    """Проверка стажа"""
    return validate_int(value, 0, 50)

def check_age_min(value):
    """Проверка минимального возраста"""
    return validate_int(value, 18, 100)

def check_salary(value):
    """Проверка оклада"""
    return validate_int(value, 0, 1000000)

def check_probation(value):
    """Проверка испытательного срока"""
    return validate_int(value, 0, 12)

def check_menu_choice(value):
    """Проверка выбора в меню"""
    return validate_int(value, 1, 9)

def check_vacancy_choice(value, max_num):
    """Проверка выбора вакансии"""
    return validate_int(value, 0, max_num)

def check_max_age(value, min_age):
    """Проверка максимального возраста"""
    return validate_int(value, min_age, 100)

def check_max_salary(value, min_salary):
    """Проверка максимального оклада"""
    return validate_int(value, min_salary, 1000000)

#СОРТИРОВКА ХОАРА И ФУНКЦИИ ДЛЯ КЛЮЧЕЙ

def quick_sort(arr, key_func=None):
    """Cортировка Хоара"""
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr)//2]
    pivot_key = key_func(pivot) if key_func else pivot
    
    left = [x for x in arr if (key_func(x) if key_func else x) < pivot_key]
    middle = [x for x in arr if (key_func(x) if key_func else x) == pivot_key]
    right = [x for x in arr if (key_func(x) if key_func else x) > pivot_key]
    
    return quick_sort(left, key_func) + middle + quick_sort(right, key_func)

def key_report1(v):
    """Ключ для отчета 1: образование (↑) + должность (↑)"""
    return (EDUCATION_RANKS.get(v['education'], 0), v['position'].lower())

def key_report2(v):
    """Ключ для отчета 2: исп.срок (↓) + стаж (↓) + возраст (↑)"""
    return (-v['probation_period'], -v['experience'], v['max_age'])

def key_report3(v):
    """Ключ для отчета 3: соцпакет (↑) + исп.срок (↓)"""
    return (0 if v['social_package'] else 1, -v['probation_period'])

#ФУНКЦИИ ДЛЯ РАБОТЫ С ВАКАНСИЯМИ

def add_vacancy():
    """Добавление новой вакансии"""
    print("\nДОБАВЛЕНИЕ НОВОЙ ВАКАНСИИ")
    
    print("\nОбразование:")
    for i in range(4):  #4 уровня образования
        print(f"{i+1}. {EDUCATION_LEVELS[i]}")
    
    position = get_input("Должность: ", check_position)
    experience = get_input("Стаж (лет): ", check_experience)
    gender = get_input("Пол (М/Ж): ", validate_gender)
    education = get_input("Образование: ", validate_education)
    
    min_age = get_input("Мин.возраст: ", check_age_min)
    max_age = get_input("Макс.возраст: ", lambda v: check_max_age(v, min_age))
    
    languages = input("Языки (Enter - пропустить): ").strip() or "Не указано"
    min_salary = get_input("Оклад (руб.): ", check_salary)
    social = get_input("Соцпакет (да/нет): ", validate_bool)
    probation = get_input("Исп.срок (мес.): ", check_probation)
    
    vacancy = {
        'position': position,
        'experience': experience,
        'gender': gender,
        'education': education,
        'min_age': min_age,
        'max_age': max_age,
        'languages': languages,
        'min_salary': min_salary,
        'social_package': social,
        'probation_period': probation
    }
    
    vacancies_db.append(vacancy)
    print(f"Вакансия '{position}' добавлена!")
    save_vacancies()

def edit_vacancy():
    """Изменение вакансии"""
    if not vacancies_db:
        print("Нет вакансий!")
        return
    
    print("\nИЗМЕНЕНИЕ ВАКАНСИИ")
    
    #Показать список вакансий
    for i, v in enumerate(vacancies_db, 1):
        print(f"{i}. {v['position']} - {v['min_salary']}₽")
    
    #Выбрать вакансию
    choice = get_input(f"Номер (1-{len(vacancies_db)}), 0-отмена: ", 
                      lambda v: check_vacancy_choice(v, len(vacancies_db)))
    
    if choice == 0:
        return
    
    vacancy = vacancies_db[choice-1]
    print(f"\nРедактирование: {vacancy['position']}")
    print("(Enter - оставить текущее)")
    
    #Редактировать каждое поле
    def edit_field(field_name, check_func, current):
        value = input(f"{field_name} [{current}]: ").strip()
        if value:
            ok, result = check_func(value)
            if ok:
                return result
        return current
    
    #Функции для проверки при редактировании
    def check_position_edit(value):
        return validate_str(value, 2, False)
    
    def check_experience_edit(value):
        return validate_int(value, 0, 50)
    
    def check_min_age_edit(value):
        return validate_int(value, 18, vacancy['max_age'])
    
    def check_max_age_edit(value):
        return validate_int(value, vacancy['min_age'], 100)
    
    def check_salary_edit(value):
        return validate_int(value, 0, 1000000)
    
    def check_probation_edit(value):
        return validate_int(value, 0, 12)
    
    vacancy['position'] = edit_field("Должность", check_position_edit, vacancy['position'])
    vacancy['experience'] = edit_field("Стаж", check_experience_edit, vacancy['experience'])
    vacancy['gender'] = edit_field("Пол", validate_gender, vacancy['gender'])
    vacancy['education'] = edit_field("Образование", validate_education, vacancy['education'])
    vacancy['min_age'] = edit_field("Мин.возраст", check_min_age_edit, vacancy['min_age'])
    vacancy['max_age'] = edit_field("Макс.возраст", check_max_age_edit, vacancy['max_age'])
    
    lang_input = input(f"Языки [{vacancy['languages']}]: ").strip()
    if lang_input:
        vacancy['languages'] = lang_input
    
    vacancy['min_salary'] = edit_field("Оклад", check_salary_edit, vacancy['min_salary'])
    
    social_input = input(f"Соцпакет [{'Да' if vacancy['social_package'] else 'Нет'}] (да/нет): ").strip()
    if social_input:
        ok, result = validate_bool(social_input)
        if ok:
            vacancy['social_package'] = result
    
    vacancy['probation_period'] = edit_field("Исп.срок", check_probation_edit, vacancy['probation_period'])
    
    print("✓ Вакансия изменена!")
    save_vacancies()

def delete_vacancy():
    """Удаление вакансии"""
    if not vacancies_db:
        print("Нет вакансий!")
        return
    
    print("\nУДАЛЕНИЕ ВАКАНСИИ")
    
    #Показать список
    for i, v in enumerate(vacancies_db, 1):
        print(f"{i}. {v['position']}")
    
    #Выбрать для удаления
    choice = get_input(f"Номер (1-{len(vacancies_db)})",
                      lambda v: check_vacancy_choice(v, len(vacancies_db)))
    
    if choice > 0:
        deleted = vacancies_db.pop(choice-1)
        print(f"Вакансия '{deleted['position']}' удалена!")
        save_vacancies()

def show_vacancies(vacancies, title=""):
    """Показать вакансии"""
    if not vacancies:
        print("Нет данных")
        return
    
    print(f"\n{title if title else 'ВАКАНСИИ'}")
    print("-" * 70)
    print(f"{'№':3} | {'Должность':20} | {'Образование':18} | {'Оклад':>8} | Стаж | Исп.срок | Соцпакет")
    print("-" * 70)
    
    for i, v in enumerate(vacancies, 1):
        social = "Да" if v['social_package'] else "Нет"
        print(f"{i:3} | {v['position'][:20]:20} | {v['education'][:18]:18} | "
              f"{v['min_salary']:>8}₽ | {v['experience']:4}л | "
              f"{v['probation_period']:8}мес | {social}")
    
    print("-" * 70)
    print(f"Всего: {len(vacancies)}")

#ФУНКЦИИ ДЛЯ ОТЧЕТОВ

def generate_report1():
    """Отчет 1: Все вакансии по образованию и должности"""
    if vacancies_db:
        sorted_vac = quick_sort(vacancies_db, key_func=key_report1)
        show_vacancies(sorted_vac, "ОТЧЕТ 1: ВСЕ ВАКАНСИИ (Образование↑ + Должность↑)")

def generate_report2():
    """Отчет 2: Вакансии с испытательным сроком ≥ 2 месяцев"""
    filtered = [v for v in vacancies_db if v['probation_period'] >= 2]
    if filtered:
        sorted_vac = quick_sort(filtered, key_func=key_report2)
        show_vacancies(sorted_vac, "ОТЧЕТ 2: ИСПЫТАТЕЛЬНЫЙ СРОК ≥ 2 МЕСЯЦЕВ")
    else:
        print("Нет вакансий с испытательным сроком ≥ 2 месяцев")

def generate_report3():
    """Отчет 3: Вакансии по диапазону зарплат"""
    
    def check_min_salary(value):
        return validate_int(value, 0, 1000000)
    
    n1 = get_input("Мин.оклад: ", check_min_salary)
    
    def check_max_salary_for_report(value):
        return check_max_salary(value, n1)
    
    n2 = get_input("Макс.оклад: ", check_max_salary_for_report)
    
    filtered = [v for v in vacancies_db if n1 <= v['min_salary'] <= n2]
    if filtered:
        sorted_vac = quick_sort(filtered, key_func=key_report3)
        show_vacancies(sorted_vac, f"ОТЧЕТ 3: ОКЛАД ОТ {n1} ДО {n2} РУБ.")
    else:
        print(f"Нет вакансий с окладом от {n1} до {n2} рублей")

#ГЛАВНОЕ МЕНЮ

def main_menu():
    """Главное меню программы"""
    options = [
        ("Показать все вакансии", lambda: show_vacancies(vacancies_db, "ВСЕ ВАКАНСИИ")),
        ("Добавить вакансию", add_vacancy),
        ("Изменить вакансию", edit_vacancy),
        ("Удалить вакансию", delete_vacancy),
        ("Отчет 1: Все вакансии", generate_report1),
        ("Отчет 2: Испытательный срок ≥ 2 мес", generate_report2),
        ("Отчет 3: По диапазону зарплат", generate_report3),
        ("Сохранить базу", save_vacancies),
        ("Выход", None)
    ]
    
    while True:
        print("\n" + "="*60)
        print(f"КАДРОВОЕ АГЕНТСТВО (вакансий: {len(vacancies_db)})")
        print("="*60)
        
        for i, (text, _) in enumerate(options, 1):
            print(f"{i}. {text}")
        
        choice = get_input("\nВыбор (1-9): ", check_menu_choice)
        
        if choice == 9:
            print("\nДо свидания!")
            break
        
        _, action = options[choice-1]
        if action:
            action()
            if choice != 9:
                input("\nEnter для продолжения...")

#ЗАПУСК ПРОГРАММЫ

if __name__ == "__main__":
    print("\n" + "="*60)
    print("КАДРОВОЕ АГЕНТСТВО")
    print("="*60)
    
    if load_vacancies():
        main_menu()
    else:
        print("\nСоздайте файл vacancies.txt и перезапустите программу.")
