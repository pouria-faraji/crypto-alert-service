import os
from typing import Dict

import requests

from alert.model.token import Token


class TelegramService():
   token = os.getenv('TELEGRAM_TOKEN', 'YOUR_TELEGRAM_TOKEN')
   chatID = os.getenv('CHAT_ID', 'YOUR_CHAT_ID')
   def format_text(self, token:Token):
       output = f"""
<b>Name:</b> {token.name}
<b>Symbol:</b> {token.symbol}
<b>Price:</b> {token.price}
<b>1h Change:</b>  {round(token.percent_change_1h, 2)}%
<b>24h Change:</b> {round(token.percent_change_24h, 2)}%
<b>7d Change:</b>  {round(token.percent_change_7d, 2)}%
       """
       return output

   def send_telegram_message(self, token:Token):
       formatted_message = self.format_text(token)
       url = 'https://api.telegram.org/bot' + self.token + '/sendMessage?chat_id=' + self.chatID + '&parse_mode=HTML&text=' + formatted_message
       response = requests.get(url)
       return response.json()

