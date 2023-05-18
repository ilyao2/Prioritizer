"""Модель таблицы metric"""
from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String, Table

from .idea import idea
from .metadata import METADATA

metric = Table(
    'metric',
    METADATA,
    Column('id', Integer, primary_key=True),
    Column('title', String, nullable=False),
    Column('idea', Integer, ForeignKey(idea.c.id, ondelete='CASCADE'), nullable=False),
    Column('type', ARRAY(String), nullable=True)
)
