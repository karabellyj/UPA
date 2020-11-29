import logging
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)

def get_database():
    try:
        engine = get_engine(name='upa', user='upa', password='upa')
        logger.info('Connected to PostgreSQL databse!')
    except IOError:
        log.exception("Failed to get database connection!")
        return None
    return engine

def get_engine(name, user, password, host='localhost', port='5432'):
    DATABASE_URL = f'postgresql://{user}:{password}@{host}:{port}/{name}'
    engine = create_engine(DATABASE_URL, pool_size=50, echo=True)
    return engine