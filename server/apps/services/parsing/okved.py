import json

from django.conf import settings

from server.apps.investment_object.models import EconomicActivity


def parsing_okved():
    """Парсинг ОКВЭД."""
    with open(
        f'{settings.BASE_DIR}'
        f'/server/apps/initial_data/okved_for_db.json'
    ) as all_okved:
        for okved in json.load(all_okved):
            EconomicActivity.objects.get_or_create(
                code=okved['code'],
                parent_code=okved['parent_code'],
                section=okved['section'],
                name=okved['name'],
                comment=okved['comment'],
            )

