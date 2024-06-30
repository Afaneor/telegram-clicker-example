import logging
import re
import time

import requests
from bs4 import BeautifulSoup

from server.apps.investment_object.models import (
    EconomicActivity,
    InvestmentObject,
    ReadyBusiness,
    TransactionForm,
)
from server.apps.services.enums import ObjectType, TransactionFormType

logger = logging.getLogger('django')

MAP_FOR_OKVED = {
    'Магазины и торговля': '47',
    'Ресторанный бизнес': '56',
    'Производство': '10-33',
    'Сфера красоты': '96',
    'Бизнес в сфере услуг': '82',
    'Интернет магазины': '47.91',
    'Медицинские центры': '86',
    'Прочее': '',
    'Гостиничный бизнес': '55',
    'Арендный бизнес': '68.2',
    'Детские центры и сады': '85.11',
    'Готовый бизнес за рубежом': '',
    'Автобизнес': '45',
    'Квесты, атракционы, сауны, развлечения': '93.2',
    'Аптечный бизнес': '47.73',
    'IT-компании': '62',
    'Строительный бизнес': '41',
    'Готовый бизнес под ключ': '',
    'Транспортный бизнес': '49.41',
    'Доли в бизнесе': '',
    'Страховой и финансовый бизнес': '64',
    'Коммерческая недвижимость': '68',
    'Сельское хозяйство': '01',
    'Бизнес по цене активов': '74.90',
    'Месторождения и карьеры': '08',
    'Туристический бизнес': '79.1',
    }


def ready_business():
    """Парсинг готового бизнеса с сайта alterainvest.ru."""
    # Формируем запрос к api для получения количества страниц.
    all_business_response = requests.get(
        url=(
            'https://alterainvest.ru/msk/products/'
        ),
        timeout=15,
    )
    all_business_data = BeautifulSoup(all_business_response.text, 'html.parser')
    number_pages = re.sub(
        '[\n\t\r ]',
        '',
        all_business_data.find('ul', class_='al-pagination mb20').contents[29].text,
    ).strip()
    for page_number in range(1, int(number_pages)+1):
        logger.info(f'Анализ страницы {page_number}')
        business_page_response = requests.get(
            url=(
                f'https://alterainvest.ru/msk/products/page-{page_number}'
            ),
            timeout=15,
        )
        business_page_data = BeautifulSoup(
            business_page_response.text,
            'html.parser',
        )

        for base_business_data in business_page_data.find_all('div', class_='al-cart-min _average al-box-white'):
            business_detail_url = base_business_data.contents[1].attrs.get('href')
            business_response = requests.get(
                url=(
                    f'https://alterainvest.ru{business_detail_url}'
                ),
                timeout=15,
            )
            business_data = BeautifulSoup(
                business_response.text,
                'html.parser',
            )

            # Дополнительные данные.
            extra_data = {
                re.sub('[\n\t\r ]', '', business_characteristics.contents[1].text).strip():
                    re.sub('[\n\t\r ]', '', business_characteristics.contents[3].text).strip()
                for business_characteristics in business_data.find_all('div', class_='col-4 mb16')
                if len(business_characteristics.contents) > 3
            }

            # Название бизнеса.
            name = re.sub(
                '[\n\t\r ]',
                '',
                business_data.find('h1', class_='heading3 mb12').text,
            ).strip()

            # Описание бизнеса.
            if business_data.find('div', class_='al-textcreator'):
                description = re.sub(
                    '[\n\t\r ]',
                    '',
                    business_data.find('div', class_='al-textcreator').text,
                ).strip()
            else:
                description = ''

            # Главная фотография.
            main_photo_url = business_data.find_all(
                'img',
                class_='image-sqr',
            )[0].attrs.get('src')

            # Стоимость.
            if extra_data.get('Стоимость'):
                cost = extra_data.get('Стоимость').replace(' ', '')[:-1]
            else:
                cost = None

            transaction_form, tf_created = (
                TransactionForm.objects.get_or_create(
                    name='Продажа',
                    transaction_form_type=TransactionFormType.SALE,
                )
            )
            investment_object, io_created = InvestmentObject.objects.update_or_create(
                name=name.split('#')[0],
                defaults={
                    'main_photo_url':
                        f'https://alterainvest.ru{main_photo_url}',
                    'object_type': ObjectType.READY_BUSINESS,
                    'transaction_form': transaction_form,
                    'cost': cost,
                    'location': (
                        extra_data.get('Район')
                        if extra_data.get('Район') != 'По запросу'
                        else ''
                    ),
                    'url': f'https://alterainvest.ru{business_detail_url}',
                    'data_source': 'alterainvest.ru',
                },
            )

            if extra_data.get('Сфера деятельности'):
                code = MAP_FOR_OKVED.get(
                    extra_data.get('Сфера деятельности').split(',')[0]
                )
                try:
                    economic_activity = EconomicActivity.objects.get(code=code)
                except EconomicActivity.DoesNotExist:
                    continue
                investment_object.economic_activities.add(economic_activity.id)

            ReadyBusiness.objects.update_or_create(
                investment_object=investment_object,
                defaults={
                    'external_id': name.split('#')[1],
                    'description': description,
                    'extra_data': extra_data,
                },
            )
            logger.info(f'Запись с id {name.split("#")[1]} добавлена')

        time.sleep(1)
