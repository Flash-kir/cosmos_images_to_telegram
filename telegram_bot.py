import os

from dotenv import load_dotenv
load_dotenv()
import telegram

bot = telegram.Bot(token=os.environ.get('TELEGRAM_TOKEN'))
#print(bot.get_me())
bot.send_message(chat_id='@Cosmos_pictures', text='Hello, my subscribers! Glad to see you in my channel!')