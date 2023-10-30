from bs4 import BeautifulSoup
import requests
import lxml
import pandas as pd


### -- Get Response -- ######


def get_valid_response(urls):
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException:
            # If there's an error, proceed to the next URL
            pass
    return None



##### ------ Fundamentals -------#######


def fundamentals(symbols,key=None):
    
    if not isinstance(symbols, list):
        symbols = [symbols]  # Convert a single symbol to a list
   
    keys = ['Quarterly Results', 'Profit & Loss','Balance Sheet', 
            'Cash Flows', 'Ratios', 'Shareholding Pattern q', 
            'Shareholding Pattern y']
    
    all_results = {}
    
    for symbol in symbols:
        results = []
        
        urls = [f'https://www.screener.in/company/{symbol}/', f'https://www.screener.in/company/{symbol}/consolidated/']
        response = get_valid_response(urls)
        if response is None:
            continue
         

        soup = BeautifulSoup(response.text,'html.parser')

        for i, table in enumerate(soup.find_all('table', class_='data-table')):


            column_header_raw = table.find_all('th')

            column_header = [headers.text.strip() for headers in column_header_raw]

            df = pd.DataFrame(columns= column_header)

            column_data = table.find_all('tr')

            for row in column_data[1:]:
                row_data = row.find_all('td')
                individual_row_data = [data.text.strip() for data in row_data]
                lenght = len(df)
                df.loc[lenght]=individual_row_data
                df = df.rename(columns={df.columns[0]: 'Particulars'})
                data_df = df[df['Particulars'] != 'Raw PDF']
                data_df.loc[:, 'Particulars'] = data_df['Particulars'].str.replace(' ', '').str.replace('+', '')
            results.append(data_df)
        #     df.insert(0, 'Symbol', symbol)
        #     df = df.rename(columns={df.columns[1]: 'Particulars'})
        #     df.columns = df.columns.str.strip('+')
        #     results[keys[i]] = df
        
        # all_results[symbol] = results
    return results[0]
            
            
    # if key is not None:
    #     selected_results = [{symbol: results[keys] for symbol, results in all_results.items() if keys in results} for keys in key]
    #     return selected_results[0]
        
        
    # else:
    #     return None
    
    
####### --- Sector and Industry -- #########

def Sector(symbols):
    
    if not isinstance(symbols, list):
        symbols = [symbols]  # Convert a single symbol to a list
    
    all_results = {}
    
    for symbol in symbols:
        results = {}
        key = None
        urls = [f'https://www.screener.in/company/{symbol}/', f'https://www.screener.in/company/{symbol}/consolidated/']
        response = get_valid_response(urls)
        if response is None:
            continue
        
        soup = BeautifulSoup(response.text,'html.parser')
        rawhtml = soup.find_all('p',class_="sub")
        rawdata = [headers.text.strip() for headers in rawhtml]
        
        filterdata_list = []
        for lines in rawdata:
            splitdata = lines.split('\n')
            filterdata = [s for s in splitdata if s.strip()]
            filterdata1 = [string.strip() for string in filterdata]
            filterdata_list.extend(filterdata1)
        
        
        for line in filterdata_list:
            if line.startswith('Sector'):
                key = 'Sector'
            elif line.startswith('Industry'):
                key = 'Industry'
            elif key is not None:
                results[key]= line.strip()
                key = None
            else:
                pass
        results['Symbol'] = symbol 
        all_results[symbol]= results
    
    
    df = pd.DataFrame(all_results).T
    return df   



######-------- #####################