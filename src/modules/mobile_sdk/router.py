from fastapi import APIRouter

router = APIRouter(prefix="/mobile-sdk", tags=["mobile_sdk"])

@router.get("/config")
async def get_sdk_config():
    return {
        "name": "WebPlatform Mobile SDK",
        "version": "1.0.0",
        "base_url": "/api/v1",
        "auth_method": "bearer_token",
        "features": [
            "products", "categories", "search", "cart", "orders",
            "wishlist", "auth", "push_notifications", "chat",
            "addresses", "payments", "reviews", "auctions",
            "gift_cards", "wallet", "loyalty", "live_shopping",
            "recommendations", "blog", "returns", "barcode_scanner",
            "pos", "qr_code"
        ],
        "endpoints": {
            "auth": "/auth/login",
            "products": "/search/products",
            "cart": "/cart",
            "orders": "/orders",
            "push_register": "/messaging/push/subscribe"
        }
    }

@router.get("/documentation")
async def get_documentation():
    return {
        "sdk_url": "https://github.com/webplatform/mobile-sdk",
        "docs_url": "/docs",
        "openapi_url": "/openapi.json",
        "platforms": ["ios", "android", "react-native", "flutter"],
        "quick_start": {
            "install": "npm install webplatform-sdk",
            "init": "import WebPlatform from 'webplatform-sdk'; const client = new WebPlatform({ apiKey: 'sk_...' });",
            "example": "const products = await client.products.search({ q: 'phone' });"
        }
    }
