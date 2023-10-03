from .database import Base
from sqlalchemy import Column, Integer, DateTime, String, TEXT, func, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(100), nullable=False)
    cost_price = Column(TEXT, nullable=False)
    quantity = Column(Integer)  
    created_at = Column(DateTime(timezone = True), server_default= func.now())
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone = True), server_default= func.now())


class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    rater_id = Column(Integer, ForeignKey('users.id'), nullable= False)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable= False)
    rating = Column(Integer, nullable=False)
    message = Column(String(500))
    created_at = Column(DateTime(timezone = True), server_default= func.now())

    CheckConstraint('rating >= 1 AND rating <= 5')
    UniqueConstraint("col2", "col3", name="uix_1")
    
    