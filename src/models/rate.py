"""Модель таблицы rate"""
from sqlalchemy import Column, ForeignKey, Integer, Table, CheckConstraint, UniqueConstraint

from .metadata import METADATA
from .metric import metric

rate = Table(
    'rate',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('metric', Integer, ForeignKey(metric.c.id, ondelete='CASCADE')),
    Column('person', Integer, nullable=False),
    Column('value', Integer, nullable=False),
    CheckConstraint('value between 0 and 100'),
    UniqueConstraint('metric', 'person'),
)
