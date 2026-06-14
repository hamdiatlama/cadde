from contextlib import asynccontextmanager
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import init_db, engine
from src.core.cache import cache
from src.core.events import event_bus
from src.modules.user.router import router as user_router
from src.modules.courier.router import router as courier_router
from src.modules.ride.router import router as ride_router
from src.modules.food.router import router as food_router
from src.modules.seller.router import router as seller_router
from src.modules.ecommerce.order.router import router as order_router
from src.modules.ecommerce.payment.router import router as payment_router
from src.modules.ecommerce.cart.router import router as cart_router
from src.modules.review.router import router as review_router
from src.modules.subscription.router import router as subscription_router
from src.modules.support.router import router as support_router
from src.modules.account.address.router import router as address_router
from src.modules.notification.router import router as notification_router
from src.modules.store.router import router as search_router
from src.modules.bina.router import router as bina_router
from src.modules.event.router import router as event_router
from src.modules.vehicle.router import router as vehicle_router
from src.modules.expert.router import router as expert_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    _startup_time = time.time()
    await init_db()
    await cache.connect()
    await event_bus.connect()
    app.state.startup_time = _startup_time
    yield
    await cache.close()
    await event_bus.close()
    await engine.dispose()


app = FastAPI(
    title="Web Platform API",
    description="Multi-service super-app backend",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(search_router)
app.include_router(seller_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(courier_router)
app.include_router(support_router)
app.include_router(review_router)
app.include_router(subscription_router)
app.include_router(food_router)
app.include_router(ride_router)
app.include_router(cart_router)
app.include_router(address_router)
app.include_router(notification_router)
app.include_router(bina_router)
app.include_router(event_router)
app.include_router(vehicle_router)
app.include_router(expert_router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "web-platform", "uptime": time.time() - getattr(app.state, "startup_time", time.time())}
