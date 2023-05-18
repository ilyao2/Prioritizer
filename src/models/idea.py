"""Модель таблицы idea"""
from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text

from .metadata import METADATA

idea = Table(
    'idea',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('title', String, nullable=False),
    Column('description', Text, nullable=True),
    Column('author', Integer, nullable=True),
    Column('parent', Integer, ForeignKey('idea.id', ondelete='CASCADE')),
)
