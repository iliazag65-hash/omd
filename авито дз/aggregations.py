import statistics
from collections import Counter
from typing import List, Union, Any, Tuple, Dict

def calculate_mean(data_list: List[Union[int, float]]) -> Union[float, None]:
    """Рассчитывает среднее значение списка чисел"""
    if not data_list:
        return None
    try:
        return statistics.mean(data_list)
    except Exception:
        return None

def calculate_median(data_list: List[Union[int, float]]) -> Union[float, None]:
    """Рассчитывает медиану списка чисел"""
    if not data_list:
        return None
    try:
        return statistics.median(data_list)
    except Exception:
        return None

def calculate_mode(data_list: List[Any]) -> Union[List[Any], None]:
    """
    Находит моду, возвращает список мод если их несколько.
    """
    if not data_list:
        return None
    
    counts = Counter(data_list)
    if not counts:
        return None
        
    max_count = max(counts.values())
    modes = [item for item, count in counts.items() if count == max_count]
    return modes


def get_top_n(data_list: List[Dict[str, Any]], key_field: str, n: int = 10) -> List[Tuple[Any, int]]:
    """
    Находит топ N самых часто встречающихся значений для заданного поля 
    в списке словарей. (Для простой частотной агрегации)
    Принимаеи на вход список словарей, поле по которому считается частота, количество элементов в топе.
    Возвращает список кортежей (значение, частота)
    """
    values = [item.get(key_field) for item in data_list if item.get(key_field) is not None]
    counts = Counter(values)
    return counts.most_common(n)
