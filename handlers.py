from telegram import ForceReply, Update
from telegram.ext import ContextTypes

from gcal import GCal

gcal = GCal()


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
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
