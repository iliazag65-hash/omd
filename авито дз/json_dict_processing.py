from functools import partial, reduce
from typing import List, Dict, Any, Union, Callable, Tuple

# чтобы не захламлять тайпхинты определю типы здесь 
ConfigDict = Dict[str, Union[List[Union[str, int]], Tuple[List[Union[str, int]], Callable[[Any], Any]]]]
ValueProcessor = Callable[[Any], Any]
SingleDictProcessor = Callable[[Dict[str, Any]], Dict[str, Any]]
ListDictProcessor = Callable[[List[Dict[str, Any]]], List[Dict[str, Any]]]

def extract_nested_value(obj: Union[Dict, List, None], keys: List[Union[str, int]]) -> Any:
    """
    Извлекает значение из вложенных структур данных по цепочке ключей.
    На вход принимаем объект, из которого извлекаются данные и список ключей/индексов для последовательного доступа,
    а возвращаем извлеченное значение или none
    """
    if not isinstance(keys, list) or not keys:
        return None

    def _safe_get(value: Any, key: Union[str, int]) -> Any:
        """Безопасное извлечение ключа или индекса."""
        if value is None:
            return None
        try:
            # Поддержка как словарей (по ключу), так и списков (по индексу)
            if isinstance(value, list) and isinstance(key, int):
                return value[key]
            if isinstance(value, dict):
                return value.get(key)
        except (KeyError, IndexError, TypeError):
            return None
        return None
    try:
        return reduce(_safe_get, keys, obj)
    except Exception:
        return None

def process_dictionary_with_config(dictionary: Dict[str, Any], config: ConfigDict) -> Dict[str, Any]:
    """
    Обрабатывает один словарь согласно конфигу.
    На вход принимает исходный словарь для обработки и словарь конфигурации.
    Возвращает плоский словарь с обработанными данными.
    """
    processed_dict = {}
    if not isinstance(dictionary, dict) or not isinstance(config, dict):
        return processed_dict

    for new_key, config_value in config.items():
        raw_value = None
        
        try:
            if isinstance(config_value, list):
                path_list = config_value
                raw_value = extract_nested_value(dictionary, path_list)
                processed_dict[new_key] = raw_value
                
            elif isinstance(config_value, tuple) and len(config_value) == 2:
                path_list, process_func = config_value
                raw_value = extract_nested_value(dictionary, path_list)
                processed_dict[new_key] = process_func(raw_value)
                
        except Exception:
            processed_dict[new_key] = None
            
    return processed_dict

def process_list_of_dicts_with_config(list_of_dicts: List[Dict[str, Any]], config: ConfigDict) -> List[Dict[str, Any]]:
    """
    Обрабатывает список словарей, применяя к каждому 
    process_dictionary_with_config.
    Принимает список словарей для обработки и словарь конфигурации, а возвращает список обработанных плоских словарей.
    """
    if not isinstance(list_of_dicts, list):
        return []
    
    return [process_dictionary_with_config(d, config) for d in list_of_dicts]

def create_processor(config: ConfigDict, list_processor: bool = False) -> Union[SingleDictProcessor, ListDictProcessor]:
    """
    Создает процессор с определенной конфигурацией.
   Принимает словарь конфигурации и индикатор, который если True, возвращаемая функция будет 
    обрабатывать список словарей, а если False, то один словарь.
    Возвращает функцию-обработчик (процессор).
    """
    if list_processor:
        # Возвращаем частично примененную функцию для списка
        return partial(process_list_of_dicts_with_config, config=config)
    else:
        # Возвращаем частично примененную функцию для одного словаря
        return partial(process_dictionary_with_config, config=config)

# Валидация
def _run_tests():
    # Тест для extract_nested_value
    test_obj = {'a': {'b': [None, {'c': 100}]}}
    assert extract_nested_value(test_obj, ['a', 'b', 1, 'c']) == 100
    assert extract_nested_value(test_obj, ['a', 'x']) is None
    assert extract_nested_value(test_obj, ['a', 'b', 0]) is None
    assert extract_nested_value(test_obj, ['a', 'b', 5]) is None
    assert extract_nested_value(None, ['a']) is None
    
    # Тест для process_dictionary_with_config
    test_dict = {
        'user': {'name': 'Pipipupu', 'details': {'age': 30}},
        'date': '2024-01-01'
    }
    
    def _add_ten(val):
        return val + 10 if isinstance(val, int) else None
        
    def _get_year(val):
        return int(val.split('-')[0]) if isinstance(val, str) else None

    test_config = {
        'full_name': ['user', 'name'],
        'age_plus_10': (['user', 'details', 'age'], _add_ten),
        'year': (['date'], _get_year),
        'missing_field': ['user', 'location']
    }
    
    processed = process_dictionary_with_config(test_dict, test_config)
    
    assert processed['full_name'] == 'Pipipupu'
    assert processed['age_plus_10'] == 40
    assert processed['year'] == 2024
    assert processed['missing_field'] is None
    
    # Тест для create_processor
    test_list = [test_dict, {'user': {'name': 'TEST'}, 'date': '2023-05-05'}]
    list_proc = create_processor(test_config, list_processor=True)
    processed_list = list_proc(test_list)
    
    assert len(processed_list) == 2
    assert processed_list[0]['full_name'] == 'Pipipupu'
    assert processed_list[1]['full_name'] == 'TEST'
    assert processed_list[1]['age_plus_10'] is None
    assert processed_list[1]['year'] == 2023
    
    print("Тесты пройдены успешно")

if __name__ == "__main__":
    _run_tests()

