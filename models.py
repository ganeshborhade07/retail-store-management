from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, Float, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transaction'
    
    id = Column(Integer, primary_key=True)
    busiuness_day = Column(Date)
    timestamp = Column(DateTime)
    

class Item(Base):
    __tablename__ = 'item'
    
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    name = Column(String)
    price = Column(Float)
    category = Column(String)
    starting_quantity = Column(Integer)


class BillItem(Base):
    __tablename__ = 'bill_item'

    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey("transaction.id"))
    price = Column(Float)
    quantity = Column(Integer)
    item_code = Column(String)
    
    transaction = relationship("Trassation")
    item = relationship("Item")
