DROP KEYSPACE IF EXISTS upa;

CREATE KEYSPACE upa WITH replication = {
  'class': 'SimpleStrategy',
  'replication_factor': 3
};

