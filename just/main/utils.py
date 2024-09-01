import re
from django.core.exceptions import ValidationError

def clean_phone(phone):
    phone = re.sub(r'\D', '', phone)  # Видалити всі нецифрові символи

    # Перевірити та нормалізувати номер
    if phone.startswith('380') and len(phone) == 12:
        phone = phone[2:]  # Видалити '380'
    elif phone.startswith('80') and len(phone) == 11:
        phone = phone[1:]  # Видалити '8'
    elif phone.startswith('0') and len(phone) == 10:
        pass  # Нічого не робити, номер вже нормальний
    elif len(phone) == 9 and not phone.startswith('0'):
        phone = '0' + phone  # Додати '0' на початок
    else:
        raise ValidationError('invalid_format')

    return phone