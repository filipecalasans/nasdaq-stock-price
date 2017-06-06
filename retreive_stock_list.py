from ftplib import FTP
from datetime import date

PATH_TO_SAVE = "../data/" 
PREFIX = date.today().strftime('%Y-%m-%d-')
FILE_TO_GET = ['nasdaqlisted.txt']
# , 'otherlisted.txt'
def main():
   
   try:
      ftp = FTP('ftp.nasdaqtrader.com')
      ftp.login()
      ftp.cwd('SymbolDirectory')

      for i,file_name in enumerate(FILE_TO_GET):
         print("Downloading {} {}/{}...".format(file_name, i+1, len(FILE_TO_GET)))
         ftp.retrbinary("RETR " + file_name, open(PATH_TO_SAVE + PREFIX + file_name, 'wb').write)

   except ftp.all_errors as err:
      print("FTP Error ! Can't download the files requested.")
      
   ftp.quit()

if __name__ == "__main__":
   print("                                     ")
   print("Get Today`s Nasdaq Stocks Information")
   print("=====================================")
   main()

