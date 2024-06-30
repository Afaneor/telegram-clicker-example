import re
from enum import Enum
from typing import Any


def get_correct_data(row_data: Any, default: Any = ''):
    """Получение корректных значений."""
    return clear_data(row_data=row_data) if row_data else default


def delete_html(row_data: Any) -> Any:
    """Очистить информацию от html."""
    if isinstance(row_data, str):
        row_data = re.sub(r'\<[^>]*\>', '', row_data)
        row_data = re.sub(r'&nbsp;', '', row_data)
        row_data = re.sub(r'&bull;', '', row_data)
        row_data = re.sub(r'&quot;', '\"', row_data)
        return row_data.strip()

    return row_data


def clear_data(row_data: Any) -> Any:
    """Очистка данных от пробелов и лишних символов."""
    if isinstance(row_data, str):
        row_data = row_data.strip()
        row_data = row_data.strip('\n')
        row_data = delete_html(row_data=row_data)

    return row_data
