import edgar_crawler
import pandas
SP500=pandas.read_csv('SP500.csv')
ticker=SP500.co_tic

filing_type = '10-K'
since_date='2000-01-01'

for tik in ticker:
    edgar_crawler.edgar_crawler(tik,filing_type,since_date)