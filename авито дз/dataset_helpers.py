from collections import defaultdict
from typing import List, Dict, Any, Callable, Tuple, Union, Literal

# Определим некоторые типы здесь чтобы не захламлять тайпхинты
LaureateRecord = Dict[str, Any]
ConditionValue = Union[Any, Callable[[Any], bool]]
AggregationFunc = Callable[[List[Any]], Union[int, float, None]]
GroupedData = Dict[Tuple[Any], List[LaureateRecord]]

def filter_data(data_list: List[LaureateRecord], conditions: Dict[str, ConditionValue]) -> List[LaureateRecord]:
    """
    Фильтрует список словарей по заданным условиям (аналог WHERE в SQL).
    """
    filtered_data = []
    
    # Функция для проверки, соответствует словарь всем условиям или нет
    def check_conditions(item: LaureateRecord) -> bool:
        for field, condition in conditions.items():
            value = item.get(field)
            
            if callable(condition):
                if not condition(value):
                    return False
            elif value != condition:
                return False
        return True

    for item in data_list:
        if check_conditions(item):
            filtered_data.append(item)
            
    return filtered_data


def get_column_data(data_list: List[Dict[str, Any]], field_name: str) -> List[Any]:
    """
    Извлекает список значений по заданному полю из списка словарей.
    Аналог data_frame['field_name'].
    """
    return [d.get(field_name) for d in data_list]