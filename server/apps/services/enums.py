from django.db import models
from django.utils.translation import gettext_lazy as _


class InfrastructureAvailability(models.TextChoices):
    """Наличие инфраструктуры"""

    POSSIBLE_CREATION = 'possible_creation', _('Возможно создание')
    YES = 'yes', _('Да')
    NOT_DATA = 'not_data', _('Нет данных')


class ObjectType(models.TextChoices):
    """Наличие инфраструктуры"""

    TECHNOPARK = 'technopark', _('Технопарк')
    TECHNOPOLIS = 'technopolis', _('Технополис')
    LAND_PLOT = 'land_plot', _('Земельный участок')
    BUILDING = 'building', _('Помещение')
    CDT = 'cdt', _('КРТ')
    TENDER_LOT = 'tender_lot', _('Лот тендера')
    READY_BUSINESS = 'ready_business', _('Реальный бизнес')
    OTHER = 'other', _('Другое')
    NOT_DATA = 'not_data', _('Нет данных')


class TransactionFormType(models.TextChoices):
    """Тип сделки."""

    RENT = 'rent', _('Аренда')
    SALE = 'sale', _('Продажа')
    RENT_OR_SALE = 'rent_or_sale', _('Аренда или продажа')
    NOT_DATA = 'not_data', _('Нет данных')


class BusinessType(models.TextChoices):
    """Тип бизнеса: ИП, физическое лицо или компания."""

    LEGAL = 'legal', _('Юридическое лицо')
    INDIVIDUAL = 'individual', _('Индивидуальный предприниматель')
    PHYSICAL = 'physical', _('Физическое лицо')


class TaxSystemType(models.TextChoices):
    """Тип системы налогооблажения."""

    OSN = 'osn', _('Общая')
    YSN = 'ysn', _('Упрощенная')
    PATENT = 'patent', _('Патентная')


class PropertyType(models.TextChoices):
    """Типы зданий."""

    WORKSHOP_BUILDING = 'workshop_building', _('Здание цеха')
    WAREHOUSE_SPACE = 'warehouse_space', _('Складское помещение')
    ADMINISTRATIVE_BUILDING = 'administrative_building', _('Административное здание')  # noqa: E501
    OTHER = 'other', _('Другие типы')


class MessageOwnerType(models.TextChoices):
    """Владелец сообщения"""

    USER = 'user', _('Пользователь')
    ASSISTANT = 'assistant', _('assistant')
    SYSTEM = 'system', _('Система')


class ServiceSupportType(models.TextChoices):
    """Тип сервиса."""

    SERVICE = 'service', _('Услуга')
    SUPPORT_MEASURE = 'support_measure', _('Мера поддержки')


class EventType(models.TextChoices):
    """Тип события."""

    WEBINAR = 'webinar', _('Вебинар')
    MEETING = 'meeting', _('Встреча')


class SubscriptionType(models.TextChoices):
    """Тип подписки."""

    INVESTMENT_OBJECT = 'investment_object', _('Инвестиционный объект')
    SERVICE_SUPPORT = 'service_support', _('Сервис поддержки')
    TOPIC = 'topic', _('Тема')
    EVENT = 'event', _('События')


class UploadDataFromFileType(models.TextChoices):
    """Типы объектов для прогрузки через xlsx файл."""

    SPECIALIZED_SITE = 'specialized_site', _('Специализированная площадка')
    REAL_ESTATE = 'real_estate', _('Недвижимость')
