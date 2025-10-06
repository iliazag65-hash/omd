def existing_departamets(df: list[list[str]]) -> list[str]:
    """Функция принимает на вход таблицу с данными и возвращает список всех существующих департаментов"""
    departaments = []
    for i in range(len(df)-1):  # -1 тк первая строка нам не нужна
        dep = df[i+1][1]
        if dep not in departaments:
            departaments.append(dep)
    return departaments


def struct_of_dep(df: list[list[str]]) -> dict[str, list[str]]:
    """Функция принимает на вход таблицу с данными и выводит структуру каждого департаментав виде: 
    Название_департамента:
            -команда_1
              ....
            -команда_N
    возвращает функция структуру департамента в виде словаря"""

    departments = existing_departamets(df)
    struct = {dep: [] for dep in departments}
    for i in range(len(df)-1):
        if df[i+1][2] not in struct[df[i+1][1]]:
            struct[df[i+1][1]].append(df[i+1][2])

    print("СТРУКТУРА КОМПАНИИ\n")
    for department, teams in struct.items():
        print(f"{department}:")
        for team in teams:
            print(f"\t-{team}")
        print()
    return struct


def summary_of_dep(df: list[list[str]]) -> dict[str, list[int]]:
    """Функция принимает на вход таблицу с данными и выводит сводку по департаментам в виде:
     Название_департамента:
            -Численность департамента: int
            -Вилка зарплат: int-int
            -Средняя зарпата: float
    Также функция возвращает сводку в виде словаря"""

    departments = existing_departamets(df)
    department_summary = {dep: [0, 0, 0, 0] for dep in departments}  # первое значение в массиве - численность, второе - мин зп, третье - макс зп, четвертое - сумма
    
    for dep in departments:
        department_summary[dep][1] = float('inf')  # мин зп
        department_summary[dep][2] = 0  # макс зп

    for i in range(len(df)-1):
        department = df[i+1][1]
        salary = int(df[i+1][5])
        department_summary[department][0] += 1
        department_summary[department][3] += salary
        department_summary[department][1] = min(department_summary[department][1], salary)  # мин зп
        department_summary[department][2] = max(department_summary[department][2], salary)  # макс зп

    for dep in departments:
        if department_summary[dep][0] > 0:
            avg_salary = department_summary[dep][3] / department_summary[dep][0]
            department_summary[dep].append(avg_salary)  # добавляем среднюю зп как 5-й элемент
        else:
            department_summary[dep].append(0)

    print("СВОДКА ПО ДЕПАРТАМЕНТАМ\n")
    for department, summary in department_summary.items():
        print(f"{department}:")
        print(f'-Численность департамента: {summary[0]}')
        print(f'-Вилка зарплат: {summary[1]}-{summary[2]}')
        print(f'-Средняя зарплата: {round(summary[4], 2)}')
        print()
    
    return department_summary


def save_department_summary_to_csv(df: list[list[str]], filename: str = 'departament_summary.csv') -> bool:
    """Принимает на вход таблицу с данными, название файла и сохраняет сводку из предыдущего пункта в csv-файл"""

    csv_content = "department;employees_count;min_salary;max_salary;avg_salary\n"
    department_summary = summary_of_dep(df)
    
    for department, data in department_summary.items():
        # Экранируем специальные символы в названии отдела
        dep_name = str(department).replace('"', '""')
        if ';' in dep_name or '\n' in dep_name or '"' in dep_name:
            dep_name = f'"{dep_name}"'
        
        row = f"{dep_name};{data[0]};{data[1]};{data[2]};{round(data[4], 2)}\n"
        csv_content += row
    
    # Записываем в файл
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(csv_content)
        print(f"Данные успешно сохранены в файл: {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")


if __name__ == "__main__":
    with open('Corp_Summary.csv', 'r', encoding='utf-8') as file:
        df = []  # 1-ый индекс - строка, 2-ой - столбец
        for line in file:
            row = line.strip().split(';')
            df.append(row)

    print('МЕНЮ')
    print('1. Структура департаментов')
    print('2. Сводка по департаментам')
    print('3. Сохранить сводку')
    print()
    options = {"1": 1, "2": 2, "3": 3}
    option = ''
    while option not in options:
        print("Выберите: {}/{}/{}".format(*options))
        print('='*40, '\n')
        option = input()

    if options[option] == 1:
        struct_of_dep(df)

    if options[option] == 2:
        summary_of_dep(df)

    if options[option] == 3:
        save_department_summary_to_csv(df)
        