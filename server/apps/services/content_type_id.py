from django.contrib.contenttypes.models import ContentType


def get_content_type_id(cicada_object) -> int:
    """Получение content_type_id по объекту."""
    obj_ct = ContentType.objects.get_for_model(  # type: ignore
        cicada_object.__class__,
    )

    return obj_ct.id
