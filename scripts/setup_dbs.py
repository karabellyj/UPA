#!/usr/bin/env python3
from postgresql_storage import PostgresStorage
from cassandra_storage import CassandraStorage

# Setup environment and create a session
if __name__ == "__main__":
    CassandraStorage().sync_tables()
    PostgresStorage().sync_tables()