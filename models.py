from sqlalchemy import Column, Integer, Date, DateTime, ForeignKey, Float, String
from sqlalchemy.orm import relationship, declarative_base
from database import Backend

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transaction'
    
    id = Column(Integer, primary_key=True)
    business_day = Column(Date)
    timestamp = Column(DateTime)
    
    def __repr__(self):
        return 'Transaction <{}>'.format(self.id)

class Item(Base):
    __tablename__ = 'item'
    
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    name = Column(String)
    price = Column(Float)
    category = Column(String)
    total_quantity = Column(Integer)

    def __repr__(self):
        return 'Item <{}>'.format(self.id)

class BillItem(Base):
    __tablename__ = 'bill_item'

    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('transaction.id'))
    price = Column(Float)
    quantity = Column(Integer)
    item_code = Column(String, ForeignKey('item.code'))
    transaction = relationship('Transaction')
    item = relationship('Item')
    
    def __repr__(self):
        return 'BillItem <{}>'.format(self.id)    

def create_all(engine):
    metadata = Base.metadata
    metadata.create_all(engine)

def main():
    create_all(engine=Backend.instance().get_engine())

if __name__ == "__main__":
    main()
