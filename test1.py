CENSORED_LIST = ['редиска', 'придурок', 'урод', 'глупый', 'тупой', 'злой', 'дурак', 'козел', ]
str1 = 'привет урод, как дела? Ты такой глупый урод, а еще я думаю ты козел и дурак. Все пока придурок! Редиска'

for censor_element in CENSORED_LIST:
    new_text = str1.replace(censor_element, censor_element[0] + "*" * (len(censor_element)-1)) # замена по нижнему регистру
    str1 = new_text
    new_text = str1.replace(censor_element.capitalize(), censor_element[0].capitalize() + "*" * (len(censor_element) - 1)) # замена по верхнему регистру
    str1 = new_text
print(new_text)