from typing import Any, Dict, List

import requests

from server.apps.investment_object.models.investment_object import (
    InvestmentObject,
)
from server.apps.services.parsing.xlsx.base import clear_data, get_correct_data

URL_MAPPING: Dict[int, str] = {
    # ТЕХНОПАРКИ. https://investmoscow.ru/business/technoparks
    1: 'https://api.investmoscow.ru/investmoscow/industry/v1/techpark/get?id={id}',
    # ПЛОЩАДКИ ОЭЗ "ТЕХНОПОЛИC".
    # https://investmoscow.ru/business/sez-technopolis-moscow
    2: 'https://api.investmoscow.ru/investmoscow/industry/v1/economiczone/getseztechnopolismoscowsite?id={id}',
    # ИНВЕСТИЦИОННЫЙ КАТАЛОГ. https://investmoscow.ru/business/invest-catalog
    3: 'https://api.investmoscow.ru/investmoscow/industry/v1/investcatalog/getobject?id={id}',
    # РЕЕСТР ПРОМПЛОЩАДОК. https://investmoscow.ru/business/site-list
    4: 'https://api.investmoscow.ru/investmoscow/industry/v1/industryzone/getroomforindustrial?id={id}',
    # РЕЕСТР ПРОМПЛОЩАДОК. ЗЕМЕЛЬНЫЕ УЧАСТКИ.
    # https://investmoscow.ru/business/site-list
    5: 'https://api.investmoscow.ru/investmoscow/industry/v1/industryzone/getsiteforindustrial?id={id}',
    # КРТ.
    # https://investmoscow.ru/business/krt
    6: 'https://api.investmoscow.ru/investmoscow/industry/v1/krt/getById?id={id}'
}


def parsing_technopark_1(
    investment_site: InvestmentObject,
):
    """Парсинг технопарков."""
    # Формируем url и совершаем запрос к api.
    url_for_parsing = URL_MAPPING.get(
        investment_site.object_type,
    ).format(
        id=investment_site.external_id,
    )
    response_json = requests.get(
        url=url_for_parsing,
        headers={'Content-Type': 'application/json'},
        timeout=15,
    ).json()

    generic_info_tab = response_json.get('genericInfoTab')
    contact_info_tab = response_json.get('contactInfoTab')

    extra_data = {
        # Общая информация.
        'Наименование': get_correct_data(generic_info_tab.get('name')),
        'Общая информация': get_correct_data(generic_info_tab.get('generalInfo')),
        'Специализация': ', '.join(generic_info_tab.get('specializations', [])),
        # Контакты.
        'Адрес': get_correct_data(contact_info_tab.get('address')),
        'Управляющая компания':
            get_correct_data(contact_info_tab.get('managementCompany')),
        'Url сайта': get_correct_data(contact_info_tab.get('url')),
        'Контактное лицо':
            get_correct_data(contact_info_tab.get('contactPerson')),
        'Телефон': get_correct_data(contact_info_tab.get('phone')),
    }

    # Добавляем фотографии, если они есть
    investment_site.photo_urls = response_json.get('photoUrls')
    investment_site.extra_data = extra_data
    investment_site.url = (
        'https://investmoscow.ru/business/'
        f'technoparks/{investment_site.external_id}'
    )
    investment_site.save(
        update_fields=['photo_urls', 'extra_data', 'url'],
    )


def parsing_technopolis_2(
    investment_site: InvestmentObject,
):
    """Парсинг технополисов."""
    # Формируем url и совершаем запрос к api.
    url_for_parsing = URL_MAPPING.get(
        investment_site.object_type,
    ).format(
        id=investment_site.external_id,
    )
    response_json = requests.get(
        url=url_for_parsing,
        headers={'Content-Type': 'application/json'},
        timeout=15,
    ).json()

    generic_info_tab = response_json.get('genericInfoTab')
    engineering_infrastructure_tab = response_json.get(
        'engineeringInfrastructureTab',
    )

    extra_data = {
        # Общая информация.
        'Наименование':
            get_correct_data(generic_info_tab.get('name')),
        'Округ':
            get_correct_data(generic_info_tab.get('okrug')),
        'Общая площадь, м2, га':
            get_correct_data(generic_info_tab.get('area')),
        'Количество резидентов особой экономической зоны':
            get_correct_data(generic_info_tab.get('residentsCount')),
        'Объем инвестиций, млрд руб':
            get_correct_data(generic_info_tab.get('investmentSize')),
        'Количество рабочих мест':
            get_correct_data(generic_info_tab.get('workplacesCount')),
        # Инженерная инфраструктура.
        'Электроснабжение. Максимально допустимая мощность.':
            get_correct_data(
                engineering_infrastructure_tab.get(
                    'powerSupplyMaxAvailablePower',
                ),
            ),
        'Электроснабжение. Свободная мощность':
            get_correct_data(
                engineering_infrastructure_tab.get('powerSupplyFreePower'),
            ),
        'Водоснабжение. Максимально допустимая мощность.':
            get_correct_data(
                engineering_infrastructure_tab.get(
                    'waterSupplyMaxAvailablePower',
                ),
            ),
        'Водоснабжение. Свободная мощность':
            get_correct_data(
                engineering_infrastructure_tab.get('waterSupplyFreePower'),
            ),
        'Водоотведение. Максимально допустимая мощность.':
            get_correct_data(
                engineering_infrastructure_tab.get(
                    'sewersMaxAvailablePower',
                ),
            ),
        'Водоотведение. Свободная мощность':
            get_correct_data(
                engineering_infrastructure_tab.get('sewersFreePower'),
            ),
        'Теплоснабжение. Максимально допустимая мощность.':
            get_correct_data(
                engineering_infrastructure_tab.get(
                    'heatingSupplyMaxAvailablePower',
                ),
            ),
        'Теплоснабжение. Свободная мощность':
            get_correct_data(
                engineering_infrastructure_tab.get(
                    'heatingSupplyFreePower',
                ),
            ),
    }

    # Добавляем фотографии, если они есть
    investment_site.photo_urls = response_json.get('photoUrls')
    investment_site.extra_data = extra_data
    investment_site.url = (
        'https://investmoscow.ru/business/'
        f'sez-technopolis-moscow/{investment_site.external_id}'
    )
    investment_site.save(
        update_fields=['photo_urls', 'extra_data', 'url'],
    )


def parsing_investment_catalog_3(
    investment_site: InvestmentObject,
):
    """Парсинг технопарков."""
    # Формируем url и совершаем запрос к api.
    url_for_parsing = URL_MAPPING.get(
        investment_site.object_type,
    ).format(
        id=investment_site.external_id,
    )
    response_json = requests.get(
        url=url_for_parsing,
        headers={'Content-Type': 'application/json'},
        timeout=15,
    ).json()

    building_tab = response_json.get('buildingTab')
    land_plot_tab = response_json.get('landPlotTab')

    extra_data = {
        # Здание.
        'Количество объектов': clear_data(building_tab.get('count', '0')),
        'Год постройки': get_correct_data(building_tab.get('year')),
        'Площадь постройки': clear_data(building_tab.get('area', '0')),
        # Земельный участок.
        'Площадь': get_correct_data(land_plot_tab.get('area')),
        'Единица изменения площади':
            get_correct_data(land_plot_tab.get('areaUnit')),
        'Кадастровый № ЗУ': get_correct_data(land_plot_tab.get('cadastralNumber')),
        'Дата ГПЗУ': get_correct_data(land_plot_tab.get('gpzuDate')),
        'Номер ГПЗУ': get_correct_data(land_plot_tab.get('gpzuNumber')),
        'ВРИ': get_correct_data(land_plot_tab.get('vri')),

    }

    investment_site.photo_urls = response_json.get('photoUrls')
    investment_site.extra_data = extra_data
    investment_site.url = (
        'https://investmoscow.ru/business/'
        f'invest-catalog/{investment_site.external_id}'
    )
    investment_site.save(
        update_fields=['photo_urls', 'extra_data', 'url'],
    )


def parsing_industrial_site_4(
    investment_site: InvestmentObject,
):
    """Парсинг промплощадок."""
    # Формируем url и совершаем запрос к api.
    url_for_parsing = URL_MAPPING.get(
        investment_site.object_type,
    ).format(
        id=investment_site.external_id,
    )
    response_json = requests.get(
        url=url_for_parsing,
        headers={'Content-Type': 'application/json'},
        timeout=15,
    ).json()

    generic_info_tab = response_json.get('genericInfoTab')
    room_for_rent_tab = response_json.get(
        'roomForRentTab',
    )

    extra_data = {
        # Здание.
        'Наименование': get_correct_data(generic_info_tab.get('name')),
        'Вид объекта': get_correct_data(generic_info_tab.get('kind')),
        'Адрес': get_correct_data(generic_info_tab.get('address')),
        'Округ': get_correct_data(generic_info_tab.get('okrug')),
        'Основная информация': get_correct_data(generic_info_tab.get('desc')),
        'Площадь земельного участка':
        get_correct_data(generic_info_tab.get('groundArea')),
        # Помещения под аренду.
        'Парковка': get_correct_data(room_for_rent_tab.get('parking')),
        'Вода': get_correct_data(room_for_rent_tab.get('water')),
        'Отопление': get_correct_data(room_for_rent_tab.get('heating')),
        'Электроэнергия': get_correct_data(room_for_rent_tab.get('electricity')),
        'Площадь помещений под аренду':
        get_correct_data(room_for_rent_tab.get('area')),
        'Стоимость площадки': get_correct_data(room_for_rent_tab.get('price')),
        'Тип площадки': get_correct_data(room_for_rent_tab.get('type')),
    }

    investment_site.photo_urls = response_json.get('photoUrls')
    investment_site.extra_data = extra_data
    investment_site.url = (
        'https://investmoscow.ru/business/site-details/'
        f'room/{investment_site.external_id}'
    )
    investment_site.save(
        update_fields=['photo_urls', 'extra_data', 'url'],
    )


def parsing_industrial_land_5(
    investment_site: InvestmentObject,
):
    """Парсинг промплощадок (земельных участков)."""
    # Формируем url и совершаем запрос к api.
    url_for_parsing = URL_MAPPING.get(
        investment_site.object_type,
    ).format(
        id=investment_site.external_id,
    )
    response_json = requests.get(
        url=url_for_parsing,
        headers={'Content-Type': 'application/json'},
        timeout=15,
    ).json()

    generic_info_tab = response_json.get('genericInfoTab')
    technical_and_economic_indicators_tab = response_json.get(
        'technicalAndEconomicIndicatorsTab',
    )

    extra_data = {
        # Общая информация.
        'Наименование': get_correct_data(generic_info_tab.get('name')),
        'Вид объекта': get_correct_data(generic_info_tab.get('kind')),
        'Адрес': get_correct_data(generic_info_tab.get('address')),
        'Округ': get_correct_data(generic_info_tab.get('okrug')),
        'Кадастровый номер земельного участка':
            get_correct_data(generic_info_tab.get('cadastrNumber')),
        'Основная информация': get_correct_data(generic_info_tab.get('desc')),
        'Площадь земельного участка':
            get_correct_data(generic_info_tab.get('groundArea')),
        'Назначение земельного участка':
            get_correct_data(generic_info_tab.get('landPurpose')),
        'Требуется внести изменения ПЗЗ г. Москвы':
            clear_data(generic_info_tab.get('needToMakeChangesToPzzOfMoscow', False)),
        # Технико-экономические показатели.
        'Максимальный процент застройки':
            get_correct_data(
                technical_and_economic_indicators_tab.get('maxBuildingPercent'),
            ),
        'Плотность застройки': get_correct_data(
            technical_and_economic_indicators_tab.get('maxDensity'),
        ),
        'Высотность': get_correct_data(
            technical_and_economic_indicators_tab.get('maxHeight'),
        ),
    }

    investment_site.photo_urls = response_json.get('photoUrls')
    investment_site.extra_data = extra_data
    investment_site.url = (
        'https://investmoscow.ru/business/site-details/'
        f'room/{investment_site.external_id}'
    )
    investment_site.save(
        update_fields=['photo_urls', 'extra_data', 'url'],
    )


def parsing_krt_6(
    investment_site: InvestmentObject,
):
    """Парсинг КРТ."""
    # Формируем url и совершаем запрос к api.
    url_for_parsing = URL_MAPPING.get(
        investment_site.object_type,
    ).format(
        id=investment_site.external_id,
    )
    response_json = requests.get(
        url=url_for_parsing,
        headers={'Content-Type': 'application/json'},
        timeout=15,
    ).json()

    extra_data = {
        # Земельный участок.
        'Кадастровый номер':
            get_correct_data(response_json.get('cadastralNumber')),
        'Площадь': get_correct_data(response_json.get('area')),
        'Округ': get_correct_data(response_json.get('okrug')),
        'Статус проекта': get_correct_data(response_json.get('status')),
        'Адрес': get_correct_data(response_json.get('address')),
        # Технико-экономические показатели.
        'Площадь застройки производственного назначения':
            get_correct_data(response_json.get('areaProduction')),
        'Площадь застройки общественно-делового назначения':
            get_correct_data(response_json.get('areaPublicAndBusiness')),
        'Суммарная поэтажная площадь застройки в ГНС':
            get_correct_data(response_json.get('areaSumGNS')),
        'Площадь существующей застройки':
            get_correct_data(response_json.get('areaExistingConstruction')),
        'Количество правообладателей':
            get_correct_data(response_json.get('numberOwners')),
        'Количество рабочих мест':
            get_correct_data(response_json.get('numberWorkplaces')),
        'Выкуп ЗИК': get_correct_data(response_json.get('buybackZIK')),
        'Виды разрешенного использования':
            get_correct_data_from_dict(
                key_name='name',
                all_data_json=response_json.get('vriZu', []),
            ),
    }

    investment_site.photo_urls = response_json.get('photoUrls')
    investment_site.extra_data = extra_data
    investment_site.url = (
        'https://investmoscow.ru/business/'
        f'krt/{investment_site.external_id}'
    )
    investment_site.save(
        update_fields=['photo_urls', 'extra_data', 'url'],
    )


def get_correct_data_from_dict(
    key_name: str,
    all_data_json: List[Dict[str, Any]],
) -> str:
    """Формирование корректной строки из словаря."""
    str_data = ''
    for data_json in all_data_json:
        str_data += data_json.get(key_name, '') + '; '

    return str_data[:-1]
