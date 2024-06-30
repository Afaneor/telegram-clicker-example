from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

INN_MIN_LENGTH, INN_MAX_LENGTH = 10, 12


def inn_sum_helper(internal_value: str) -> str:
    """Вспомогательная функция для проверки ИНН."""
    index = (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
    pairs = zip(
        index[11 - len(internal_value):],  # noqa: WPS432
        [int(number) for number in internal_value],
    )
    return str(sum([k * v for k, v in pairs]) % 11 % 10)  # noqa: WPS432, WPS111, WPS221, E501


def inn_validator(value_to_check: str) -> None:
    """Проверка валидности ИНН."""
    inn_length = len(value_to_check)
    if inn_length not in {INN_MIN_LENGTH, INN_MAX_LENGTH}:
        raise ValidationError(_('Должно быть введено 10 или 12 цифр'))
    elif inn_length == INN_MIN_LENGTH:
        if value_to_check[-1] != inn_sum_helper(value_to_check[:-1]):
            raise ValidationError(_('Введен некорректный ИНН'))
    elif inn_length == INN_MAX_LENGTH:
        str1 = inn_sum_helper(value_to_check[:-2])
        str2 = inn_sum_helper(value_to_check[:-1])
        if value_to_check[-2:] != str1 + str2:
            raise ValidationError(_('Введен некорректный ИНН'))
