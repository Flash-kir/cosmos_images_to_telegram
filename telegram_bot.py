import os

from dotenv import load_dotenv
load_dotenv()
import telegram

chat_id = '@Cosmos_pictures'
bot = telegram.Bot(token=os.environ.get('TELEGRAM_TOKEN'))
#print(bot.get_me())
bot.send_message(chat_id=chat_id, text='Image from spacex launch')
bot.send_document(chat_id=chat_id, document=open('images/50291306061_2f9e350a85_o.jpg', 'rb'))