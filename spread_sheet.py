from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import todays_stocks_list as stock_list
from string import ascii_uppercase

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'credential-google.json'
APPLICATION_NAME = 'Google Sheets API - STOCK SPREAD SHEET'


def get_credentials():
   """Gets valid user credentials from storage.

   If nothing has been stored, or if the stored credentials are invalid,
   the OAuth2 flow is completed to obtain the new credentials.

   Returns:
      Credentials, the obtained credential.
   """
   home_dir = os.path.expanduser('../')
   credential_dir = os.path.join(home_dir, 'credentials')
   if not os.path.exists(credential_dir):
      os.makedirs(credential_dir)
   credential_path = os.path.join(credential_dir,
                                 'sheets.googleapis-credential.json')

   store = Storage(credential_path)
   credentials = store.get()
   if not credentials or credentials.invalid:
      flow = client.flow_from_clientsecrets('../credentials/' + CLIENT_SECRET_FILE, SCOPES)
      flow.user_agent = APPLICATION_NAME
      if flags:
         credentials = tools.run_flow(flow, store, flags)
      else: # Needed only for compatibility with Python 2.6
         credentials = tools.run(flow, store)
      print('Storing credentials to ' + credential_path)
   return credentials

def build_stock_spread_sheet():

	all_listed = stock_list.parse_file()

	"""Shows basic usage of the Sheets API.

	Creates a Sheets API service object and prints the names and majors of
	students in a sample spreadsheet:
	https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
	"""
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())

	discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
						'version=v4')

	service = discovery.build('sheets', 'v4', http=http,
									discoveryServiceUrl=discoveryUrl)

	spreadsheet_id = '1gG6PIAKMKA0lBGRj-5X9UBM6DiELpbqktThJM_sWM6Q'

	stock_values = all_listed.keys()

	major_dimension = "COLUMNS"

	# price: market price of the stock – delayed by up to 20 minutes.
	# priceopen: the opening price of the stock for the current day.
	# high: the highest price the stock traded for the current day.
	# low: the lowest price the stock traded for the current day.
	# volume: number of shares traded of this stock for the current day.
	# marketcap: the market cap of the stock.
	# tradetime: the last time the stock traded.
	# datadelay: the delay in the data presented for this stock using the googleFinance() function.
	# volumeavg: the average volume for this stock.
	# pe: the Price-to-Earnings ratio for this stock.
	# eps: the earnings-per-share for this stock.
	# high52: the 52-week high for this stock.
	# low52: the 52-week low for this stock.
	# change: the change in the price of this stock since yesterday’s market close.
	# beta: the beta value of this stock.
	# changepct: the percentage change in the price of this stock since yesterday’s close.
	# closeyest: yesterday’s closing price of this stock.
	# shares: the number of shares outstanding of this stock.
	# currency: the currency in which this stock is traded.

	data = [
		"stocks",
		"price",
		"priceopen",
		"high",
		"low",
		"volume",
		"marketcap",
		"tradetime",
		"datadelay",
		"volumeavg",
		"pe",
		"eps",
		"high52",
		"low52",
		"change",
		"beta",
		"changepct",
		"closeyest",
		"shares",
		"currency"
	]

	fold_size = 200
	current_index = 0
	init_index = 1

	while current_index < len(stock_values):
		
		print("Populating Fold #{}".format(current_index % fold_size))
		values = []
		
		for data_name in data:
			print("Building Column {} ======== ".format(data_name))
			array_data = [ data_name ]
			if (data_name is "stocks") and (current_index is not 0):
				row_index = 0
				for stock in stock_values:
					array_data.append(stock)
					row_index = row_index + 1
					if row_index is fold_size:
						break
			elif (data_name is not "stocks"):
				row_index = 0
				for stock in stock_values:
					array_data.append("=GoogleFinance(\"{}\";\"{}\")".format(stock, data_name))
					row_index = row_index + 1
					if row_index is fold_size:
						break
			else:
				continue
		
			values.append(array_data)
		
		
		size = len(values[0])
		current_index += size

		first_letter = ascii_uppercase[0]
		last_letter = ascii_uppercase[len(data)-1]

		range_name = '{}{}:{}{}'.format(first_letter, init_index, last_letter, init_index + size)
		value_input_option= "USER_ENTERED"

		init_index += size

		body = {
			"range": range_name,
			"majorDimension": major_dimension,
			"values": values
		}  

		# result = service.spreadsheets().values().batchUpdate(
		#    spreadsheetId=spreadsheetId, body=batch_update_values_request_body).execute()
		#  
		
		result = service.spreadsheets().values().update(
			spreadsheetId=spreadsheet_id, range=range_name,
			valueInputOption=value_input_option, body=body).execute()
			
		values = result.get('responses', [])

		# if not values:
		#    print('No data found.')
		# else:
		#    print(values)


if __name__ == '__main__':
   build_stock_spread_sheet()



