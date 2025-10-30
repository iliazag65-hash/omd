from json_dict_processing import create_processor
from processing_utils import process_year
from typing import Dict, Any

CONFIG_PRIZE = {
    'prize_amount': ['prizeAmount'],
    'prize_amount_adjusted': ['prizeAmountAdjusted'],
    'award_year': (['awardYear'], process_year),
    'category_en': ['category', 'en'],
    'prize_status': ['prizeStatus'],
    'motivation': ['motivation', 'en']
}

def prize_processor() -> Dict[str, Any]:
    """
    создает готовый процессор для списка призов.
    """
    return create_processor(CONFIG_PRIZE, list_processor=True)

process_prizes = prize_processor()

# Валидация
def _run_tests():
    test_prize_list = [
        {
            'prizeAmount': 10000000,
            'prizeAmountAdjusted': 15547541,
            'awardYear': '2001',
            'category': {'en': 'Economic Sciences'},
            'prizeStatus': 'received',
            'motivation': {'en': 'for their analysis'}
        },
        {
            'prizeAmount': 630000,
            'prizeAmountAdjusted': 4304697,
            'awardYear': '1975',
            'category': {'en': 'Physics'},
            'prizeStatus': 'received',
            'motivation': {'en': 'for the discovery'}
        }
    ]
    
    processed = process_prizes(test_prize_list)
    
    assert len(processed) == 2
    assert processed[0]['award_year'] == 2001
    assert processed[0]['category_en'] == 'Economic Sciences'
    assert processed[0]['motivation'] == 'for their analysis'
    assert processed[1]['prize_amount'] == 630000
    assert processed[1]['category_en'] == 'Physics'
    
    print("Тесты пройдены успешно")

if __name__ == "__main__":
    _run_tests()