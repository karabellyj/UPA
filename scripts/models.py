#!/usr/bin/env python3
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from sqlalchemy import Column, ForeignKey, String, \
                       Integer, Float, Date, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

class Ticker(Model):
    name = columns.Text(primary_key=True, max_length=5)
    time = columns.DateTime(primary_key=True, index=True)
    quantity = columns.Integer()
    country = columns.Text()
    value = columns.Float()

Base = declarative_base()

class Currency(Base):
    __tablename__ = 'currency'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column('code', String(5), nullable=False)
    country = Column('country', String(256), nullable=False)

class CurrencyPrice(Base):
    __tablename__ = 'currency_price'
    id = Column(Integer, primary_key=True)
    date = Column('date', Date, nullable=False)
    value = Column('value', Float)
    
    currency_id = Column(Integer, ForeignKey(
        'currency.id',
        onupdate='CASCADE',
        ondelete='CASCADE',
    ))

    UniqueConstraint('date', 'currency_id')
    currency = relationship('Currency')