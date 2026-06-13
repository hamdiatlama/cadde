"""Seed database with sample data for all domains."""
import asyncio, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./web_platform.db")

from src.database import init_db, async_session
from src.core.auth import hash_password


async def seed():
    await init_db()
    async with async_session() as db:
        from src.modules.user.models import User
        from src.modules.seller.models import Seller, Question
        from src.modules.store.models import Product
        from src.modules.courier.models import Courier
        from src.modules.food.models import Restaurant, RestaurantBranch, FoodMenuItem
        from src.modules.ride.models import Driver

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

        await db.commit()
        print("Seed complete!")
        print(f"  Seller: {seller_user.email} / 123123")
        print(f"  Customer: {customer_user.email} / 123123")
        print(f"  Courier: {courier_user.email} / 123123")
        print(f"  Admin: {admin_user.email} / 123123")
        print(f"  Food Seller: {food_seller.email} / 123")


if __name__ == "__main__":
    asyncio.run(seed())
