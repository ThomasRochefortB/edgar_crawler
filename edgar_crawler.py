def edgar_crawler(ticker,filingtype,sincedate):
    #Sincedate has to be in the form 'YYYY-MM-DD'
    # import our libraries
    import requests
    from bs4 import BeautifulSoup
    import pandas
    import os
    import timeit
    from datetime import date
    
    start = timeit.default_timer()
    ticker=ticker.lower()              ## EDGAR seems to not recognize capitalized tickers....
    dir = 'sec_edgar_filings/'
    if os.path.exists(dir)==False:
        print("Making a home directory 'sec_edgar_filings' for the filings")
        os.makedirs(dir)

    cik_db=pandas.read_csv('ticker_cik.txt', sep='\t', lineterminator='\n')
    cik=cik_db.loc[cik_db['co_tic'] == ticker].CIK

    # base URL for the SEC EDGAR browser
    endpoint = r"https://www.sec.gov/cgi-bin/browse-edgar"
    dir = 'sec_edgar_filings/{0}'.format(ticker)
    if os.path.exists(dir)==False:
        print('Making a subdirectory for the company:',ticker)
        os.makedirs(dir)
    
    dir ='sec_edgar_filings/{0}/{1}'.format(ticker,filingtype)
    if os.path.exists(dir)==False:
        os.makedirs(dir)
        
    save_path = ('sec_edgar_filings/{0}/{1}'.format(ticker,filingtype))
    # define our parameters dictionary
    today = date.today()
    today = today.strftime("%y%m%d")
    param_dict = {'action':'getcompany',
                  'CIK':cik,              #Can also use: 'Company': 'Microsoft',
                  #'company':'Microsoft',
                  'type':filingtype,
                  'dateb':today,
                  'owner':'exclude',
                  'start':'',
                  'output':'atom',
                  'count':'100'}

    # request the url, and then parse the response.
    response = requests.get(url = endpoint, params = param_dict)  # This is the url of the search results, not the annual report itself
    soup = BeautifulSoup(response.content, 'lxml')

    # Let the user know it was successful.
    print('Request Successful')
    print(response.url)

    # find all the entry tags
    entries = soup.find_all('entry')

    # initalize our list for storage
    master_list_xml = []
    accession_num_saved=[]
    # loop through each found entry on the search results page
    for entry in entries:

        # grab the accession number so we can create a key value
        accession_num = entry.find('accession-nunber').text
        accession_num_saved.append(accession_num)

        # create a new dictionary
        entry_dict = {}
        entry_dict[accession_num] = {}

        # store the file info
        entry_dict[accession_num]['file_info'] = {}
        entry_dict[accession_num]['file_info']['filing_date'] =  entry.find('filing-date').text
        entry_dict[accession_num]['file_info']['filing_href'] = entry.find('filing-href').text
        entry_dict[accession_num]['request_info'] = {}
        entry_dict[accession_num]['request_info']['link'] =  entry.find('link')['href']
        entry_dict[accession_num]['request_info']['title'] =  entry.find('title').text
        entry_dict[accession_num]['request_info']['last_updated'] =  entry.find('updated').text
        
        # store in the master list
        master_list_xml.append(entry_dict)
        
    # Loop through the filings found on the results page
    for z in range(0,len(master_list_xml)):
        if master_list_xml[z][accession_num_saved[z]]['file_info']['filing_date']>=sincedate: 
            filing_date=master_list_xml[z][accession_num_saved[z]]['file_info']['filing_date']
            url_2=master_list_xml[z][accession_num_saved[z]]['request_info']['link']
            response2 = requests.get(url=url_2,stream=True)
            soup2 = BeautifulSoup(response2.content, 'lxml')

            try:
                target=soup2.findAll("table", {"class": "tableFile"})
                target2=target[0].findAll('tr')
                target3=target2[1].findAll('a',href=True)
                html=target3[0]['href']
                filetype=target3[0].text.split('.')[1]
                if filetype=='htm':
                    filetype='html' 
                prefix='https://www.sec.gov/'
                finalhtml=prefix+html
                if '/ix?doc=/' in finalhtml:
                    finalhtml=finalhtml.replace('/ix?doc=/','')

            except:
                print('Encounterd an invalid file from:',master_list_xml[z][accession_num_saved[z]]['file_info']['filing_date'],'\n')

            # grab the response
            response = requests.get(finalhtml, stream=True)
            content=response.content
            file_name=accession_num_saved[z]
            name_of_file = ('%s.%s' % (file_name,filetype))   # The file will be named with the accession number of the file
            completeName = os.path.join(save_path, name_of_file) 
            if os.path.exists(completeName):
                print('The',filingtype,'of',ticker,'from',filing_date,'already exists on the drive')
            else:
                open(completeName, "wb").write(content)


    stop = timeit.default_timer()
    print('Time: ', (stop - start))  

# Partie du code qui sera roule si le script lui-meme est execute.
if __name__ == '__main__':
    edgar_crawler('aapl','10-K','2000-01-01')