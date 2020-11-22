from io import StringIO
import pandas as pd
import datetime
import requests
import sys

bank_url = 'https://www.cnb.cz/'
bank_api_endpoint = 'cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/denni_kurz.txt?date='

def get_next_day(date):
	return date + datetime.timedelta(days=1)

def check_whether_date_is_weekend(date):
	return date.weekday() > 4

def get_values_for_date(date):

	if check_whether_date_is_weekend(datetime.datetime.strptime(date, "%d.%m.%Y")):
		print("Bank API doesn't support weekend dates")
		sys.exit(1)

	response = requests.get(bank_url + bank_api_endpoint + date)

	if response.status_code != 200:
		print("API request failed, return code %d"%response.status_code)
		sys.exit(1)

	r = response.text
	r_lines = r.splitlines()

	#check if first line returned from API has correct date
	#this happens when weekend days are requested or if date belongs to holiday days
	if date != r_lines[0].split(' ')[0]:
		print("Data returned from API has incorrect date")
		print("Required date %s, API response date %s" % (date, r_lines[0].split(' ')[0]))
		print("Skipping this date")
		return None

	resultx = '\n'.join(r_lines[1:])
	result = pd.read_csv(StringIO(resultx), sep='|')

	return result


def get_values_for_time_period(start_date, num_of_days):
	
	if num_of_days < 1:
		print("Num of days has to be greater than zero!")
		sys.exit(1)

	start_date = datetime.datetime.strptime(start_date, "%d.%m.%Y").date()

	if datetime.date.today() < start_date:
		print("Start date shouldn't be in future!")
		sys.exit(1)

	tmp_date = start_date
	dates = []

	for _ in range(num_of_days):

		if tmp_date > datetime.date.today(): break

		while check_whether_date_is_weekend(tmp_date):
			tmp_date = get_next_day(tmp_date)

		dates.append(tmp_date)
		tmp_date = get_next_day(tmp_date)

	if len(dates) < num_of_days:
		print("There isn't enough weekdays between start_date and now!")
		sys.exit(1)

	result = {}

	for d in dates:
		date_string = d.strftime("%d.%m.%Y")
		r = get_values_for_date(date_string)
		result[date_string] = r

	return result

print(get_values_for_time_period("16.11.2020", 5))

#TODO pass data to cassana DB

