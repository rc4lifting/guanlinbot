import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import random
from asyncio import sleep

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def is_special_message(message_text):
    # pattern to match the message starting with various forms of "i'm " including different apostrophes
    pattern = re.compile(r"^(i['`’\"]m )(.+)", re.IGNORECASE)

    match = pattern.match(message_text)
    if match:
        # return True and the message without the "i'm" part
        return True, match.group(2)
    return False, None


def filter_intro_message(message):
    """Filter function to check if the message starts with "i'm", "I'm", "im", or "Im" followed by any text."""
    message_text = message.text.lower()
    if message_text.startswith("i'm ") or message_text.startswith("im ") or message_text.startswith("i’m ") or message_text.startswith("i`m ") or message_text.startswith("i\"m ") or message_text.startswith("i‘m "):
        return True, message_text.split(" ", 1)[1]
    return False, None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for the /start command."""
    await update.message.reply_text(
        'Hi! I am Guan Lin. I will respond to messages starting with "i\'m" or "im" followed by any text.'
    )


async def respond_to_intro(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for messages starting with "i'm", "I'm", "im", or "Im" followed by any text."""
    print("test")
    is_intro, text = filter_intro_message(update.message)
    if is_intro:
        response = f"hi {text}, i'm guan lin"
        await update.message.reply_text(response)


async def respond_to_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text.lower()
    # if message from lynn
    # print userid and msg
    print(update.message.from_user.id, message_text)
    if update.message.from_user.id == 371742259:
        # every 20 messages, bully lynn
        print("lynn msg")
        if "fast" in message_text:
            await update.message.reply_text("speaking of fast, what about your backpedalling speed (submission by carol)")
        elif random.randint(1, 20) == 1:
            messages = ["hahahahah good bants lynn, watch out for your ankles",
                        "good point lynn what about your valorant kda"]
            # pick one and reply to her
            response = random.choice(messages)
            await update.message.reply_text(response, reply_to_message_id=update.message.message_id)
        # return
    if update.message.from_user.id == 547045575 and random.randint(1, 20) == 1:
        print("carol msg")
        messages = ["stfu u gremlin"]
        response = random.choice(messages)
        await update.message.reply_text(response, reply_to_message_id=update.message.message_id)

    if "tank" in message_text:
        await update.message.reply_text("speaking of tanks, lynn have you considered going down to tank? (submission by carol)")
        return
    # Check if message is an introduction
    is_intro, intro_text = filter_intro_message(update.message)
    if is_intro:
        # chekc if intro_text >50 letters, if so, ignore
        if len(intro_text) > 250:
            await update.message.reply_text("i aint reading all that bruh")
            return
        response = f"hi {intro_text}, i'm guan lin"
        await update.message.reply_text(response, reply_to_message_id=update.message.message_id)
        return  # Stop further processing

    # Check if message should trigger a wtf response
    is_wtf = filter_wtf_message(update.message)
    if is_wtf:
        await update.message.reply_text("lmao call police ah", reply_to_message_id=update.message.message_id)

    # every 100 messages, send nananananananana
    if random.randint(1, 500) == 1:
        await update.message.reply_text("nananananananana")


async def madness(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Determine if the /madness command is a reply to another message
    reply_to_message_id = None
    if update.message.reply_to_message:
        reply_to_message_id = update.message.reply_to_message.message_id

    # Start message
    # Ensure the message is replying to the original message that /madness was a reply to
    message = await update.message.reply_text(
        "Consulting madness charts... 🧐",
        reply_to_message_id=reply_to_message_id
    )

    # Simulate some processing time and update the message to show a loading animation
    for i in range(3):
        await sleep(0.5)
        animation_frames = ["🌑🌒🌓🌔🌕", "🌕🌖🌗🌘🌑", "🌑🌒🌓🌔🌕"]
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=message.message_id,
            text=f"Consulting madness charts... 🧐 {animation_frames[i]}"
        )

    # Midpoint update
    await sleep(0.5)  # Ensuring the sleep to simulate more processing time
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=message.message_id,
        text="[=====>.......] Double-checking the madness... 🕵️"
    )

    # Simulate more processing time
    await sleep(0.5)

    final_messages = [
        "VERIFIED: 🚨 Bro did a madness! 🚨",
        "VERIFIED: 😔 Bro did not do a madness..."
    ]
    # Randomly choose one of the final messages
    final_text = random.choice(final_messages)
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=message.message_id,
        text=final_text
    )


async def bully_lynn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # lynns id is 371742259
    lynn_id = 371742259


def filter_wtf_message(message):
    """Filter function to check if the message contains 'wtf' and is longer than 5 words."""
    message_text = message.text.lower()
    if ("wtf" in message_text or "fuck" in message_text or "fk" in message_text) and len(message_text.split()) >= 5:
        return True
    return False


async def respond_to_wtf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for messages containing 'wtf' and longer than 5 words."""
    is_wtf = filter_wtf_message(update.message)
    if is_wtf:
        await update.message.reply_text("lmao call police ah")


def main() -> None:
    """Start the bot."""
    # check if GUANLIN_BOT_TOKEN defined in environment variables, if not, exit
    if "GUANLIN_BOT_TOKEN" not in os.environ:
        logger.error(
            "GUANLIN_BOT_TOKEN is not defined in environment variables")
        return

    application = Application.builder().token(
        os.environ["GUANLIN_BOT_TOKEN"]).build()

    # application.add_handler(MessageHandler(
    #     filters.TEXT & ~filters.COMMAND, respond_to_wtf))
    # Register the command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, respond_to_message))
    # application.add_handler(MessageHandler(
    #     filters.TEXT & ~filters.COMMAND, respond_to_intro))

    application.add_handler(CommandHandler("madness", madness))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
