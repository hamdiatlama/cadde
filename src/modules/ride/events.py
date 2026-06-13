from typing import Protocol


class RideEvent:
    RIDE_CREATED = "ride.created"
    RIDE_ACCEPTED = "ride.accepted"
    RIDE_REJECTED = "ride.rejected"
    RIDE_ARRIVED = "ride.arrived"
    RIDE_STARTED = "ride.started"
    RIDE_COMPLETED = "ride.completed"
    RIDE_CANCELLED = "ride.cancelled"
    RIDE_RATED = "ride.rated"
    RIDE_INCIDENT_REPORTED = "ride.incident.reported"
    RIDE_GPS_ANOMALY = "ride.gps.anomaly"
    DRIVER_LOCATION_UPDATED = "driver.location.updated"


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
