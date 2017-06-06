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
   
   data = [
      "stocks",
      "price",
      "priceopen",
      "high",
      "low",
      "volume",
      "datedelay",
      "change",
      "changepct",
      "closeyest",
      "shares",
   ]

   values = []
   
   for data_name in data:
      print("{} ======== ".format(data_name))
      array_data = [ data_name ]
      if data_name is "stocks":
         for stock in stock_values:
            array_data.append(stock)
      else:
         for stock in stock_values:
            array_data.append("=GoogleFinance(\"{}\";\"{}\")".format(stock, data_name))
   
      values.append(array_data)

   init_index = 1
   size = len(values[0])

   first_letter = ascii_uppercase[0]
   last_letter = ascii_uppercase[len(data)-1]

   range_name = '{}{}:{}{}'.format(first_letter, init_index, last_letter, size + init_index)
   value_input_option= "USER_ENTERED"

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



