from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class OrderModel(Base):
    __tablename__ = 'orders'

    order_id = Column(String(45), primary_key=True)
    user_id = Column(String(45), nullable=False)
    date = Column(DateTime(timezone=True), default=func.now())
    total_amount = Column(Float, nullable=False)
