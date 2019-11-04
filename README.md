# Nasdaq Stock Price

This set of scripts builds a Google Docs Spreadsheets for Nasdaq Prices follow-up using Google Finance and GoogleAPI in Python.
The scripts get the stocks listed in Nasdaq's FTP Server and populates a Spreadsheet in google docs
using the Python GoogleAPI. 

If you want to use these scripts, you need to provide the google credentials in a 
file named 'credential-google.json' at ../credentials. If you prefer, you can change the logic in the code.

## Table Example 

|stocks|price|priceopen|high|low|volume|datedelay|change|changepct|closeyest|shares|
|------|------|------|------|------|------|------|------|------|------|------:|
|CBAN	|13,55	|#N/A	|#N/A	|#N/A	|0	|#N/A	|0	|0	|13,55|8439259|
|FGBI	|25,99	|25,99	|25,99	|25,99	|0	|#N/A	|-0,01	|-0,04	|26	|7609192|
|CNXR	|0,82	|0,82	|0,82	|0,82	|0	|#N/A	|0	|0,12	|0,82	|20841000|


