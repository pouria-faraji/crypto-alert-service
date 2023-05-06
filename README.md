# Automated Crypto Data Fetching and Alert System via Telegram
This project is an automated service that fetches cryptocurrency data every 2 hours and sends alert messages via Telegram based on specific conditions. It uses APIs to gather data and integrates with Telegram's Bot API for messaging. The code is written in a Python script that can be easily deployed and configured for personal use. APIs are implemented using [FastAPI](https://fastapi.tiangolo.com/).

## Cryptocurrencies
The list of tokens are as follows. This list can be modified in the `crypto.py` file.

```python
watchlist = ['BTC', 'ETH', 'BNB', 'ADA', 'SOL', 'XRP', 'LINK', 'LTC', 'MATIC', 'BCH', 'XLM', 'FTM', 'ONE', 'HOT', 'CELR', 'TOMO', 'FORTH', 'BEAM']
```
## Data Source
Data are fetched from [CoinMarketCap](https://coinmarketcap.com/), and you must have an account in order to get data from their APIs. After creating an account, you will get an API key, and you must use this API key inside your request's header. Create a file and name it `alert.env`. Then put an environment variable called `X_CMC_PRO_API_KEY` and use it in the code.

```
X_CMC_PRO_API_KEY = your API key
```

You can use this variable in `headers` attribute of `CryptoService` class in `crypto.py` file.
``` python
headers = {
    'Accepts': 'application/json',
    #'X-CMC_PRO_API_KEY': os.getenv('X_CMC_PRO_API_KEY_TEST', 'YOUR_TEST_API_KEY'), # Only for Test
    'X-CMC_PRO_API_KEY': os.getenv('X_CMC_PRO_API_KEY', 'YOUR_API_KEY'),
    }
```
## Data Model
The recieved data from CoinMarketCap are then used to create the `Token` data model.
```python
class Token(BaseModel):
    name:str
    symbol: str
    price:float
    percent_change_1h: Optional[float]
    percent_change_24h: Optional[float]
    percent_change_7d: Optional[float]
```

## Conditions
The alerts are sent to the Telegram if any of the following two conditions are met:
- The change percentage of 1 hour, or 24 hours, or 7 days is less than -10%
- The change percentage of 1 hour, or 24 hours, or 7 days is more than 20%

In the first case, the tokens are considered good candidate for buying, and for the second case, they are considered good candidate for selling.

## Telegram
In order to send messages to your Telegram, you must create a bot using official Telegram [tutorial](https://core.telegram.org/bots/tutorial).

Then you recieve a bot token and a chat ID which you must put them inside the `alert.env` file you created earlier. So, finally your environment variables file looks like this:
```
X_CMC_PRO_API_KEY = xxxxx-xxxx-xxx-xxxxx
X_CMC_PRO_API_KEY_TEST = yyyyyy-yyyyy-yyy-yyyyyy
TELEGRAM_TOKEN = xxxxxxx:yyyyyyyyy
CHAT_ID = zzzzzzzzz
```
`TELEGRAM_TOKEN` and `CHAT_ID` are used in `telegram.py` file as the two parameteres of the `TelegramService` class.
```python
class TelegramService():
   token = os.getenv('TELEGRAM_TOKEN', 'YOUR_TELEGRAM_TOKEN')
   chatID = os.getenv('CHAT_ID', 'YOUR_CHAT_ID')
   ...
```

## Run the application
Simply run the following command:

```
docker-compose up -d --build
```