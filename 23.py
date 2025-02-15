import json
import logging
import secrets
import string

from telegram.ext import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, WebAppInfo


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Dictionary to store referral links
referral_links = {}

# Define a `/start` command handler.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with a button that opens a the web app."""
    await update.message.reply_text(
        "Ты перешел по реферальной ссылке пользователя @catfrik",
        reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(
                text="Открыть через сократитель",
                web_app=WebAppInfo(url="https://as-opal.vercel.app/"),
            )
        ),
    )

# Define a `/ref` command handler.
async def generate_ref_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate a referral link and store it in the dictionary."""
    user_id = update.effective_user.id
    if user_id in referral_links:
        ref_link = referral_links[user_id]
    else:
        ref_code = str(user_id)
        ref_link = f"https://t.me/as_opalbot?start={ref_code}"
        referral_links[user_id] = ref_link
    await update.message.reply_text(f"Your referral link is: {ref_link}")

# Handle incoming WebAppData
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Print the received data and remove the button."""
    # Here we use `json.loads`, since the WebApp sends the data JSON serialized string
    # (see webappbot.html)
    data = json.loads(update.effective_message.web_app_data.data)
    await update.message.reply_html(
        text=(
            f"You selected the color with the HEX value <code>{data['hex']}</code>. The "
            f"corresponding RGB value is <code>{tuple(data['rgb'].values())}</code>."
        ),
        reply_markup=ReplyKeyboardRemove(),
    )

    # Check if the user came through a referral link
    ref_code = context.args[0] if context.args else None
    if ref_code:
        for user_id, link in referral_links.items():
            if link.endswith(ref_code):
                try:
                    await context.bot.send_message(user_id, f"User {update.effective_user.mention_html()} has used your referral link!", parse_mode="HTML")
                except Exception as e:
                    logger.error(f"Error sending referral notification: {e}")
                break

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("7521199935:AAE6-z9bgumTHd6CTcgQNHqU5jiNrl8foOU").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ref", generate_ref_link))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
