from typing import Protocol


class SellerEvent:
    SELLER_PROFILE_UPDATED = "seller.profile.updated"
    QUESTION_ASKED = "seller.question.asked"
    QUESTION_ANSWERED = "seller.question.answered"


class EventPublisher(Protocol):
    async def publish(self, topic: str, data: dict) -> None: ...


class InMemoryPublisher:
    async def publish(self, topic: str, data: dict) -> None:
        pass


class CompositePublisher:
    def __init__(self):
        self._handlers: dict[str, list[callable]] = {}

    def on(self, topic: str, handler: callable):
        self._handlers.setdefault(topic, []).append(handler)

    async def publish(self, topic: str, data: dict) -> None:
        for handler in self._handlers.get(topic, []):
            try:
                if callable(handler):
                    await handler(data)
            except Exception:
                pass


publisher = CompositePublisher()


async def publish_event(topic: str, data: dict) -> None:
    await publisher.publish(topic, data)


def on_event(topic: str):
    def decorator(func):
        publisher.on(topic, func)
        return func
    return decorator
