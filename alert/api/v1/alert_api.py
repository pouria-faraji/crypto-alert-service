from threading import Thread

import fastapi
from alert.crypto import CryptoService
from alert.schedule import Schedule
from alert.telegram import TelegramService
from fastapi import APIRouter, status
from starlette.responses import JSONResponse, Response

alert_api_router = APIRouter(tags=["Crypto Alert API"])

@alert_api_router.get("/listings")
async def get_listing():
    crypto_service = CryptoService()
    result = await crypto_service.get_listings()
    return result

@alert_api_router.get("/data")
async def get_data():
    crypto_service = CryptoService()
    result = await crypto_service.extract_data()
    return result


@alert_api_router.post("/send")
def send_message():
    crypto_service = CryptoService()
    result = crypto_service.get_filtered_tokens()

    telegram_service = TelegramService()

    for token in result:
        telegram_service.send_telegram_message(token)

    #return JSONResponse(result)
    return Response(status_code=status.HTTP_200_OK)

@alert_api_router.get("/status")
def check_schedule_status():
    result = {'Started': Schedule.STARTED}
    return JSONResponse(result, status_code=status.HTTP_200_OK)

@alert_api_router.get("/start")
def start():
    def start_thread():
        Schedule.s.enter(0, Schedule.priority, Schedule.get_crypto_send_telegram)
        Schedule.s.run()

    if not Schedule.STARTED:
        Schedule.STARTED = True
        thread = Thread(target = start_thread)
        thread.start()
        return Response("Started", status_code=status.HTTP_200_OK)
    else:
        return Response("The service is already started.", status_code=status.HTTP_200_OK)

@alert_api_router.get("/stop")
def stop():
    if Schedule.STARTED:
        Schedule.s.cancel(Schedule.event)
        Schedule.STARTED = False
        return Response("Stopped", status_code=status.HTTP_200_OK)
    else:
        return Response("The service is already stopped.", status_code=status.HTTP_200_OK)
