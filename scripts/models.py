from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class Ticker(Model):
    name = columns.Text(primary_key=True, max_length=5)
    time = columns.DateTime(primary_key=True, index=True)
    quantity = columns.Integer()
    country = columns.Text()
    value = columns.Float()