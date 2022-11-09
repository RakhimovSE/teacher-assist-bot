import asyncio
from typing import Union

import telegram.error
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatAction
from ptbcontrib.roles import BOT_DATA_KEY
from datetime import datetime, timezone, timedelta
from dateutil import parser

from src.google_calendar.gcal import GCal

gcal = GCal()


def get_admin_ids(context: ContextTypes.DEFAULT_TYPE) -> list[int]:
    return context.bot_data[BOT_DATA_KEY].admins.chat_ids


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(f'Hi {user.mention_html()}!')

    admin_ids = get_admin_ids(context)
    if user.id in admin_ids:
        return

    new_user_text = f'{user.mention_html()} (id={user.id}) joined bot'
    context.application.create_task(
        asyncio.gather(
            *(
                context.bot.send_message(admin_id, new_user_text, parse_mode=ParseMode.HTML)
                for admin_id in admin_ids
            )
        )
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def send_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    async def send_reminder(_class: dict) -> Union[str, None]:
        if 'telegram_id' not in _class['args']:
            return None

        now = datetime.now(timezone.utc)
        class_start = parser.parse(_class['start'].get('dateTime', _class['start'].get('date')))
        if class_start - now > timedelta(days=1):
            return None

        class_end = parser.parse(_class['end'].get('dateTime', _class['end'].get('date')))

        text = f'Привет!\nНапоминаю о занятии {class_start.strftime("%d.%m")} с ' \
               f'{class_start.strftime("%H:%M")} до {class_end.strftime("%H:%M")}. Всё в силе?'
        try:
            await context.bot.send_message(_class['args']['telegram_id'], text)
            return f'"{_class["summary"]}": успешно'
        except telegram.error.BadRequest as ex:
            return f'"{_class["summary"]}": ошибка ({ex.message})'

    await update.message.reply_chat_action(ChatAction.TYPING)
    NO_NEW_CLASSES = 'В ближайшее время занятий нет'

    classes = gcal.get_next_events()

    if not classes:
        await update.message.reply_text(NO_NEW_CLASSES)
        return

    reminder_jobs = (send_reminder(_class) for _class in classes)
    notify_responses = [res for res in await asyncio.gather(*reminder_jobs) if res]
    await update.message.reply_text(
        '\n'.join(notify_responses) if len(notify_responses) else NO_NEW_CLASSES)


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Ты админ')
