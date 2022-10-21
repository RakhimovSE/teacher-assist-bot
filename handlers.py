import asyncio

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from ptbcontrib.roles import BOT_DATA_KEY

from gcal import GCal

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


async def events(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    events = gcal.get_next_events()

    if not events:
        await update.message.reply_text('No upcoming events found.')
        return

    events_formatted = []
    # Prints the start and name of the next 10 events
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        events_formatted.append(f'{start} {event["summary"]}')
    await update.message.reply_text('\n'.join(events_formatted))


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Ты админ')
