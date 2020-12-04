#!/usr/bin/env python3

# /* +--------------------------------------------------+ */
# /* |      UPA Projekt - Kurzy devízového trhu         | */
# /* |              postgresql_storage.py               | */
# /* |   (c) copyright xersek00 [Martin Eršek]    2020  | */
# /* |   (c) copyright xkarab03 [Jozef Karabelly] 2020  | */
# /* +--------------------------------------------------+ */

import logging
from models import Base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

def get_database():
    try:
        engine = get_engine(name='', user='postgres', password='')
        logger.info('Connected to PostgreSQL databse!')
    except IOError:
        log.exception("Failed to get database connection!")
        return None
    return engine

def get_engine(name, user, password, host='localhost', port='5432'):
    DATABASE_URL = f'postgresql://{user}:{password}@{host}:{port}/{name}'
    engine = create_engine(DATABASE_URL, pool_size=50, echo=True)
    return engine

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class PostgresStorage(metaclass=Singleton):
    def __init__(self):
        self.db = get_database()

        Session = sessionmaker(bind=self.db)
        self.meta = MetaData(bind=self.db)
        self.session = Session()

    def sync_tables(self):
        Base.metadata.create_all(self.db)
        logger.info('PostgreSQL tables synced.')
    