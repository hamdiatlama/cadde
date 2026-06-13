from typing import Protocol


class FoodEvent:
    RESTAURANT_REGISTERED = "food.restaurant.registered"
    RESTAURANT_UPDATED = "food.restaurant.updated"
    RESTAURANT_VERIFIED = "food.restaurant.verified"
    MENU_ITEM_CREATED = "food.menu.created"
    MENU_ITEM_UPDATED = "food.menu.updated"
    MENU_ITEM_DELETED = "food.menu.deleted"
    MODIFIER_ADDED = "food.modifier.added"
    MODIFIER_DELETED = "food.modifier.deleted"
    BRANCH_ADDED = "food.branch.added"
    ZONE_ADDED = "food.zone.added"
    CHAT_MESSAGE_SENT = "food.chat.sent"
    TEMPERATURE_LOGGED = "food.temperature.logged"
    HYGIENE_REPORTED = "food.hygiene.reported"
    DRIVER_REPORTED = "food.driver.reported"
    SHIFT_STARTED = "food.shift.started"
    SHIFT_ENDED = "food.shift.ended"


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
