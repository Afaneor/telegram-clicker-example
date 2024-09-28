from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, \
    WebAppInfo
from telegram.ext import Application, CommandHandler
import logging
from django.conf import settings

logger = logging.getLogger('django')


async def start(update: Update, context):
    """Обрабатывает команду /start."""
    keyboard = [
        [
            InlineKeyboardButton(
                'Launch App',
                web_app=WebAppInfo(settings.FRONTEND_URL),
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        '<b>Hey!</b>\nGo to the app!',
        reply_markup=reply_markup,
        parse_mode='HTML',
    )


def run_telegram_bot():
    """Основная функция для запуска бота через long polling."""
    logger.info('starting management command')
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

    # Регистрируем обработчики команд и сообщений
    application.add_handler(CommandHandler('start', start))

    # Запускаем бота с использованием long polling
    logger.info('running tg bot')
    application.run_polling()
