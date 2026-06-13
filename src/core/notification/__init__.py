"""FCM push notification sender (adapter pattern)."""
from typing import Optional

from src.config import FCM_CREDENTIALS_PATH

try:
    import firebase_admin
    from firebase_admin import credentials, messaging
    _fcm_available = True
except ImportError:
    firebase_admin = None
    _fcm_available = False


class FCMClient:
    def __init__(self, credentials_path: str = FCM_CREDENTIALS_PATH):
        self._app = None
        self._credentials_path = credentials_path

    def initialize(self):
        if self._app is None and firebase_admin:
            try:
                cred = credentials.Certificate(self._credentials_path)
                self._app = firebase_admin.initialize_app(cred)
            except Exception:
                pass

    def send_to_device(self, device_token: str, title: str, body: str, data: Optional[dict] = None) -> bool:
        if not self._app:
            return False
        message = messaging.Message(
            token=device_token,
            notification=messaging.Notification(title=title, body=body),
            data=data or {},
        )
        try:
            messaging.send(message)
            return True
        except Exception:
            return False

    def send_to_topic(self, topic: str, title: str, body: str, data: Optional[dict] = None) -> bool:
        if not self._app:
            return False
        message = messaging.Message(
            topic=topic,
            notification=messaging.Notification(title=title, body=body),
            data=data or {},
        )
        try:
            messaging.send(message)
            return True
        except Exception:
            return False


fcm = FCMClient()
