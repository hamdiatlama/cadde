from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base


class ProductQuestion(Base):
    __tablename__ = "product_questions"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ProductAnswer(Base):
    __tablename__ = "product_answers"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("product_questions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ProductBundle(Base):
    __tablename__ = "product_bundles"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(200))
    total_price = Column(Float)
    discount_rate = Column(Float, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BundleItem(Base):
    __tablename__ = "bundle_items"
    id = Column(Integer, primary_key=True, index=True)
    bundle_id = Column(Integer, ForeignKey("product_bundles.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)


class GiftRegistry(Base):
    __tablename__ = "gift_registries"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String(20))
    title = Column(String(200))
    event_date = Column(DateTime(timezone=True))
    is_public = Column(Boolean, default=True)
    share_code = Column(String(20), unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class GiftRegistryItem(Base):
    __tablename__ = "gift_registry_items"
    id = Column(Integer, primary_key=True, index=True)
    registry_id = Column(Integer, ForeignKey("gift_registries.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    purchased_quantity = Column(Integer, default=0)


class ProductBarcode(Base):
    __tablename__ = "product_barcodes"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    barcode = Column(String(100), unique=True, nullable=False)
    type = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ProductExpiryBatch(Base):
    __tablename__ = "product_expiry_batches"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    batch_no = Column(String(100))
    lot_no = Column(String(100))
    quantity = Column(Integer, default=0)
    expiry_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
