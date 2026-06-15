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
from src.modules.vehicle.listings import router as vehicle_listings_router
from src.modules.expert.router import router as expert_router
from src.modules.realestate.router import router as realestate_router
from src.modules.food_supplier.router import router as food_supplier_router
from src.modules.cicek.router import router as cicek_router
from src.modules.cargo.router import router as cargo_router
from src.modules.wishlist.router import router as wishlist_router
from src.modules.campaign.router import router as campaign_router
from src.modules.escrow.router import router as escrow_router
from src.modules.payout.router import router as payout_router
from src.modules.dashboard.router import router as dashboard_router
from src.modules.advertising.router import router as advertising_router
from src.modules.comparison.router import router as comparison_router
from src.modules.protection.router import router as protection_router
from src.modules.i18n.router import router as i18n_router
from src.modules.store.coupon_router import router as coupon_router
from src.modules.variant.router import router as variant_router
from src.modules.chat.router import router as chat_router
from src.modules.b2b.router import router as b2b_router
from src.modules.tax.router import router as tax_router
from src.modules.warehouse.router import router as warehouse_router
from src.modules.abandoned_cart.router import router as abandoned_cart_router
from src.modules.seller_performance.router import router as seller_performance_router
from src.modules.multiseller.router import router as multiseller_router
from src.modules.auction.router import router as auction_router
from src.modules.gift_card.router import router as gift_card_router
from src.modules.payment_extended.router import router as payment_extended_router
from src.modules.commission.router import router as commission_router
from src.modules.loyalty.router import router as loyalty_router
from src.modules.marketing.router import router as marketing_router
from src.modules.fulfillment.router import router as fulfillment_router
from src.modules.delivery_extended.router import router as delivery_extended_router
from src.modules.subscribe_save.router import router as subscribe_save_router
from src.modules.recommendation.router import router as recommendation_router
from src.modules.live_shopping.router import router as live_shopping_router
from src.modules.return_management.router import router as return_management_router
from src.modules.trade_in.router import router as trade_in_router
from src.modules.handmade.router import router as handmade_router
from src.modules.brand.router import router as brand_router
from src.modules.dropshipping.router import router as dropshipping_router
from src.modules.verification.router import router as verification_router
from src.modules.chatbot.router import router as chatbot_router
from src.modules.marketplace_core.router import router as marketplace_core_router
from src.modules.social_commerce.router import router as social_commerce_router
from src.modules.developer.router import router as developer_router
from src.modules.fraud.router import router as fraud_router
from src.modules.product_enhanced.router import router as product_enhanced_router
from src.modules.tax_extended.router import router as tax_extended_router
from src.modules.logistics_advanced.router import router as logistics_advanced_router
from src.modules.compliance.router import router as compliance_router
from src.modules.seller_tools.router import router as seller_tools_router
from src.modules.customer_service.router import router as customer_service_router
from src.modules.storefront.router import router as storefront_router
from src.modules.pos.router import router as pos_router
from src.modules.messaging.router import router as messaging_router
from src.modules.payment_vault.router import router as payment_vault_router
from src.modules.dynamic_pricing.router import router as dynamic_pricing_router
from src.modules.analytics.router import router as analytics_router
from src.modules.integration.router import router as integration_router
from src.modules.payout_extended.router import router as payout_extended_router
from src.modules.marketing_automation.router import router as marketing_automation_router
from src.modules.mobile_sdk.router import router as mobile_sdk_router
from src.modules.hotel.router import router as hotel_router
from src.modules.accommodation.router import router as accommodation_router
from src.modules.payment_gateway.router import router as payment_gateway_router
from src.modules.digital_compendium.router import router as digital_compendium_router
from src.modules.energy_manager.router import router as energy_manager_router
from src.modules.channel_manager.router import router as channel_manager_router
from src.modules.hotel_revenue.router import router as hotel_revenue_router
from src.modules.multi_property.router import router as multi_property_router
from src.modules.mobile_checkin.router import router as mobile_checkin_router
from src.modules.reputation.router import router as reputation_router
from src.modules.upselling.router import router as upselling_router
from src.modules.website_builder.router import router as website_builder_router
from src.modules.ai_concierge.router import router as ai_concierge_router
from src.modules.iot_manager.router import router as iot_manager_router
from src.modules.agency.router import router as agency_router
from src.modules.tourism.router import router as tourism_router
from src.modules.rental.router import router as rental_router
from src.modules.trip_planner.router import router as trip_planner_router
from src.modules.transport.router import router as transport_router


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
app.include_router(vehicle_listings_router)
app.include_router(expert_router)
app.include_router(realestate_router)
app.include_router(food_supplier_router)
app.include_router(cicek_router)
app.include_router(cargo_router)
app.include_router(wishlist_router)
app.include_router(campaign_router)
app.include_router(escrow_router)
app.include_router(payout_router)
app.include_router(dashboard_router)
app.include_router(advertising_router)
app.include_router(comparison_router)
app.include_router(protection_router)
app.include_router(i18n_router)
app.include_router(coupon_router)
app.include_router(variant_router)
app.include_router(chat_router)
app.include_router(b2b_router)
app.include_router(tax_router)
app.include_router(warehouse_router)
app.include_router(abandoned_cart_router)
app.include_router(seller_performance_router)
app.include_router(multiseller_router)
app.include_router(auction_router)
app.include_router(gift_card_router)
app.include_router(payment_extended_router)
app.include_router(commission_router)
app.include_router(loyalty_router)
app.include_router(marketing_router)
app.include_router(fulfillment_router)
app.include_router(delivery_extended_router)
app.include_router(subscribe_save_router)
app.include_router(recommendation_router)
app.include_router(live_shopping_router)
app.include_router(return_management_router)
app.include_router(trade_in_router)
app.include_router(handmade_router)
app.include_router(brand_router)
app.include_router(dropshipping_router)
app.include_router(verification_router)
app.include_router(chatbot_router)
app.include_router(marketplace_core_router)
app.include_router(social_commerce_router)
app.include_router(developer_router)
app.include_router(fraud_router)
app.include_router(product_enhanced_router)
app.include_router(tax_extended_router)
app.include_router(logistics_advanced_router)
app.include_router(compliance_router)
app.include_router(seller_tools_router)
app.include_router(customer_service_router)
app.include_router(storefront_router)
app.include_router(pos_router)
app.include_router(messaging_router)
app.include_router(payment_vault_router)
app.include_router(dynamic_pricing_router)
app.include_router(analytics_router)
app.include_router(integration_router)
app.include_router(payout_extended_router)
app.include_router(marketing_automation_router)
app.include_router(mobile_sdk_router)
app.include_router(hotel_router)
app.include_router(accommodation_router)
app.include_router(payment_gateway_router)
app.include_router(digital_compendium_router)
app.include_router(energy_manager_router)
app.include_router(channel_manager_router)
app.include_router(hotel_revenue_router)
app.include_router(multi_property_router)
app.include_router(mobile_checkin_router)
app.include_router(reputation_router)
app.include_router(upselling_router)
app.include_router(website_builder_router)
app.include_router(ai_concierge_router)
app.include_router(iot_manager_router)
app.include_router(agency_router)
app.include_router(tourism_router)
app.include_router(rental_router)
app.include_router(trip_planner_router)
app.include_router(transport_router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "web-platform", "uptime": time.time() - getattr(app.state, "startup_time", time.time())}
