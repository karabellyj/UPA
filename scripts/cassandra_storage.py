#!/usr/bin/env python3

# /* +--------------------------------------------------+ */
# /* |      UPA Projekt - Kurzy devízového trhu         | */
# /* |               cassandra_storage.py               | */
# /* |   (c) copyright xersek00 [Martin Eršek]    2020  | */
# /* |   (c) copyright xkarab03 [Jozef Karabelly] 2020  | */
# /* +--------------------------------------------------+ */

import logging
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import connection
from cassandra.cluster import Cluster
from models import Ticker

logger = logging.getLogger(__name__)

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class CassandraStorage(metaclass=Singleton):
    def  __init__(self):
        self.cluster = Cluster()
        self.session = self.cluster.connect('upa')
        connection.set_session(self.session)

    def sync_tables(self):
        sync_table(Ticker)
        logger.info('Cassandra tables synced.')

    def import_dataframe(self, df):
        for index, values in df.iterrows():
            Ticker.create(name=values['kód'], time=index.date(), quantity=values['množství'], country=values['země'], value=values['kurz'])
    
    def filter_by_date_range(self, from_date, to_date=None):
        q = Ticker.objects.filter(name='*', time__gte=from_date)
        if to_date:
            q.filter(time_lte=to_date)
        return q