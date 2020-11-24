from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import connection
from cassandra.cluster import Cluster
from models import Ticker
from dataset_downloader import get_values_for_time_period

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

    def import_dataframe(self, df):
        for index, values in df.iterrows():
            Ticker.create(name=values['kód'], time=index.date(), quantity=values['množství'], country=values['země'], value=values['kurz'])