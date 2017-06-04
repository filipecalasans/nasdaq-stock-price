import retreive_stock_list as datadir
from enum import Enum, unique

READ_PREFIX = datadir.PATH_TO_SAVE + datadir.PREFIX
FILES_PATH = [READ_PREFIX + filename for filename in datadir.FILE_TO_GET]

@unique
class FileIndex(Enum):
   SYMBOL = 0
   SECURITY_NAME = 1
   MARKET_CATEGORY = 2
   TEST_ISSUE = 3
   FINANCIAL_STATUS = 4
   ROUND_LOT_SIZE = 5
   ETF = 6
   NEXTSHARES = 8
   SIZE = 9
   
class StockInfo:

   def __init__(self, symbol='', security_name='', market_cat='', test_issue='', fin_stats='', lot_size=0, etf=False, nxtShares=''):
      self.symbol = symbol
      self.security_name = security_name
      self.market_category = market_cat
      self.test_issue = test_issue
      self.financial_status = fin_stats
      self.round_lot_size = lot_size
      self.etf=etf
      self.nextShares=nxtShares

   def __str__(self):
      return print("{}|{}|{}|{}|{}|{}|{}|{}".format(self.symbol, 
                                                    self.security_name, 
                                                    self.market_category, 
                                                    self.test_issue, 
                                                    self.financial_status.
                                                    self.round_lot_size,
                                                    self.etf,
                                                    self.nextShares))

def parse_file(filename):
   f = open(filename, 'r')

   line = f.readline() # Discard First line (Header)
   stock_info = {}

   last_key_inserted = ''

   for line in f:
      line = line.replace("\n", "")
      values = line.split("|")
      last_key_inserted = values[FileIndex['SYMBOL'].value]

      stock = StockInfo(symbol=values[FileIndex['SYMBOL'].value], 
                        security_name=[FileIndex['SECURITY_NAME'].value], 
                        market_cat=[FileIndex['MARKET_CATEGORY'].value], 
                        test_issue=[FileIndex['TEST_ISSUE'].value], 
                        fin_stats=[FileIndex['FINANCIAL_STATUS'].value], 
                        lot_size=[FileIndex['ROUND_LOT_SIZE'].value], 
                        etf=[FileIndex['ETF'].value]=='Y', 
                        nxtShares=[FileIndex['NEXTSHARES'].value])
                     
      if len(stock.symbol):
         stock_info[stock.symbol] = stock
   
   del stock_info[last_key_inserted]
   return stock_info

if __name__ == "__main__":
   for file in FILES_PATH:
      stock_info = parse_file(file)
      print("===================================================")
      print("{}".format(file))
      print("===================================================")
      for stock in stock_info:
         print(stock)



   

