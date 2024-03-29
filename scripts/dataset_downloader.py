#!/usr/bin/env python3

# /* +--------------------------------------------------+ */
# /* |      UPA Projekt - Kurzy devízového trhu         | */
# /* |              dataset_downloader.py               | */
# /* |   (c) copyright xersek00 [Martin Eršek]    2020  | */
# /* |   (c) copyright xkarab03 [Jozef Karabelly] 2020  | */
# /* +--------------------------------------------------+ */

import argparse
import pandas as pd
import requests
import sys

from datetime import datetime, date
from io import StringIO
from cassandra_storage import CassandraStorage
from postgresql_storage import PostgresStorage

bank_url = 'https://www.cnb.cz/'
bank_api_endpoint = 'cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt?date='

def get_values_for_date(timestamp):
	date = timestamp.date().strftime("%d.%m.%Y")
	response = requests.get(bank_url + bank_api_endpoint + date)

	if response.status_code != 200:
		print("API request failed, return code %d" % response.status_code)
		sys.exit(1)

	r = response.text
	r_lines = r.splitlines()

	# check if first line returned from API has correct date
	# when requested date is bad (weekend day or if date belongs to holiday days)
	# API will return nearest working day data
	if date != r_lines[0].split(' ')[0]:
		print("Data returned from API has incorrect date")
		print("Required date %s, API response date %s" % (date, r_lines[0].split(' ')[0]))
		print("Skipping this date")
		return None

	result = pd.read_csv(StringIO(r), sep='|', skiprows=[0])
	result = result.assign(timestamp=timestamp).set_index('timestamp')
	result['kurz'] = result['kurz'].str.replace(',', '.').astype(float)
	return result


def get_values_for_time_period(start_date, end_date=None):
	start_date = start_date.date()

	if end_date is None:
		end_date = date.today()
	# else:
		# end_date = datetime.strptime(end_date, "%d.%m.%Y").date()

	if end_date < start_date:
		print("Start date shouldn't be in future!")
		sys.exit(1)

	date_range = pd.bdate_range(start=start_date, end=end_date)	

	if date_range.empty:
		print("There isn't enough business days between start date and end_date!")
		sys.exit(1)

	result = pd.DataFrame()

	for timestamp in date_range:
		values = get_values_for_date(timestamp)
		if values is not None:
			result = pd.concat([result, values])
	return result

def extract_and_transform(start_date, end_date=None):
	extracted_data = get_values_for_time_period(start_date=start_date, end_date=end_date)
	
	cassandra_storage = CassandraStorage()
	cassandra_storage.import_dataframe(extracted_data)

	# start_date = datetime.strptime(start_date, "%d.%m.%Y").date()
	# if end_date is not None:
		# end_date = datetime.strptime(end_date, "%d.%m.%Y").date()

	qs = cassandra_storage.filter_by_date_range(start_date, end_date)

	postgres_storage = PostgresStorage()
	postgres_storage.import_cassandra_records(qs.all())


def valid_date(s):
    try:
        return datetime.strptime(s, "%d.%m.%Y")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Dataset Downloader')
	
	parser.add_argument('--start_date', action='store', type=valid_date, required=True, help='Dataset start date in format: "%d.%m.%Y"')
	parser.add_argument('--end_date', action='store', type=valid_date, help='Dataset end date in format: "%d.%m.%Y"')

	args = parser.parse_args()
	extract_and_transform(start_date=args.start_date, end_date=args.end_date)