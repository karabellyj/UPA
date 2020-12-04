#!/usr/bin/env python3

# /* +--------------------------------------------------+ */
# /* |      UPA Projekt - Kurzy devízového trhu         | */
# /* |                 setup_dbs.py                     | */
# /* |   (c) copyright xersek00 [Martin Eršek]    2020  | */
# /* |   (c) copyright xkarab03 [Jozef Karabelly] 2020  | */
# /* +--------------------------------------------------+ */

from postgresql_storage import PostgresStorage
from cassandra_storage import CassandraStorage

# Setup environment and create a session
if __name__ == "__main__":
    CassandraStorage().sync_tables()
    PostgresStorage().sync_tables()