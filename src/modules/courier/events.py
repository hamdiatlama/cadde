"""Event publishing abstraction for courier domain.

In production, this would publish to NATS/RabbitMQ for async processing.
Currently uses an in-memory handler pattern for easy future migration.
"""

from typing import Protocol, Any


class CourierEvent:
    COURIER_LOCATION_UPDATED = "courier.location.updated"
    COURIER_ASSIGNED = "courier.assigned"
    COURIER_DELIVERED = "courier.delivered"
    COURIER_SHIFT_STARTED = "courier.shift.started"
    COURIER_SHIFT_ENDED = "courier.shift.ended"
    COURIER_GPS_ANOMALY = "courier.gps.anomaly"


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
