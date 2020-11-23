from cassandra.cqlengine.management import sync_table
from cassandra.cluster import Cluster
from models import Ticker

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class CassandraStorage(metaclass=Singleton):
    def  __init__():
        self.cluster = Cluster()
        self.session = self.cluster.connect()
    
    @staticmethod
    def sync_tables():
        sync_table(Ticker)

    def import_dataframe(df):
        raise NotImplementedError