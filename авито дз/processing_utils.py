def process_year(date_string):
    """
    Извлекает год из строки даты (формат "YYYY-MM-DD" или "YYYY").
    Возвращает год как int или none.
    """
    if not isinstance(date_string, str):
        return None
    try:
        year_str = date_string[:4]
        return int(year_str)
    except (ValueError, TypeError):
        return None