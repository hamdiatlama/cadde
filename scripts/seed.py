"""Seed database with sample data for all domains."""
import asyncio, sys, os
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./web_platform.db")

from sqlalchemy import select
from src.database import init_db, async_session
from src.core.auth import hash_password


async def seed():
    await init_db()
    async with async_session() as db:
        from src.modules.user.models import User
        from src.modules.seller.models import Seller, Question
        from src.modules.store.models import Product
        from src.modules.courier.models import Courier
        from src.modules.food.models import Restaurant, RestaurantBranch, FoodMenuItem, MenuItemModifier, DeliveryZone
        from src.modules.ride.models import Driver
        from src.modules.support.models import SupportTicket, TicketMessage
        from src.modules.notification.models import Notification
        from src.modules.ecommerce.payment.models import Payment, Invoice, PointsTransaction
        from src.modules.review.models import Review
        from src.modules.subscription.models import Subscription
        from src.modules.bina.models import (
            Site, Blok, Daire, Kisi, Duyuru, Aidat, Gelir, Gider,
            Arac, Personel, Firma, IsTalebi, Sayac, Kargo, Ziyaretci,
        )
        from src.modules.event.models import Venue, VenueSection, Event, EventSession, SessionPricing, Seat
        from src.modules.vehicle.models import (
            VehicleCategory, VehicleSegment, BodyType, VehicleBrand, VehicleModel,
            VehicleModelBodyType, VehicleCategoryModel, VehicleModelYear,
            FeatureGroup, Feature, VehicleModelFeature,
        )
        from src.modules.expert.models import (
            ExpertCompany, ExpertPackage,
        )

        seller_user = User(
            email="florist@test.com", phone="555-1000",
            password_hash=hash_password("123123"),
            full_name="Ahmet Cicekci", role="seller",
        )
        db.add(seller_user)
        await db.flush()

        customer_user = User(
            email="customer@test.com", phone="555-2000",
            password_hash=hash_password("123123"),
            full_name="Ayse Yilmaz", role="customer",
        )
        db.add(customer_user)
        await db.flush()

        courier_user = User(
            email="courier@test.com", phone="555-3000",
            password_hash=hash_password("123123"),
            full_name="Mehmet Kurye", role="courier",
        )
        db.add(courier_user)
        await db.flush()

        admin_user = User(
            email="admin@test.com", phone="555-4000",
            password_hash=hash_password("123123"),
            full_name="Admin", role="admin",
        )
        db.add(admin_user)
        await db.flush()

        seller = Seller(
            user_id=seller_user.id, store_name="Ahmet'in Cicek Evi",
            slug="ahmetin-cicek-evi", description="Taze cicekler, hizli teslimat",
            phone="555-1001", address="Bagdat Cad. No:123, Kadikoy",
            latitude=40.9900, longitude=29.0270,
        )
        db.add(seller)
        await db.flush()

        products_data = [
            ("Kirmizi Gul Buketi", "cicek", "buket", 299.90, 50, 4.8, 120, "kirmizi,gul"),
            ("Beyaz Zambak", "cicek", "cicek", 249.90, 30, 4.5, 45, "beyaz,zambak"),
            ("Papatya Buketi", "cicek", "buket", 149.90, 80, 4.2, 200, "sari,papatya"),
            ("Orkide", "cicek", "saksı", 399.90, 15, 4.9, 60, "mor,orkide"),
            ("Gul + Papatya Karisim", "cicek", "buket", 199.90, 40, 4.6, 90, "kirmizi,sari,gul,papatya"),
            ("Lavanta Buketi", "cicek", "buket", 179.90, 25, 4.7, 150, "mor,lavanta"),
        ]
        for name, cat, sub, price, stock, rating, rc, tags in products_data:
            p = Product(
                seller_id=seller.id, name=name, slug=name.lower().replace(" ", "-"),
                category=cat, subcategory=sub, price=price, stock=stock,
                rating=rating, review_count=rc, tags=tags,
            )
            db.add(p)

        food_seller = User(
            email="food@seller.com", password_hash=hash_password("123"),
            full_name="Adana Kebap Evi", role="seller",
        )
        db.add(food_seller)
        await db.flush()

        food_seller_profile = Seller(
            user_id=food_seller.id, store_name="Adana Kebap Evi",
            slug="adana-kebap-evi", description="Gerçek odun atesinde Adana kebap",
            phone="212-555-0101",
        )
        db.add(food_seller_profile)
        await db.flush()

        restaurant = Restaurant(
            seller_id=food_seller_profile.id, name="Adana Kebap Evi",
            cuisine_type="Turk", opening_time="10:00", closing_time="23:00",
            min_order_amount=50, delivery_fee=24.90,
            free_delivery_min_amount=120, preparation_time_min=20,
            verification_status="verified",
        )
        db.add(restaurant)
        await db.flush()

        branch = RestaurantBranch(
            restaurant_id=restaurant.id, name="Kadikoy Subesi",
            address="Caferaga Mah. Sifa Sok. No:5, Kadikoy",
            latitude=40.9900, longitude=29.0270,
        )
        db.add(branch)

        menu = [
            ("Adana Kebap", "main", 180.0, 650, 35.0, 28.0, True, True, "et,domates,biber"),
            ("Lahmacun", "main", 45.0, 350, 18.0, 15.0, False, False, "bugday,etin"),
            ("Peynirli Pide", "main", 95.0, 420, 22.0, 14.0, True, False, "bugday,sut"),
            ("Coban Salata", "starter", 55.0, 120, 2.0, 8.0, True, True, ""),
            ("Baklava (4'lu)", "dessert", 85.0, 320, 4.0, 5.0, True, False, "bugday,fistik"),
            ("Ayran", "drink", 20.0, 60, 2.0, 3.0, True, True, "sut"),
        ]
        for name, cat, price, cal, prot, fat, veg, hal, aller in menu:
            item = FoodMenuItem(
                restaurant_id=restaurant.id, name=name, category=cat, price=price,
                calories_kcal=cal, protein_g=prot, fat_g=fat,
                is_vegetarian=veg, is_halal=hal, allergens=aller,
            )
            db.add(item)

        courier = Courier(
            user_id=courier_user.id, vehicle_type="motorcycle",
            vehicle_plate="34 ABC 123", is_available=True,
            current_latitude=40.9920, current_longitude=29.0250,
        )
        db.add(courier)

        driver = Driver(
            user_id=courier_user.id, is_available=True,
            license_plate="34 XYZ 789", vehicle_model="Sedan",
            vehicle_color="Beyaz",
        )
        db.add(driver)

        # ── Food Modifiers & Zones ──
        items = await db.execute(select(FoodMenuItem))
        for item in items.scalars():
            db.add(MenuItemModifier(menu_item_id=item.id, group_name="Porsiyon", name="Büyük",
                                     price_modifier=item.price * 0.3, max_select=1))
        db.add(DeliveryZone(restaurant_id=restaurant.id, name="Kadıköy Merkez",
                             min_latitude=40.98, max_latitude=41.00,
                             min_longitude=29.01, max_longitude=29.04))
        db.add(DeliveryZone(restaurant_id=restaurant.id, name="Moda",
                             min_latitude=40.98, max_latitude=40.995,
                             min_longitude=29.01, max_longitude=29.03))

        # ── Support Tickets ──
        ticket = SupportTicket(user_id=customer_user.id, subject="Sipariş geç geldi",
                                category="teslimat", status="open", priority="normal")
        db.add(ticket)
        await db.flush()
        db.add(TicketMessage(ticket_id=ticket.id, sender_id=customer_user.id,
                              message="Siparişim 2 saat geç geldi, ürünler soğumuştu."))
        db.add(TicketMessage(ticket_id=ticket.id, sender_id=admin_user.id,
                              message="Üzgünüz, ilgili kurye ile görüşüldü. Bir sonraki siparişinizde geçerli 50 TL kupon tanımlandı.",
                              is_staff=True))

        # ── Notifications ──
        db.add(Notification(user_id=seller_user.id, type="new_order",
                             title="Yeni Sipariş", message="1 adet yeni siparişiniz var."))
        db.add(Notification(user_id=customer_user.id, type="order_delivered",
                             title="Sipariş Teslim Edildi",
                             message="Kırmızı Gül Buketi teslim edildi."))

        # ── Payment & Invoice ──
        payment = Payment(order_id=1, user_id=customer_user.id, method="card",
                           amount=299.90, status="completed")
        db.add(payment)
        await db.flush()
        db.add(Invoice(order_id=1, user_id=customer_user.id,
                        invoice_no=f"INV-{seller.id}-{customer_user.id}-001",
                        amount=299.90, status="paid"))
        db.add(PointsTransaction(user_id=customer_user.id, amount=30,
                                  type="earned", description="Sipariş puanı", order_id=1))

        # ── Review ──
        products_list = await db.execute(select(Product).limit(1))
        product = products_list.scalar_one_or_none()
        if product:
            db.add(Review(order_id=1, product_id=product.id, user_id=customer_user.id,
                           rating=5, title="Harika", comment="Çok güzel ve taze çiçekler!"))

        # ── Bina / Site Yonetimi ──
        site = Site(adi="Yildiz Sitesi", adres="Cekmekoy, Istanbul", sekil="site",
                     kurucu="Ali Yildiz", banka="Is Bankasi")
        db.add(site)
        await db.flush()

        blok = Blok(site_id=site.id, adi="A Blok", kat_adet=4, daire_kat=2)
        db.add(blok)
        await db.flush()

        kapi_no = 1
        daireler_list = []
        for k in range(1, 5):
            for d in range(1, 3):
                d_obj = Daire(blok_id=blok.id, no=f"{k}{d}", kat=k, kapi_no=kapi_no, alan=100 + d * 10)
                db.add(d_obj)
                daireler_list.append(d_obj)
                kapi_no += 1
        await db.flush()

        db.add(Kisi(site_id=site.id, ad="Ali Yildiz", tel="555-0101", email="ali@yildiz.com",
                     rol="malik", daire_id=daireler_list[0].id, blok_id=blok.id, yetki="yonetici"))
        db.add(Kisi(site_id=site.id, ad="Ayse Kaya", tel="555-0102", email="ayse@mail.com",
                     rol="malik", daire_id=daireler_list[1].id, blok_id=blok.id))
        await db.flush()

        db.add(Duyuru(site_id=site.id, baslik="Genel Temizlik", icerik="15 Haziran'da genel temizlik yapilacak.",
                       kategori="duyuru", yapan="Ali Yildiz"))

        db.add(Gelir(site_id=site.id, baslik="Haziran Aidati", tutar=24000, kategori="aidat"))
        db.add(Gider(site_id=site.id, baslik="Temizlik Malzemesi", tutar=1500, kategori="temizlik"))

        db.add(Arac(site_id=site.id, plaka="34 ABC 123", sakin_ad="Ali Yildiz", tel="555-0101"))
        db.add(Personel(site_id=site.id, ad="Mehmet Temizlikci", tel="555-9999", gorev="temizlik", maas=8500))
        db.add(Firma(site_id=site.id, ad="Sistem Asansor", yetkili="Ahmet Usta", tel="555-8888", sektor="asansor"))

        db.add(Aidat(site_id=site.id, daire_id=daireler_list[0].id, blok_id=blok.id, daire_no=daireler_list[0].no,
                      ay=6, yil=2025, tutar=1500.0, kapi_no=daireler_list[0].kapi_no))
        db.add(Aidat(site_id=site.id, daire_id=daireler_list[1].id, blok_id=blok.id, daire_no=daireler_list[1].no,
                      ay=6, yil=2025, tutar=1500.0, kapi_no=daireler_list[1].kapi_no, odendi=True))

        db.add(IsTalebi(site_id=site.id, baslik="Asansor Ariza", aciklama="A Blok asansor calismiyor",
                         sektor="asansor", talep_eden_ad="Ali Yildiz"))

        db.add(Sayac(site_id=site.id, daire_id=daireler_list[0].id, blok_id=blok.id, daire_no="11",
                      tur="su", son_endeks=1450.5, onceki_endeks=1400.2, birim_fiyat=12.50,
                      tarih=datetime(2025, 6, 1)))

        db.add(Kargo(site_id=site.id, takip_no="PTT-123456", daire_id=daireler_list[0].id, blok_id=blok.id,
                      sakin_ad="Ali Yildiz", tel="555-0101"))

        db.add(Ziyaretci(site_id=site.id, ad="Veli Misafir", daire_id=daireler_list[0].id, blok_id=blok.id,
                          giris=datetime(2025, 6, 10, 14, 30), plaka="34 XYZ 789"))

        # ── Event / Ticketing ──
        venue = Venue(name="Hali Saha Acik Hava", city="Istanbul", district="Kadikoy",
                       address="Kadikoy Merkez", capacity=5000, venue_type="acik")
        db.add(venue)
        venue2 = Venue(name="Buyuk Sinema Salonu", city="Istanbul", district="Besiktas",
                        address="Besiktas Kültür Merkezi", capacity=200)
        db.add(venue2)
        await db.flush()

        db.add(VenueSection(venue_id=venue.id, name="VIP", capacity=100, price_multiplier=3.0))
        db.add(VenueSection(venue_id=venue.id, name="Tribün", capacity=4900, price_multiplier=1.0))
        db.add(VenueSection(venue_id=venue2.id, name="Salon", capacity=200, price_multiplier=1.0))
        await db.flush()

        event = Event(title="Fenerbahce vs Galatasaray", category="futbol", venue_id=venue.id,
                       organizer="Futbol Federasyonu", status="published")
        db.add(event)
        event2 = Event(title="Yeni Film: Kayip Sehir", category="sinema", venue_id=venue2.id,
                        organizer="Film Yapim", status="published")
        db.add(event2)
        await db.flush()

        sess = EventSession(event_id=event.id, start_time=datetime(2025, 7, 15, 20, 0),
                             end_time=datetime(2025, 7, 15, 22, 0))
        db.add(sess)
        sess2 = EventSession(event_id=event2.id, start_time=datetime(2025, 6, 20, 15, 30),
                              end_time=datetime(2025, 6, 20, 17, 30))
        db.add(sess2)

        # ── Vehicle Catalog ──
        categories = [
            VehicleCategory(name="Otomobil", slug="otomobil", sort_order=1),
            VehicleCategory(name="SUV", slug="suv", sort_order=2),
            VehicleCategory(name="Ticari", slug="ticari", sort_order=3),
            VehicleCategory(name="Motosiklet", slug="motosiklet", sort_order=4),
        ]
        db.add_all(categories)
        await db.flush()

        segments = [
            VehicleSegment(code="A", name="Mini", description="Mini sınıf (city cars)"),
            VehicleSegment(code="B", name="Küçük", description="Küçük sınıf (supermini)"),
            VehicleSegment(code="C", name="Orta", description="Orta sınıf (compact)"),
            VehicleSegment(code="D", name="Üst Orta", description="Üst orta sınıf"),
            VehicleSegment(code="E", name="Lüks", description="Lüks sınıf (executive)"),
            VehicleSegment(code="F", name="Süper Lüks", description="Süper lüks sınıf (premium luxury)"),
            VehicleSegment(code="J", name="Arazi/SUV", description="Arazi araçları ve SUV'lar"),
            VehicleSegment(code="S", name="Spor", description="Spor otomobiller"),
            VehicleSegment(code="M", name="Çok Amaçlı", description="MPV ve multi-purpose araçlar"),
        ]
        db.add_all(segments)
        await db.flush()

        body_types = [
            BodyType(name="Sedan", slug="sedan"),
            BodyType(name="Hatchback", slug="hatchback"),
            BodyType(name="SUV", slug="suv"),
            BodyType(name="Station Wagon", slug="station-wagon"),
            BodyType(name="Coupe", slug="coupe"),
            BodyType(name="Cabrio", slug="cabrio"),
            BodyType(name="MPV", slug="mpv"),
        ]
        db.add_all(body_types)
        await db.flush()

        feature_groups = [
            FeatureGroup(name="Güvenlik", slug="guvenlik", sort_order=1),
            FeatureGroup(name="Konfor", slug="konfor", sort_order=2),
            FeatureGroup(name="Multimedya", slug="multimedya", sort_order=3),
            FeatureGroup(name="Sürüş Destek", slug="surus-destek", sort_order=4),
        ]
        db.add_all(feature_groups)
        await db.flush()

        features = [
            Feature(group_id=feature_groups[0].id, name="ABS", slug="abs"),
            Feature(group_id=feature_groups[0].id, name="ESP", slug="esp"),
            Feature(group_id=feature_groups[1].id, name="Klima", slug="klima"),
            Feature(group_id=feature_groups[1].id, name="Deri Koltuk", slug="deri-koltuk"),
            Feature(group_id=feature_groups[2].id, name="Navigasyon", slug="navigasyon"),
            Feature(group_id=feature_groups[0].id, name="Park Sensörü", slug="park-sensoru"),
            Feature(group_id=feature_groups[0].id, name="Geri Görüş Kamerası", slug="geri-gorus-kamerasi"),
            Feature(group_id=feature_groups[2].id, name="Bluetooth", slug="bluetooth"),
            Feature(group_id=feature_groups[3].id, name="Hız Sabitleyici", slug="hiz-sabitleyici"),
        ]
        db.add_all(features)
        await db.flush()

        brands = [
            VehicleBrand(name="BMW", slug="bmw", country="Almanya"),
            VehicleBrand(name="Mercedes", slug="mercedes", country="Almanya"),
            VehicleBrand(name="Volkswagen", slug="volkswagen", country="Almanya"),
            VehicleBrand(name="Ford", slug="ford", country="ABD"),
            VehicleBrand(name="Toyota", slug="toyota", country="Japonya"),
            VehicleBrand(name="Honda", slug="honda", country="Japonya"),
            VehicleBrand(name="Hyundai", slug="hyundai", country="Güney Kore"),
            VehicleBrand(name="Renault", slug="renault", country="Fransa"),
            VehicleBrand(name="Fiat", slug="fiat", country="İtalya"),
            VehicleBrand(name="Audi", slug="audi", country="Almanya"),
        ]
        db.add_all(brands)
        await db.flush()

        models_data = [
            (0, "3 Serisi", "D", 2018), (0, "5 Serisi", "E", 2017), (0, "X5", "J", 2019),
            (1, "C Serisi", "D", 2014), (1, "E Serisi", "E", 2016), (1, "GLC", "J", 2015),
            (2, "Golf", "C", 1974), (2, "Passat", "D", 1973), (2, "Tiguan", "J", 2007),
            (3, "Focus", "C", 1998), (3, "Mustang", "S", 1964),
            (4, "Corolla", "C", 1966), (4, "RAV4", "J", 1994),
            (5, "Civic", "C", 1972), (5, "CR-V", "J", 1995),
            (6, "i20", "B", 2008), (6, "Tucson", "J", 2004),
            (7, "Clio", "B", 1990), (7, "Megane", "C", 1995),
            (8, "Egea", "C", 2015), (8, "Doblo", "M", 2000),
            (9, "A3", "C", 1996), (9, "A4", "D", 1994), (9, "Q5", "J", 2008),
        ]
        models_list = []
        for brand_ix, name, segment_code, prod_start in models_data:
            m = VehicleModel(brand_id=brands[brand_ix].id, name=name, segment_code=segment_code, production_start=prod_start)
            db.add(m)
            models_list.append(m)
        await db.flush()

        body_map = {b.slug: b for b in body_types}
        cat_map = {c.slug: c for c in categories}

        body_assignments = [
            (0, ["sedan", "station-wagon"]), (1, ["sedan", "station-wagon"]), (2, ["suv"]),
            (3, ["sedan", "station-wagon"]), (4, ["sedan", "station-wagon"]), (5, ["suv"]),
            (6, ["hatchback"]), (7, ["sedan", "station-wagon"]), (8, ["suv"]),
            (9, ["hatchback", "sedan", "station-wagon"]), (10, ["coupe", "cabrio"]),
            (11, ["sedan", "hatchback"]), (12, ["suv"]),
            (13, ["sedan", "hatchback"]), (14, ["suv"]),
            (15, ["hatchback"]), (16, ["suv"]),
            (17, ["hatchback"]), (18, ["hatchback", "sedan", "station-wagon"]),
            (19, ["sedan", "hatchback", "station-wagon"]), (20, ["mpv"]),
            (21, ["hatchback", "sedan"]), (22, ["sedan", "station-wagon"]), (23, ["suv"]),
        ]
        cat_assignments = [
            (0, ["otomobil"]), (1, ["otomobil"]), (2, ["suv"]),
            (3, ["otomobil"]), (4, ["otomobil"]), (5, ["suv"]),
            (6, ["otomobil"]), (7, ["otomobil"]), (8, ["suv"]),
            (9, ["otomobil"]), (10, ["otomobil"]),
            (11, ["otomobil"]), (12, ["suv"]),
            (13, ["otomobil"]), (14, ["suv"]),
            (15, ["otomobil"]), (16, ["suv"]),
            (17, ["otomobil"]), (18, ["otomobil"]),
            (19, ["otomobil"]), (20, ["ticari"]),
            (21, ["otomobil"]), (22, ["otomobil"]), (23, ["suv"]),
        ]
        for i, slug_list in body_assignments:
            for slug in slug_list:
                db.add(VehicleModelBodyType(model_id=models_list[i].id, body_type_id=body_map[slug].id))
        for i, cat_slugs in cat_assignments:
            for slug in cat_slugs:
                db.add(VehicleCategoryModel(category_id=cat_map[slug].id, model_id=models_list[i].id))

        for m in models_list:
            db.add(VehicleModelYear(model_id=m.id, year=2024, trim_name="Benzinli", engine_volume=1.6, horsepower=130, fuel_type="Benzin", transmission="Manuel"))
            db.add(VehicleModelYear(model_id=m.id, year=2025, trim_name="Dizel", engine_volume=2.0, horsepower=150, fuel_type="Dizel", transmission="Otomatik"))

        # ── Expert Inspection ──
        expert_company = ExpertCompany(
            name="Ekspertiz Merkezi A.Ş.",
            phone="0850-555-0101",
            email="info@ekspertizmerkezi.com",
            address="Kısıklı Mah. Teknoloji Cad. No:5, Üsküdar/İstanbul",
            tax_no="1234567890",
            tax_office="Üsküdar VD",
        )
        db.add(expert_company)
        await db.flush()

        packages = [
            ExpertPackage(
                name="Temel", price=500.0,
                description="Temel ekspertiz paketi - temel kontroller ve raporlama",
                checks_included="Kaporta kontrolü, iç mekan kontrolü, lastik kontrolü, sıvı seviyeleri",
            ),
            ExpertPackage(
                name="Premium", price=1000.0,
                description="Premium ekspertiz paketi - detaylı kontroller ve testler",
                checks_included="Temel kontroller + mekanik kontrol, test sürüşü, tramer kaydı, egzoz emisyon testi",
            ),
            ExpertPackage(
                name="VIP", price=2000.0,
                description="VIP ekspertiz paketi - en kapsamlı ekspertiz hizmeti",
                checks_included="Premium kontroller + şase kontrolü, dört çeker kontrolü, dinamometre testi, kayış kontrolü, ek donanım kontrolü",
            ),
        ]
        db.add_all(packages)

        # ── Food Suppliers ──
        from src.modules.food_supplier.models import FoodSupplier, FoodSupplierProduct
        supplier_user = User(
            email="tedarikci@test.com", phone="555-5000",
            password_hash=hash_password("123123"),
            full_name="Ege Ciftligi", role="seller",
        )
        db.add(supplier_user)
        await db.flush()

        supplier1 = FoodSupplier(
            user_id=supplier_user.id, company_name="Ege Organik Ciftlik",
            slug="ege-organik-ciftlik", description="Ege bolgesinden organik meyve sebze",
            supplier_type="producer", city="Izmir", district="Selcuk",
            contact_phone="555-5001", is_organic_certified=True,
            product_categories="meyve,sebze,zeytinyagi",
            verification_status="verified", is_active=True,
        )
        db.add(supplier1)
        await db.flush()

        home_chef_user = User(
            email="evinmutfagi@test.com", phone="555-6000",
            password_hash=hash_password("123123"),
            full_name="Ayse Teyze", role="seller",
        )
        db.add(home_chef_user)
        await db.flush()

        supplier2 = FoodSupplier(
            user_id=home_chef_user.id, company_name="Ayse Teyze'nin Mutfagi",
            slug="ayse-teyzenin-mutfagi",
            description="Geleneksel ev yemekleri, borekler ve tatlilar",
            supplier_type="home_chef", city="Ankara", district="Cankaya",
            address="Karanfil Sokak No:15, Cankaya/Ankara",
            contact_phone="555-6001",
            kitchen_photos="https://cdn.example.com/ayse-mutfak1.jpg,https://cdn.example.com/ayse-mutfak2.jpg",
            product_categories="ev yemekleri,ev borekleri,ev tatlilari",
            verification_status="verified", is_active=True,
        )
        db.add(supplier2)
        await db.flush()

        supplier_products = [
            FoodSupplierProduct(supplier_id=supplier1.id, name="Organik Domates", category="sebze", unit="kg", price_per_unit=25.0, is_organic=True),
            FoodSupplierProduct(supplier_id=supplier1.id, name="Salkim Domates", category="sebze", unit="kg", price_per_unit=30.0, is_organic=True),
            FoodSupplierProduct(supplier_id=supplier1.id, name="Naturel Zeytinyagi", category="zeytinyagi", unit="litre", price_per_unit=180.0, is_organic=True),
            FoodSupplierProduct(supplier_id=supplier2.id, name="Ev Boregi", category="ev borekleri", unit="porsiyon", price_per_unit=55.0),
            FoodSupplierProduct(supplier_id=supplier2.id, name="Islak Kek", category="ev tatlilari", unit="porsiyon", price_per_unit=35.0),
            FoodSupplierProduct(supplier_id=supplier2.id, name="Taze Ekmek", category="ev ekmekleri", unit="adet", price_per_unit=20.0),
        ]
        db.add_all(supplier_products)

        # --- Flower (Cicek) System Seed ---
        from src.modules.cicek.models import FloristProfile, FlowerProduct

        florist_user_id = seller_user.id
        florist_profile = FloristProfile(
            user_id=florist_user_id, shop_name="Ahmet'in Cicek Evi", slug="ahmetin-cicek-evi",
            description="Taze cicekler, hizli teslimat",
            city="Istanbul", district="Kadikoy",
            address="Caferaga Mah. Sakiz Sok. No:12",
            latitude=40.9900, longitude=29.0270,
            preparation_time_min=30, delivery_radius_km=5.0,
            min_order_amount=50, delivery_fee=24.90,
            free_delivery_min_amount=120, verification_status="verified",
            is_open=True, is_active=True,
        )
        db.add(florist_profile)
        await db.flush()

        flower_products = [
            FlowerProduct(seller_type="florist", seller_id=florist_profile.id, name="Kırmızı Gül Buketi", category="buket", subcategory="buket", occasion="sevgililer", price=250, stock=30, flowers_json='[{"name":"Gul","color":"Kirmizi","count":12}]', meaning="Ask ve tutku", season="Yil boyu", lifespan_days=7, care_level="Orta", is_express_eligible=True),
            FlowerProduct(seller_type="florist", seller_id=florist_profile.id, name="Beyaz Zambak", category="cicek", subcategory="cicek", occasion="taziye", price=180, stock=20, flowers_json='[{"name":"Zambak","color":"Beyaz","count":7}]', meaning="Masumiyet, saygi", season="Ilkbahar", lifespan_days=10, care_level="Kolay"),
            FlowerProduct(seller_type="florist", seller_id=florist_profile.id, name="Papatya Buketi", category="buket", subcategory="buket", occasion="dogum-gunu", price=120, stock=40, flowers_json='[{"name":"Papatya","color":"Beyaz","count":20}]', meaning="Mutluluk, neşe", season="Yil boyu", lifespan_days=7, care_level="Kolay"),
            FlowerProduct(seller_type="florist", seller_id=florist_profile.id, name="Orkide", category="saksi", subcategory="saksi", occasion="hediye", price=350, stock=10, flowers_json='[{"name":"Orkide","color":"Mor","count":1}]', meaning="Zarafet, asalet", season="Yil boyu", lifespan_days=45, care_level="Orta"),
            FlowerProduct(seller_type="florist", seller_id=florist_profile.id, name="Gül + Papatya Karışım", category="buket", subcategory="buket", occasion="sevgililer", price=200, stock=15, flowers_json='[{"name":"Gul","color":"Kirmizi","count":6},{"name":"Papatya","color":"Beyaz","count":10}]', meaning="Sevgi ve mutluluk", season="Yil boyu", lifespan_days=7, care_level="Kolay", is_express_eligible=True),
            FlowerProduct(seller_type="florist", seller_id=florist_profile.id, name="Lavanta Buketi", category="buket", subcategory="buket", occasion="hediye", price=90, stock=25, flowers_json='[{"name":"Lavanta","color":"Mor","count":15}]', meaning="Huzur", season="Yaz", lifespan_days=14, care_level="Kolay"),
        ]
        db.add_all(flower_products)

        # --- Vehicle Listing Seed ---
        from src.modules.vehicle.models import VehicleListing, VehicleGalleryCompany

        v_listing = VehicleListing(
            user_id=customer_user.id, title="2020 BMW 320d M Sport",
            year=2020, price=850000, brand_id=1, model_id=1,
            fuel_type="dizel", transmission="otomatik", mileage=85000,
            color="Beyaz", city="Istanbul", condition="ikinci_el",
            status="active", is_active=True,
        )
        db.add(v_listing)

        v_gallery = VehicleGalleryCompany(
            user_id=seller_user.id, company_name="Istanbul Oto Galeri",
            slug="istanbul-oto-galeri", city="Istanbul",
            phone="02121234567", is_active=True,
        )
        db.add(v_gallery)

        # --- Kargo Firmaları ---
        from src.modules.cargo.models import CargoCompany, CargoBranch, CargoPricingTier, CargoServiceArea

        cargo_users = []
        for i, (name, slug, city) in enumerate([
            ("Yurtiçi Kargo", "yurtici-kargo", "Istanbul"),
            ("Aras Kargo", "aras-kargo", "Istanbul"),
            ("MNG Kargo", "mng-kargo", "Ankara"),
            ("PTT Kargo", "ptt-kargo", "Ankara"),
            ("Sürat Kargo", "surat-kargo", "Izmir"),
            ("FedEx Türkiye", "fedex-turkiye", "Istanbul"),
            ("UPS Türkiye", "ups-turkiye", "Istanbul"),
        ]):
            cu = User(email=f"cargo{i+1}@test.com", password=hashed, full_name=f"{name} Admin", role="seller", is_active=True)
            db.add(cu)
            await db.flush()
            cargo_users.append(cu)
            comp = CargoCompany(
                user_id=cu.id, company_name=name, slug=slug, city=city,
                phone=f"0212{1000000+i*1000}", email=f"info@{slug}.com",
                api_key=f"api_key_{slug}", is_verified=True,
                verification_status="verified", is_active=True,
            )
            db.add(comp)
            await db.flush()
            branch = CargoBranch(
                company_id=comp.id, branch_name=f"{name} Merkez Şube",
                branch_code=f"BR{i+1:03d}", city=city, district="Merkez",
                address=f"{city} Merkez Şube Adresi", is_main_branch=True,
            )
            db.add(branch)
            await db.flush()
            pricing = CargoPricingTier(
                company_id=comp.id, tier_name="Standart",
                min_weight_kg=0, max_weight_kg=30,
                min_volume_dm3=0, max_volume_dm3=100,
                zone_type="sehirler_arasi", base_price=49.90,
                price_per_kg=2.50, price_per_dm3=0.50,
            )
            db.add(pricing)
            area = CargoServiceArea(
                company_id=comp.id, city=city, is_available=True,
                delivery_time_hours=24, pickup_available=True,
            )
            db.add(area)

        await db.commit()
        print("Seed complete!")
        print(f"  Seller: {seller_user.email} / 123123")
        print(f"  Customer: {customer_user.email} / 123123")
        print(f"  Courier: {courier_user.email} / 123123")
        print(f"  Admin: {admin_user.email} / 123123")
        print(f"  Food Seller: {food_seller.email} / 123")
        print(f"  Supplier: {supplier_user.email} / 123123")
        print(f"  Home Chef: {home_chef_user.email} / 123123")
        print(f"  Florist: {seller_user.email} / 123123")
        print(f"  Vehicle Listing: 2020 BMW 320d M Sport (850,000 TL)")


if __name__ == "__main__":
    asyncio.run(seed())
