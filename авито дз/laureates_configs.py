from json_dict_processing import create_processor
from processing_utils import process_year
import prizes_configs as pc 
from typing import Callable, Dict, Any, Union

#функция для преобразования айдишника в число
def process_id(id_str: str) -> Union[int, None]:
    try:
        return int(id_str)
    except (ValueError, TypeError):
        return None

PRIZES_PROCESSOR_FUNC = pc.prize_processor()

# человек
CONFIG_PERSON = {
    'id': (['id'], process_id),
    'name': ['knownName', 'en'],
    'gender': ['gender'],
    'birth_year': (['birth', 'date'], process_year),
    'country_birth': ['birth', 'place', 'country', 'en'],
    'country_now': ['birth', 'place', 'countryNow', 'en'],
    'prizes_relevant': (['nobelPrizes'], PRIZES_PROCESSOR_FUNC)
}

# организация
CONFIG_ORG = {
    'id': (['id'], process_id),
    'name': ['orgName', 'en'],
    'founded_year': (['founded', 'date'], process_year),
    'country_founded': ['founded', 'place', 'country', 'en'],
    'country_now': ['founded', 'place', 'countryNow', 'en'],
    'prizes_relevant': (['nobelPrizes'], PRIZES_PROCESSOR_FUNC)
}

def person_processor() -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    """
    Создает процессор для лауреата человека.
    """
    return create_processor(CONFIG_PERSON, list_processor=False)

def org_processor() -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    """
    Создаюет процессор для организации.
    """
    return create_processor(CONFIG_ORG, list_processor=False)

process_persons = person_processor()
process_orgs = org_processor()

# Валидация
def _run_tests():
    # Пример человека
    test_person = {
        'id': '745',
        'knownName': {'en': 'A. Michael Spence'},
        'gender': 'male',
        'birth': {
            'date': '1943-00-00',
            'place': {
                'country': {'en': 'USA'},
                'countryNow': {'en': 'USA'}
            }
        },
        'nobelPrizes': [
            {
                'awardYear': '2001',
                'category': {'en': 'Economic Sciences'},
                'prizeAmount': 10000000
            }
        ]
    }
    
    # Пример организации
    test_org = {
        'id': '525',
        'orgName': {'en': 'AAABBBEEE'},
        'founded': {
            'date': '2000-00-00',
            'place': {
                'country': {'en': 'UBEBE'},
                'countryNow': {'en': 'BUBABA'}
            }
        },
        'nobelPrizes': [
            {'awardYear': '1963', 'category': {'en': 'POPOPU'}}
        ]
    }
    
    processed_p = process_persons(test_person)
    processed_o = process_orgs(test_org)
    
    assert processed_p['id'] == 745
    assert processed_p['name'] == 'A. Michael Spence'
    assert processed_p['birth_year'] == 1943
    assert processed_p['country_now'] == 'USA'
    assert len(processed_p['prizes_relevant']) == 1
    assert processed_p['prizes_relevant'][0]['award_year'] == 2001
    assert processed_p['prizes_relevant'][0]['category_en'] == 'Economic Sciences'

    assert processed_o['id'] == 525
    assert processed_o['name'] == 'AAABBBEEE'
    assert processed_o['founded_year'] == 2000
    assert len(processed_o['prizes_relevant']) == 1
    assert processed_o['prizes_relevant'][0]['award_year'] == 1963
    
    print("Тесты пройдены успешно")

if __name__ == "__main__":
    _run_tests()