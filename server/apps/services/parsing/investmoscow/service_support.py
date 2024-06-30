import logging

import requests

from server.apps.services.enums import ServiceSupportType
from server.apps.services.parsing.xlsx.base import clear_data
from server.apps.support.models import ServiceSupport

logger = logging.getLogger('django')


def parsing_investmoscow_service_support():
    """Парсинг сервисов investmoscow.ru"""
    # Получаем https://investmoscow.ru/catalog/search
    response = requests.post(
        url=(
            'https://api.investmoscow.ru/common/usoz-services/v1/'
            'services/searchPublished'
        ),
        headers={
            "accept": "application/json",
            "accept-language": "ru-RU",
            "content-type": "application/json",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "x-requested-with": "XMLHttpRequest"
        },
        json={
            'PageNumber': 1,
            'PageSize': 500,
        },
        timeout=15,
    )
    for entity in response.json().get('entities'):
        entity_url = (
            'https://api.investmoscow.ru/common/usoz-services/v1/services/'
            f"getPublishedService/{entity.get('id')}"
        )
        entity_response = requests.get(url=entity_url).json()['information']
        type_services = {
            'меры поддержки': ServiceSupportType.SUPPORT_MEASURE,
            'услуги': ServiceSupportType.SERVICE,
        }
        services = ServiceSupport.objects.filter(
            name=entity.get('name'),
        )
        if services.exists():
            service = services.first()
            service.type_service = entity.get('categoryName', '').lower()
            service.external_id = entity.get('id')
            service.url = entity_url
        else:
            applicant_requirement = ''
            for item in entity_response.get('applicantRequirements').get('items'):
                item = clear_data(row_data=item.get('description'))
                applicant_requirement += f'- {item}\n'

            applicant_procedure = ''
            for index, item in enumerate(entity_response.get('considerationProcedure').get('procedures')):
                item = clear_data(row_data=item)
                applicant_requirement += f'- {item}\n'

            service, created = ServiceSupport.objects.get_or_create(
                external_id=entity.get('id'),
                defaults={
                    'region': 'Москва',
                    'type_service':
                        clear_data(
                            row_data=type_services.get(
                                entity.get('serviceTypeName', ''),
                            ),
                        ),
                    'name':
                        clear_data(row_data=entity.get('name', '')),
                    'support_type':
                        clear_data(
                            row_data=entity.get('categoryName', '').lower(),
                        ),
                    'support_level': 'региональные меры',
                    'description':
                        clear_data(
                            row_data=entity_response.get(
                                'common', {},
                            ).get(
                                'fullDescription', '',
                            )
                        ),
                    'legal_act':
                        clear_data(
                            row_data=entity_response.get(
                                'reasons', {},
                            ).get(
                                'regulatoryLegalActs', [{}],
                            )[0].get(
                                'name', '',
                            )
                        ),
                    'url_legal_act':
                        clear_data(
                            row_data=entity_response.get(
                                'reasons',
                            ).get(
                                'regulatoryLegalActs', [{}],
                            )[0].get(
                                'link',  '',
                            )
                        ),
                    'url_application_form':
                        clear_data(
                            row_data=entity_response.get(
                                'other', {},
                            ).get(
                                'descriptionLink', '',
                            ),
                        ),
                    'name_responsible_body':
                        clear_data(
                            row_data=entity_response.get(
                                'contacts', {},
                            ).get(
                                'responsibleAuthorityTitle', '',
                            ),
                        ),
                    'applicant_requirement': applicant_requirement,
                    'applicant_procedure': applicant_procedure,
                    'url': entity_url,
                }
            )

        logger.info(f'Обработана запись: {service.name}')
