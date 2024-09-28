from django.core.management.base import BaseCommand, CommandError

from server.apps.bot.services.bot import run_telegram_bot


class Command(BaseCommand):
    help = "Run telegram bot for miniapp"

    def handle(self, *args, **options):
        run_telegram_bot()
