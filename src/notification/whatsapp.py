import requests

from src import settings
from src.helpers import get_today_date
from src.utils import logger


class WhatsappNotification():

    def send(self, data: str="", type: str=""):
        if not settings.SEND_WHATSAPP_NOTIFICATION:
            logger.info("Whatsapp notification disabled.")
            return None

        if not data:
            raise ValueError("data can't be empty")

        url = settings.WHAPI_URL
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {settings.WHAPI_TOKEN}"
        }
        payload = {
            "to": settings.WHAPI_GROUP_ID,
            "body": data
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                logger.info(f"Whatsapp {type} insight sent on {get_today_date()}.")
            else:
                error_data = response.json()
                logger.error(
                    f"Failed to send whatsapp {type} insight on {get_today_date()}."
                    f"status: {response.status_code}, Error: {error_data}"
                )
        except requests.exceptions.RequestException as e:
            logger.error(f"Whatsapp API failed for {type}: {str(e)}")
