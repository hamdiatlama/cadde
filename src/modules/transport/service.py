import random
import string
from datetime import datetime, timedelta
from src.modules.transport.repository import TransportRepository
from src.modules.transport.models import TicketStatus


def generate_ticket_no():
    return "TCK" + "".join(random.choices(string.digits, k=10))


def generate_qr(ticket_no: str):
    return f"https://cadde.app/bilet/{ticket_no}"


class TransportService:
    def __init__(self, repo: TransportRepository):
        self.repo = repo

    # ─── Arama / Route-based search ─────────────────────
    async def search_trips(self, origin_id: int, destination_id: int, date: str,
                           vehicle_type: str = None, **filters):
        return await self.repo.search_schedules(origin_id, destination_id, date, vehicle_type, **filters)

    async def search_by_location(self, from_lat: float, from_lng: float,
                                  to_lat: float, to_lng: float, date: str,
                                  vehicle_type: str = None):
        """Find routes passing near the user's location"""
        routes = await self.repo.list_routes(vehicle_type=vehicle_type)
        matching = []
        for r in routes:
            stops = await self.repo.list_route_stops(r.id, can_pickup=True)
            for s in stops:
                if s.lat and s.lng:
                    dist = ((s.lat - from_lat) ** 2 + (s.lng - from_lng) ** 2) ** 0.5
                    if dist < 0.05:
                        schedules = await self.repo.search_schedules(
                            r.origin_station_id, r.destination_station_id, date,
                            vehicle_type=vehicle_type, company_id=r.company_id,
                            is_pickup_route=True,
                        )
                        matching.extend(schedules)
                        break
        return matching

    async def get_schedule_with_details(self, schedule_id: int):
        return await self.repo.get_schedule_with_details(schedule_id)

    async def get_route_stops(self, schedule_id: int):
        return await self.repo.list_schedule_stops(schedule_id)

    async def get_available_seats(self, schedule_id: int, seat_class: str = None):
        seats = await self.repo.list_seats(schedule_id, seat_class)
        return [s for s in seats if s.is_available]

    # ─── Bilet Satın Alma ───────────────────────────────
    async def buy_ticket(self, user_id: int, schedule_id: int, seat_id: int,
                         passenger_name: str, passenger_surname: str = None,
                         passenger_id_no: str = None, passenger_phone: str = None,
                         passenger_email: str = None,
                         pickup_stop_id: int = None, dropoff_stop_id: int = None,
                         pickup_lat: float = None, pickup_lng: float = None,
                         pickup_address: str = None):
        seat = await self.repo.get_seat(seat_id)
        if not seat or not seat.is_available:
            raise ValueError("Seçilen koltuk müsait değil")
        schedule = await self.repo.get_schedule(schedule_id)
        if not schedule or schedule.available_seats <= 0:
            raise ValueError("Seferde boş koltuk yok")
        ticket_no = generate_ticket_no()
        ticket = await self.repo.create_ticket({
            "ticket_no": ticket_no, "schedule_id": schedule_id,
            "seat_id": seat_id, "user_id": user_id,
            "pickup_stop_id": pickup_stop_id, "dropoff_stop_id": dropoff_stop_id,
            "passenger_name": passenger_name, "passenger_surname": passenger_surname,
            "passenger_id_no": passenger_id_no, "passenger_phone": passenger_phone,
            "passenger_email": passenger_email,
            "pickup_lat": pickup_lat, "pickup_lng": pickup_lng,
            "pickup_address": pickup_address,
            "price": seat.price or schedule.base_price,
            "status": TicketStatus.CONFIRMED,
            "qr_code": generate_qr(ticket_no),
        })
        await self.repo.update_seat_availability(seat_id, False)
        await self.repo.update_schedule_seats(schedule_id, -1)
        # If pickup stop, create pickup booking
        if pickup_stop_id:
            stop = await self.repo.get_route_stop(pickup_stop_id)
            stop_times = await self.repo.list_schedule_stops(schedule_id)
            pickup_time = None
            for st in stop_times:
                if st.route_stop_id == pickup_stop_id:
                    pickup_time = st.estimated_time
                    break
            await self.repo.create_pickup_booking({
                "ticket_id": ticket.id, "schedule_id": schedule_id,
                "pickup_stop_id": pickup_stop_id, "pickup_time": pickup_time,
                "passenger_phone": passenger_phone, "status": "confirmed",
            })
        return ticket

    async def cancel_ticket(self, ticket_no: str, user_id: int, reason: str = None):
        ticket = await self.repo.get_ticket(ticket_no)
        if not ticket: raise ValueError("Bilet bulunamadı")
        if ticket.user_id != user_id: raise ValueError("Bu bilet size ait değil")
        if ticket.status == TicketStatus.CANCELLED: raise ValueError("Bilet zaten iptal edilmiş")
        ticket = await self.repo.update_ticket_status(ticket.id, "cancelled", reason)
        if ticket.seat_id:
            await self.repo.update_seat_availability(ticket.seat_id, True)
        await self.repo.update_schedule_seats(ticket.schedule_id, 1)
        return ticket

    async def get_user_tickets(self, user_id: int, status: str = None):
        return await self.repo.list_user_tickets(user_id, status)

    async def get_ticket_detail(self, ticket_no: str):
        return await self.repo.get_ticket(ticket_no)

    # ─── Firma / Araç / Şoför Yönetimi ─────────────────
    async def list_companies(self, vehicle_type: str = None, is_reseller: bool = None):
        return await self.repo.list_companies(vehicle_type, is_reseller)

    async def register_company(self, data: dict):
        return await self.repo.create_company(data)

    async def add_vehicle(self, company_id: int, data: dict):
        data["company_id"] = company_id
        return await self.repo.create_vehicle(data)

    async def add_driver(self, company_id: int, data: dict):
        data["company_id"] = company_id
        return await self.repo.create_driver(data)

    async def create_schedule(self, data: dict):
        schedule = await self.repo.create_schedule(data)
        await self.repo.generate_seats(schedule.id, data.get("total_seats", 40), data.get("base_price", 0))
        return schedule

    async def search_stations(self, query: str):
        return await self.repo.search_stations(query)

    # ─── Rota Durağı Ekleme ─────────────────────────────
    async def add_route_stop(self, route_id: int, station_id: int, name: str,
                              km_from_start: float, minutes_from_departure: int,
                              lat: float = None, lng: float = None):
        return await self.repo.create_route_stop({
            "route_id": route_id, "station_id": station_id, "name": name,
            "km_from_start": km_from_start, "minutes_from_departure": minutes_from_departure,
            "lat": lat, "lng": lng, "sort_order": minutes_from_departure,
        })

    # ─── Değerlendirme ──────────────────────────────────
    async def rate_transport(self, ticket_id: int, user_id: int, company_id: int,
                              driver_id: int = None, company_rating: int = None,
                              driver_rating: int = None, cleanliness: int = None,
                              comfort: int = None, punctuality: int = None,
                              overall: int = None, comment: str = None):
        rating = await self.repo.create_rating({
            "ticket_id": ticket_id, "company_id": company_id,
            "driver_id": driver_id, "user_id": user_id,
            "company_rating": company_rating, "driver_rating": driver_rating,
            "cleanliness_rating": cleanliness, "comfort_rating": comfort,
            "punctuality_rating": punctuality, "overall_rating": overall,
            "comment": comment,
        })
        return rating

    # ─── Bildirim / Yolcu Uyarı ─────────────────────────
    async def get_pickups_for_driver(self, driver_id: int, date: str = None):
        return await self.repo.get_driver_pickups(driver_id, date)

    async def notify_pickup(self, pickup_id: int):
        """15 dk kala yolcuya bildirim + şoföre bildirim"""
        pass  # SMS/push notification logic will be added
