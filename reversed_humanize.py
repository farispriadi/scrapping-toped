from datetime import datetime, date ,timedelta
from dateutil.relativedelta import *


def humanize_to_date(humanize_str):

	humanize_str = humanize_str.lower()

	today = date.today()
	splited_str = humanize_str.split(" ")


	if 'minggu lalu' in humanize_str:
		result = today + relativedelta(weeks=-1*(int(splited_str[0])))
	elif 'bulan lalu' in humanize_str:
		result = today + relativedelta(months=-1*(int(splited_str[0])))
	elif 'tahun lalu' in humanize_str:
		result = today + relativedelta(years=-1*(int(splited_str[0])))
	elif 'hari lalu	' not in humanize_str:
		result = today + relativedelta(days=-1*(int(splited_str[0])))
	else:
		result = today
	
	return result.strftime("%d-%m-%Y")
