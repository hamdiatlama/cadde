from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base

class MapPolicy(Base):
    __tablename__ = "map_policies"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    min_advertised_price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class MapViolation(Base):
    __tablename__ = "map_violations"
    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("map_policies.id"), nullable=False)
    reported_price = Column(Float, nullable=False)
    reported_by = Column(Integer, ForeignKey("users.id"))
    status = Column(String(20), default="pending")
    resolved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CounterfeitReport(Base):
    __tablename__ = "counterfeit_reports"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    reported_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(Text)
    evidence_url = Column(String(500))
    status = Column(String(20), default="pending")
    resolved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ProductCompliance(Base):
    __tablename__ = "product_compliance"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    cert_type = Column(String(100))
    cert_number = Column(String(100))
    cert_file_url = Column(String(500))
    issued_at = Column(DateTime(timezone=True))
    expires_at = Column(DateTime(timezone=True))
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ProductRecall(Base):
    __tablename__ = "product_recalls"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    reason = Column(Text, nullable=False)
    risk_level = Column(String(20))
    affected_batch = Column(String(100))
    action_taken = Column(String(500))
    status = Column(String(20), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PolicyViolation(Base):
    __tablename__ = "policy_violations"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    violation_type = Column(String(100))
    description = Column(Text)
    evidence = Column(String(500))
    penalty = Column(String(100))
    status = Column(String(20), default="pending")
    resolved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
