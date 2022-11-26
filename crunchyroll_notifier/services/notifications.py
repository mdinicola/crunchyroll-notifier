import requests
import logging

_logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        pass

    @classmethod
    def get_notifications(self, data):
        return [CrunchyNotification(f"New anime released: {item.title}") for item in data]

class CrunchyNotification:
    def __init__(self, message):
        self.message = message