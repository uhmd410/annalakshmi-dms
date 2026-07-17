from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Annalakshmi(Base):
    __tablename__ = "annalakshmis"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(150), nullable=False)
    mobile_number = Column(String(15), nullable=False, unique=True, index=True)
    email = Column(String(150), nullable=True)
    address = Column(String(300), nullable=False)
    area = Column(String(100), nullable=False, index=True)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    pin_code = Column(String(10), nullable=False)
    cuisine_specialization = Column(String(150), nullable=False)
    veg_or_nonveg = Column(String(10), nullable=False)
    signature_dishes = Column(String(500), nullable=True)
    available_timings = Column(String(200), nullable=True)
    max_orders_per_day = Column(Integer, nullable=False, default=10)
    date_joined = Column(Date, nullable=False)
    status = Column(String(10), nullable=False, default="active", index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
