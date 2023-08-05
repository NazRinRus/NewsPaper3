from django import template

register = template.Library()


@register.filter()
def censor(value):
    CENSORED_LIST = ['редиска', 'придурок', 'урод', 'глупый', 'тупой', 'злой', 'дурак', 'козел']

    if isinstance(value, str):
        str1 = value

        for censor_element in CENSORED_LIST:
            new_text = str1.replace(censor_element, censor_element[0] + "*" * (len(censor_element) - 1))  # замена по нижнему регистру
            str1 = new_text
            new_text = str1.replace(censor_element.capitalize(), censor_element[0].capitalize() + "*" * (len(censor_element) - 1))  # замена по верхнему регистру
            str1 = new_text

        value = str1
    else:
        raise TypeError('Фильтр "censor" может быть применен только к текстовому типу данных')

    return f'{value}'