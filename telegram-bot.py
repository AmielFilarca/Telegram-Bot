import re
import requests
from telegram.ext.dispatcher import run_async
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
import logging
import feedparser
import telegram
from functools import wraps


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
######################## Commands ########################
@send_typing_action
def start(update, context):
    """Send a message when the command /start is issued."""
    keyboard = [['/meme 😂', '/news 📰'], ['/doge 🐶',
                                         '/cat 🐱', '/dog_fact 🐕', '/cat_fact 🐈'], ['/help ❓']]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True, selective=True)
    firstName = update.message.from_user.first_name
    if firstName == 'Amiel':
        update.message.reply_text(
            'Hi {}! I am your sex bot. \nFor more info, use /help.'.format(firstName), reply_markup=reply_markup)
    else:
        update.message.reply_text(
            'Hi {}! I am Amiel\'s sex bot. \nFor more info, use /help.'.format(firstName), reply_markup=reply_markup)


@send_typing_action
def help(update, context):
    """Send a message when the command /help is issued."""

    keyboard = [['/meme 😂', '/news 📰'], ['/doge 🐶',
                                         '/cat 🐱', '/dog_fact 🐕', '/cat_fact 🐈'], ['/help ❓']]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True, selective=True)
    update.message.reply_text(
        'Use /meme for a meme. \nUse /doge or /cat for a picture. \nUse /dog_fact or /cat_fact for a fact. \nUse /news for the latest article.', reply_markup=reply_markup)


@send_typing_action
def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


######################## Random Dog Picture ########################
def get_dog_url():
    """Get random dog url from json"""
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url


def get_dog_image_url():
    """Get random dog image url"""
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_dog_url()
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    return url


@send_typing_action
@run_async
def doge(update, context):
    """Send random dog image"""
    chat_id = update.message.chat_id
    url = get_dog_image_url()
    context.bot.send_photo(chat_id=chat_id, photo=url)


######################## Random Cat Picture ########################
def get_cat_url():
    """Get random cat url from json"""
    # contents = requests.get(
    #     'https://api.thecatapi.com/v1/images/search').json()
    # contents = contents[0]
    # url = contents['url']
    # return url
    contents = requests.get(
        'http://aws.random.cat/meow').json()
    url = contents['file']
    return url


def get_cat_image_url():
    """Get random cat image url"""
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_cat_url()
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    return url


@send_typing_action
@run_async
def cat(update, context):
    chat_id = update.message.chat_id
    """Send random cat image"""
    url = get_cat_image_url()
    context.bot.send_photo(chat_id=chat_id, photo=url)


######################## Random Dog Fact ########################
def get_dog_fact():
    json = requests.get('https://some-random-api.ml/facts/dog').json()
    fact = json['fact']
    return fact


@send_typing_action
def dog_fact(update, context):
    fact = get_dog_fact()
    context.bot.send_message(chat_id=update.effective_chat.id, text=fact)


######################## Random Cat Fact ########################
def get_cat_fact():
    json = requests.get('https://catfact.ninja/fact').json()
    fact = json['fact']
    return fact


@send_typing_action
def cat_fact(update, context):
    fact = get_cat_fact()
    context.bot.send_message(chat_id=update.effective_chat.id, text=fact)


######################## Random Meme ########################
def get_meme_contents():
    contents = requests.get('https://meme-api.herokuapp.com/gimme').json()
    return contents


@send_typing_action
def meme(update, context):
    chat_id = update.message.chat_id
    contents = get_meme_contents()
    caption = contents['title']
    image = image = contents['url']
    context.bot.send_photo(chat_id=chat_id, photo=image)
    context.bot.send_message(chat_id=update.effective_chat.id, text=caption)


######################## News ########################
@send_typing_action
def news(update, context):
    chat_id = update.message.chat_id
    NewsFeed = feedparser.parse("https://rss.app/feeds/06baSi0bagPEqNTP.xml")
    entry = NewsFeed.entries[0]
    # print(entry.keys())
    title = ''
    published = ''
    media_content = ''
    summary = ''
    link = ''
    author = ''

    if 'title' in entry.keys():
        # print(entry.title)
        title = entry.title
    if 'published' in entry.keys():
        # print(entry.published)
        published = str(entry.published)
        published = published[0:17]
    if 'media_content' in entry.keys():
        thisdict = entry.media_content[0]
        if thisdict['medium'] == 'image':
            # print(thisdict.get('url'))
            media_content = thisdict.get('url')
    if 'summary' in entry.keys():
        # print(entry.summary)
        summary = str(entry.summary)
        split_list = summary.split("<div>")
        summary = split_list[2]
        length = len(summary) + 1
        summary = summary[-length:-12]
    if 'link' in entry.keys():
        # print(entry.link)
        link = entry.link
    if 'author' in entry.keys():
        # print(entry.author)
        author = entry.author

    text = f'{title}'
    image = f'{media_content}'
    subtext = f'{summary}\n\n{author} ● {published}'

    context.bot.send_message(chat_id=chat_id, text=text)
    context.bot.send_photo(chat_id=chat_id, photo=image)
    context.bot.send_message(chat_id=chat_id, text=subtext)


######################## Main ########################
def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        "1012535764:AAHvhJ5sJy-bU7kpR9Fr3YNEaSNHFSXm0ao", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("doge", doge))
    dp.add_handler(CommandHandler("cat", cat))
    dp.add_handler(CommandHandler("dog_fact", dog_fact))
    dp.add_handler(CommandHandler("cat_fact", cat_fact))
    dp.add_handler(CommandHandler("meme", meme))
    dp.add_handler(CommandHandler("news", news))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
