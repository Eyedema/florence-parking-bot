import logging
from bot_utils import Bot_utils
from bot_api_token import API_TOKEN

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
LOGGER = logging.getLogger(__name__)
BOT_UTILS = Bot_utils()
KEYBOARD = [
    [InlineKeyboardButton('Stato dei parcheggi', callback_data='parks')],
    [InlineKeyboardButton('Dettagli dei parcheggi', callback_data='data')]
]
REPLY_MARKUP = InlineKeyboardMarkup(KEYBOARD)

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!\
Chiedimi lo stato dei parcheggi a Firenze con il pulsante *Stato dei parcheggi*\.\
Chiedimi i dettagli su un solo parcheggio con il pulsante *Dettagli dei parcheggi*\.\
\
©️Margin SRL\.', reply_markup=REPLY_MARKUP)

def main_choice_menu(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'parks':
        show_parking_occupancy(query)
    elif query.data == 'data':
        show_list_parkings(query)
    else:
        show_parking_details(query)    

def show_parking_details(query) -> None:
    query.edit_message_text(text=BOT_UTILS.get_parking_details(query), reply_markup=REPLY_MARKUP)

def show_parking_occupancy(query) -> None:
    query.edit_message_text("Elaboro dati...")
    query.edit_message_text(BOT_UTILS.get_parking_occupancy_info(), parse_mode='MarkdownV2', disable_web_page_preview=True, reply_markup=REPLY_MARKUP)

def show_list_parkings(query) -> None:
    keyboard = []
    for parking in BOT_UTILS.get_parking_names():
        keyboard.append([InlineKeyboardButton(parking, callback_data=BOT_UTILS.get_parking_names().get(parking))])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text='Scegli un parcheggio:', reply_markup=reply_markup)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(API_TOKEN)
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(main_choice_menu))
    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, start))
    # Start the Bot
    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
