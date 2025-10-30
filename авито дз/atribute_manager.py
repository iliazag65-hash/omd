def add_attribute(data_list, new_field_name, calculation_func):
    """
    Добавляет новое поле в каждый словарь в списке, 
    вычисляя его значение с помощью переданной функции.
    """
    for item in data_list:
        item[new_field_name] = calculation_func(item)
    return data_list

def remove_attribute(data_list, field_name):
    """
    Удаляет указанное поле из всех словарей в списке.
    """
    for item in data_list:
        item.pop(field_name, None) 
    return data_list
