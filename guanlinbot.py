import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def filter_intro_message(message):
    """Filter function to check if the message starts with "i'm", "I'm", "im", or "Im" followed by any text."""
    message_text = message.text.lower()
    if message_text.startswith("i'm ") or message_text.startswith("im "):
        return True, message_text.split(" ", 1)[1]
    return False, None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for the /start command."""
    await update.message.reply_text(
        'Hi! I am Guan Lin. I will respond to messages starting with "i\'m" or "im" followed by any text.'
    )


async def respond_to_intro(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for messages starting with "i'm", "I'm", "im", or "Im" followed by any text."""
    is_intro, text = filter_intro_message(update.message)
    if is_intro:
        response = f"hi {text}, i'm guan lin"
        await update.message.reply_text(response)


def main() -> None:
    """Start the bot."""
    # check if GUANLIN_BOT_TOKEN defined in environment variables, if not, exit
    if "GUANLIN_BOT_TOKEN" not in os.environ:
        logger.error(
            "GUANLIN_BOT_TOKEN is not defined in environment variables")
        return

    application = Application.builder().token(
        os.environ["GUANLIN_BOT_TOKEN"]).build()

    # Register the command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, respond_to_intro))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
