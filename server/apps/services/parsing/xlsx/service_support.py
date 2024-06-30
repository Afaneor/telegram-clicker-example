import logging
import re

import pylightxl as xl

from server.apps.investment_object.models.economic_activity import (
    EconomicActivity,
)
from server.apps.investment_object.models.restriction import Restriction
from server.apps.services.enums import ServiceSupportType
from server.apps.services.parsing.xlsx.base import get_correct_data
from server.apps.support.models import ServiceSupport
from server.settings.components import BASE_DIR

logger = logging.getLogger('django')


def parsing_xlsx_service_support():
    """
    Парсинг мер поддержки.
    """
    db = xl.readxl(
        f'{BASE_DIR}'
        '/server/apps/initial_data/support.xlsx'
    )
    for list_name in db.ws_names:
        for index, row in enumerate(db.ws(ws=list_name).rows):
            if index != 0:
                support_service, s_created = ServiceSupport.objects.update_or_create(
                    name=row[1],
                    defaults={
                        'region': get_correct_data(row[0]).strip().capitalize(),
                        'service_support_type':
                            ServiceSupportType.SUPPORT_MEASURE,
                        'support_type': get_correct_data(row[2]).capitalize(),
                        'support_level': get_correct_data(row[3]).capitalize(),
                        'description': (
                            get_correct_data(row[4])
                            if row[4]
                            else 'Подробнее на сайте https://investmoscow.ru/catalog/search'
                        ),
                        'legal_act': get_correct_data(row[5]).capitalize(),
                        'url_legal_act': get_correct_data(row[6]),
                        'url_application_form': get_correct_data(row[8]),
                        'name_responsible_body': get_correct_data(row[9]),
                        'msp_roster': row[13].capitalize(),
                        'applicant_requirement': get_correct_data(row[14]),
                        'applicant_procedure': get_correct_data(row[15]),
                        'required_document': get_correct_data(row[16]),
                    },
                )
                if row[11]:
                    objects_for_add = []
                    for economic_activity_row_data in re.split(';', row[11]):
                        economic_activity_data = economic_activity_row_data.split('-')
                        try:
                            economic_activity = EconomicActivity.objects.get(
                                code=get_correct_data(
                                    economic_activity_data[0],
                                ),
                            )
                        except EconomicActivity.DoesNotExist:
                            continue

                        objects_for_add.append(economic_activity)
                    support_service.economic_activities.set(objects_for_add)

                if row[12]:
                    objects_for_add = []
                    for restriction_row_data in row[12].split(';'):
                        restriction, created = (
                            Restriction.objects.get_or_create(
                                name=get_correct_data(
                                    restriction_row_data,
                                ).capitalize(),
                            )
                        )

                        objects_for_add.append(restriction)
                    support_service.restrictions.set(objects_for_add)

            logger.info(f'Завершена обработка {row[1]}')
