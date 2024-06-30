import logging
from typing import Any, Dict

import requests

from server.apps.investment_object.models.investment_object import (
    InvestmentObject,
)
from server.apps.services.enums import ObjectType
from server.apps.services.parsing.investmoscow.investment_object import (
    parsing_industrial_land_5,
    parsing_industrial_site_4,
    parsing_investment_catalog_3,
    parsing_krt_6,
    parsing_technopark_1,
    parsing_technopolis_2,
)

logger = logging.getLogger('django')


FUNCTION_MAP: Dict[int, Any] = {
    1: parsing_technopark_1,
    2: parsing_technopolis_2,
    3: parsing_investment_catalog_3,
    4: parsing_industrial_site_4,
    5: parsing_industrial_land_5,
    6: parsing_krt_6,
}

object_type = {
    1: ObjectType.TECHNOPARK,
    2: ObjectType.TECHNOPOLIS,
    3: ObjectType.LAND_PLOT,
    4: ObjectType.BUILDING,
    5: ObjectType.LAND_PLOT,
    6: ObjectType.CDT,
}


def parsing_investmoscow():
    """Парсинг данных с сайта investmoscow.ru"""
    # Получаем https://investmoscow.ru/about-moscow/investment-map-v2
    response = requests.post(
        url=(
            'https://api.investmoscow.ru/investmoscow/investment-map/'
            'v1/investmentPlatform/searchInvestmentObjects'
        ),
        headers={
            'Content-Type': 'application/json'
        },
        json={
            'PageNumber': 1,
            'PageSize': 500,
            'districts': [],
            'metros': [],
        },
        timeout=15,
    )
    for entity in response.json()['entities']:
        if entity.get('coords'):
            if entity.get('coords').get('type') == 'Point':
                longitude = entity.get('coords').get('coordinates')[0]
                latitude = entity.get('coords').get('coordinates')[1]
            elif entity.get('coords').get('type') == 'Polygon':
                longitude = entity.get('coords').get('coordinates')[0][0][0]
                latitude = entity.get('coords').get('coordinates')[0][0][1]
            elif entity.get('coords').get('type') == 'MultiPolygon':
                longitude = entity.get('coords').get('coordinates')[0][0][0][0]
                latitude = entity.get('coords').get('coordinates')[0][0][0][1]
            else:
                longitude = None
                latitude = None
        else:
            longitude = None
            latitude = None

        investment_site, created = InvestmentObject.objects.get_or_create(
            external_id=entity.get('investmentPlatformId'),
            name=entity.get('name'),
            defaults={
                'main_photo_url': entity.get('previewImgUrl'),
                'longitude': longitude,
                'latitude': latitude,
                'object_type': object_type.get(entity.get('type')),
            },
        )
        FUNCTION_MAP.get(entity.get('type'))(
            investment_site=investment_site,
        )
        logger.info(f"Обработано {entity.get('name')}")
