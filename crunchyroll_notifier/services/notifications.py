import requests
import logging

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)

class NotificationService:
    def __init__(self, notification_client = None):
        self.notification_client = notification_client        

    def configure_pushover_client(self, config: dict):
        self.notification_client = PushoverClient(config.get('user_token'), config.get('app_token'))

    @staticmethod
    def get_notifications(notification_title, data, sound):
        return [CrunchyNotification(notification_title, f"{item.series_title} - {item.season_number}x{item.episode_number} - {item.title}", sound) for item in data]

    def notify(self, data):
        return self.notification_client.notify(data)

class CrunchyNotification:
    def __init__(self, title, message, sound):
        self.title = title
        self.message = message
        self.sound = sound

class PushoverClient:
    def __init__(self, user_token: str, app_token: str):
        self.user_token = user_token
        self.app_token = app_token

    def notify(self, data: CrunchyNotification):
        request_data = {
            "token": self.app_token,
            "user": self.user_token,
            "title": data.title,
            "message": data.message,
            "sound": data.sound
        }

        return requests.post("https://api.pushover.net/1/messages.json", request_data)