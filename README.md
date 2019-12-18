# edgar_crawler
This function collects the html files of the sec filings of a company from the [EDGAR](https://www.sec.gov/edgar/searchedgar/companysearch.html) database and saves them in the running directory.


## Getting Started

In this repository you will find the following files :

- edgar_crawler.py : The python script containing the edgar_crawler() function.

- SP500.csv : A .csv file containing the constituents of the S&P500 from October 3rd, 2019

- test_SP500.py : A script to test the edgar_crawler function.

- ticker_cik.txt : A file mapping all the CIK numbers from EDGAR to their coresponding ticker. File obtained from (http://rankandfiled.com/#/data/tickers)

## How to use

The function edgar_crawler(ticker, filing_type, since_date) has three entries:

- ticker: A string containing the ticker of the company from which we want to download the sec filings. Ex : 'aapl', 'msft', ...

- filing_type : A string containing the type of report that we want to download. Supported types:
        '10-K' (Annual report)
        '10-Q' (Quarterly report) NOT TESTED
        'DEF-14A' (Shareholders proxy statement) NOT TESTED


- since_date : A string containing the date from which we want to download the filings. Must be in the format 'YYYY-MM-DD'. Ex : '2000-01-01' will download all the filings from January 1st, 2000. 

Example: 
        
        edgar_crawler(' aapl ', ' 10-K ', ' 2000-01-01 ') 
will download all the annual report of Apple since January 1st, 2000.  It is this example that is executed if you run edgar_crawler.py directly.

To download all the annual report from the companies in the SP500 since 2000, execute the following command in the terminal window:
        
        python3 test_SP500.py
        
Make sure the terminal environment is running from the "edgar_crawler" directory.

### Prerequisites

This project runs on python 3.7.5. To install python visit the following page : (https://www.python.org/downloads/)


The following python package were used:

- requests 
- beautifulsoup4
- pandas
- os
- timeit
- datetime

Python comes with the package installer "pip". To install the package execute the following command in the terminal:

    pip install requests
    pip install beautifulsoup4
    pip install pandas
    pip install os
    pip install timeit
    pip install datetime

## Built With

* [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - The parsing library used to parse the HTML from EDGAR.

