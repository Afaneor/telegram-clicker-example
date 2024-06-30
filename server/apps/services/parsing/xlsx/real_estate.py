import logging
import re

import pylightxl as xl

from server.apps.investment_object.models import (
    Infrastructure,
    InvestmentObject,
    RealEstate,
    TransactionForm,
)
from server.apps.investment_object.models.economic_activity import (
    EconomicActivity,
)
from server.apps.services.enums import (
    InfrastructureAvailability,
    ObjectType,
    TransactionFormType,
)
from server.apps.services.parsing.xlsx.base import clear_data, get_correct_data
from server.settings.components import BASE_DIR

logger = logging.getLogger('django')


def parsing_real_estate(file=None):
    """
    Парсинг зданий и сооружений.
    """
    if file:
        db = xl.readxl(file)
    else:
        db = xl.readxl(
            f'{BASE_DIR}'
            '/server/apps/initial_data/real_estate.xlsx'
        )
    for list_name in db.ws_names:
        for index, row in enumerate(db.ws(ws=list_name).rows):
            if index != 0:
                row = list(map(clear_data, row))
                object_type = (
                    ObjectType.BUILDING.value
                    if row[11] and row[11] == 'Помещение'
                    else ObjectType.LAND_PLOT.value
                )

                if row[83]:
                    photo_urls = row[83].split('\n')
                    main_photo_url = photo_urls[0]
                else:
                    photo_urls = []
                    main_photo_url = ''

                # Форма сделки.
                if row[14] and row[14].lower().find('аренда') >= 0:
                    transaction_form, tf_created = (
                        TransactionForm.objects.get_or_create(
                            name=get_correct_data(row[14]),
                            transaction_form_type=TransactionFormType.RENT,
                        )
                    )
                elif row[14] and row[14].lower().find('продажа') >= 0:
                    transaction_form, tf_created = (
                        TransactionForm.objects.get_or_create(
                            name=get_correct_data(row[14]),
                            transaction_form_type=TransactionFormType.SALE,
                        )
                    )
                elif row[14]:
                    transaction_form, tf_created = (
                        TransactionForm.objects.get_or_create(
                            name=get_correct_data(row[14]),
                            transaction_form_type=TransactionFormType.NOT_DATA,
                        )
                    )
                else:
                    transaction_form, tf_created = (
                        TransactionForm.objects.get_or_create(
                            name='Нет данных',
                            transaction_form_type=TransactionFormType.NOT_DATA,
                        )
                    )

                # Стоимость.
                if row[15]:
                    cost = row[15].replace(',', '.')
                else:
                    cost = None

                # Площадь земли.
                if row[22]:
                    land_area = row[22].replace(',', '.')
                else:
                    land_area = None

                # Площадь земли.
                if row[27]:
                    building_area = row[27].replace(',', '.')
                else:
                    building_area = None

                investment_object, io_created = (
                    InvestmentObject.objects.update_or_create(
                        name=row[0],
                        defaults={
                            'main_photo_url': main_photo_url,
                            'photo_urls': photo_urls,
                            'object_type': object_type,
                            'transaction_form': transaction_form,
                            'cost': cost,
                            'land_area': land_area,
                            'building_area': building_area,
                            'location': get_correct_data(row[8]),
                            'data_source': 'investmoscow.ru',
                            'url': get_correct_data(row[32]),
                            'longitude':
                                row[86].split(',')[0] if row[86] else None,
                            'latitude':
                                row[86].split(',')[1] if row[86] else None,
                        },
                    )
                )

                if row[79]:
                    objects_for_add = []
                    for economic_activity_row_data in re.split(r';', row[11]):
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
                    investment_object.economic_activities.set(objects_for_add)

                real_estate, re_created = RealEstate.objects.update_or_create(
                    investment_object=investment_object,
                    defaults={
                        'preferential_treatment': get_correct_data(row[1]),
                        'preferential_treatment_object_code':
                            get_correct_data(row[2]),
                        'preferential_treatment_object_name':
                            get_correct_data(row[3]),
                        'support_infrastructure_object':
                            get_correct_data(row[4]),
                        'support_infrastructure_object_code':
                            get_correct_data(row[5]),
                        'support_infrastructure_object_name':
                            get_correct_data(row[6]),
                        'region': get_correct_data(row[7]),
                        'address': get_correct_data(row[9]),
                        'nearest_cities': get_correct_data(row[10]),
                        'site_format': get_correct_data(row[11]),
                        'site_type': get_correct_data(row[12]),
                        'ownership_type': get_correct_data(row[13]),
                        'rental_period': get_correct_data(row[18]),
                        'procedure_determining_cost': get_correct_data(row[19]),
                        'hazard_class_object': get_correct_data(row[20]),
                        'characteristic_object': get_correct_data(row[21]),
                        'land_cadastral_number': get_correct_data(row[23]),
                        'permitted_use_options': get_correct_data(row[24]),
                        'cupping': (
                            get_correct_data(row[25]).capitalize()
                            if row[25]
                            else ''
                        ),
                        'land_category': get_correct_data(row[26]),
                        'building_cadastral_number': get_correct_data(row[28]),
                        'building_technical_specifications': get_correct_data(row[29]),
                        'owner_name': get_correct_data(row[30]),
                        'owner_inn': get_correct_data(row[31]),
                        'other_characteristics': get_correct_data(row[75]),
                        'application_procedure': get_correct_data(row[76]),
                        'documents_for_application': get_correct_data(row[77]),
                        'application_form_url': get_correct_data(row[78]),
                        'urban_planning': get_correct_data(row[80]),
                        'other_information': get_correct_data(row[82]),
                        'maip': (
                            get_correct_data(row[84]).capitalize()
                            if row[84]
                            else ''
                        ),
                        'benefit_description': get_correct_data(row[85]),
                    }
                )

                if row[34] and row[34].lower() != 'нет':
                    availability = (
                        InfrastructureAvailability.YES
                        if row[34].lower() == 'да'
                        else InfrastructureAvailability.POSSIBLE_CREATION
                    )
                    infrastructure_water_supply = create_infrastructure(
                        row=row,
                        start_number_row=35,
                        name='Водоснабжение',
                        unit_measure='руб./куб. м',
                        availability=availability,
                    )

                    real_estate.infrastructures.add(infrastructure_water_supply)

                if row[41] and row[41].lower() != 'нет':
                    availability = (
                        InfrastructureAvailability.YES
                        if row[41].lower() == 'да'
                        else InfrastructureAvailability.POSSIBLE_CREATION
                    )
                    infrastructure_sewage = create_infrastructure(
                        row=row,
                        start_number_row=42,
                        name='Водоотведение',
                        unit_measure='руб./куб. м',
                        availability=availability,
                    )

                    real_estate.infrastructures.add(infrastructure_sewage)

                if row[48] and row[48].lower() != 'нет':
                    availability = (
                        InfrastructureAvailability.YES
                        if row[48].lower() == 'да'
                        else InfrastructureAvailability.POSSIBLE_CREATION
                    )
                    infrastructure_gas = create_infrastructure(
                        row=row,
                        start_number_row=49,
                        name='Газоснабжение',
                        unit_measure='руб./куб. м',
                        availability=availability,
                    )

                    real_estate.infrastructures.add(infrastructure_gas)

                if row[55] and row[55].lower() != 'нет':
                    availability = (
                        InfrastructureAvailability.YES
                        if row[55].lower() == 'да'
                        else InfrastructureAvailability.POSSIBLE_CREATION
                    )
                    infrastructure_electricity = create_infrastructure(
                        row=row,
                        start_number_row=56,
                        name='Электроснабжение',
                        unit_measure='руб./МВт*ч',
                        availability=availability,
                    )

                    real_estate.infrastructures.add(infrastructure_electricity)

                if row[62] and row[62].lower() != 'нет':
                    availability = (
                        InfrastructureAvailability.YES
                        if row[62].lower() == 'да'
                        else InfrastructureAvailability.POSSIBLE_CREATION
                    )
                    infrastructure_heat = create_infrastructure(
                        row=row,
                        start_number_row=63,
                        name='Теплоснабжение',
                        unit_measure='руб./Гкал*ч',
                        availability=availability,
                    )

                    real_estate.infrastructures.add(infrastructure_heat)

                if row[69] and row[69].lower() != 'нет':
                    availability = (
                        InfrastructureAvailability.YES
                        if row[69].lower() == 'да'
                        else InfrastructureAvailability.POSSIBLE_CREATION
                    )
                    infrastructure_tko = Infrastructure.objects.create(
                        name='Вывоз ТКО',
                        consumption_tariff=(
                            f'{row[71]}  руб./куб. м'
                            if row[71]
                            else None
                        ),
                        availability=availability
                    )

                    real_estate.infrastructures.add(infrastructure_tko)

                if row[72] and row[72].lower() != 'нет':
                    availability = (
                        InfrastructureAvailability.YES
                        if row[72].lower() == 'да'
                        else InfrastructureAvailability.POSSIBLE_CREATION
                    )
                    infrastructure_access_roads = Infrastructure.objects.create(
                        name='Подъездные пути',
                        availability=availability
                    )

                    real_estate.infrastructures.add(infrastructure_access_roads)

                if row[73] and row[73].lower() != 'нет':
                    availability = (
                        InfrastructureAvailability.YES
                        if row[73].lower() == 'да'
                        else InfrastructureAvailability.POSSIBLE_CREATION
                    )
                    infrastructure_railroad_tracks = Infrastructure.objects.create(
                        name='Ж/д пути',
                        availability=availability
                    )

                    real_estate.infrastructures.add(
                        infrastructure_railroad_tracks,
                    )

                if row[74] and row[74].lower() != 'нет':
                    availability = (
                        InfrastructureAvailability.YES
                        if row[74].lower() == 'да'
                        else InfrastructureAvailability.POSSIBLE_CREATION
                    )
                    infrastructure_availability_truck_parking = Infrastructure.objects.create(
                        name='Наличие парковки грузового транспорт',
                        availability=availability
                    )

                    real_estate.infrastructures.add(
                        infrastructure_availability_truck_parking,
                    )

                logger.info(f'Завершена обработка {row[0]}')


def create_infrastructure(
    row,
    start_number_row: int,
    name: str,
    unit_measure: str,
    availability: str,
):
    return Infrastructure.objects.create(
        name=name.replace('• ', ''),
        consumption_tariff=(
            f'{row[start_number_row]} {unit_measure}'
            if row[start_number_row]
            else ''
        ),
        transportation_tariff=(
            f'{row[start_number_row+1]} {unit_measure}'
            if row[start_number_row+1]
            else ''
        ),
        max_allowable_power=(
            f'{row[start_number_row+2]} {unit_measure}'
            if row[start_number_row+2]
            else ''
        ),
        free_power=(
            f'{row[start_number_row+3]} {unit_measure}'
            if row[start_number_row+3]
            else ''
        ),
        throughput=(
            f'{row[start_number_row+5]} {unit_measure}'
            if row[start_number_row+5]
            else ''
        ),
        other_characteristics=(
            row[start_number_row+4]
            if row[start_number_row+4]
            else ''
        ),
        availability=availability
    )
