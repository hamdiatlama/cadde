import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./web_platform.db")
IS_SQLITE = DATABASE_URL.startswith("sqlite")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
NATS_URL = os.getenv("NATS_URL", "nats://localhost:4222")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "webplatform")
MEILISEARCH_URL = os.getenv("MEILISEARCH_URL", "http://localhost:7700")
MEILISEARCH_API_KEY = os.getenv("MEILISEARCH_API_KEY", "master-key")
OSRM_URL = os.getenv("OSRM_URL", "http://localhost:5000")
FCM_CREDENTIALS_PATH = os.getenv("FCM_CREDENTIALS_PATH", "./firebase-credentials.json")
