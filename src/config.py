"""Конфигурационные переменные"""
import os


DB_USER = os.environ.get('DB_USER') or 'postgres'
DB_PASS = os.environ.get('DB_PASS') or 'postgres'
DB_HOST = os.environ.get('DB_HOST') or '0.0.0.0'
DB_PORT = os.environ.get('DB_PORT') or '5432'
DB_NAME = os.environ.get('DB_NAME') or 'main_data'

validate_not_none = {
    'DB_USER': DB_USER,
    'DB_PASS': DB_PASS,
    'DB_HOST': DB_HOST,
    'DB_PORT': DB_PORT,
    'DB_NAME': DB_NAME,
}
for name, var in validate_not_none.items():
    if var is None:
        raise NotImplementedError(name)
