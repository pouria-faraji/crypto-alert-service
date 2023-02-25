import datetime
import sched
import time
from datetime import timezone
from typing import List

import pytz
from loguru import logger

from alert.crypto import CryptoService
from alert.model.token import Token
from alert.telegram import TelegramService


class Schedule(object):
    STARTED: bool = False
    s = sched.scheduler(time.time, time.sleep)
    delay = 60 * 60 * 2 # Seconds, every 2 hours
    priority = 1
    event = None



    @staticmethod
    def get_crypto_send_telegram():
        now = datetime.datetime.now(pytz.timezone('Europe/Rome'))

        if Schedule.STARTED and now.hour > 8:
            logger.debug("Getting crypto list and sending to telegram")
            crypto_service = CryptoService()
            result:List[Token] = crypto_service.get_filtered_tokens()

            logger.debug(f"Returned tokens: {[token.symbol for token in result]}")

            telegram_service = TelegramService()

            for token in result:
                telegram_service.send_telegram_message(token)
        Schedule.event = Schedule.s.enter(Schedule.delay, Schedule.priority, Schedule.get_crypto_send_telegram)

