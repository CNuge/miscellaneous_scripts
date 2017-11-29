


from pandas import DataFrame
import pandas_datareader.data as web
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from datetime import date, datetime, timedelta

def date_splits(start_date, end_date, delta=timedelta(days=30)):
	""" a generator to return 30 day intervals between two dates"""
	current_date = start_date
	while current_date < end_date:
		yield current_date
		current_date += delta

def date_pairs(start_date, end_date, delta=timedelta(days=30)):
	""" take the days at 30 day intervals, and make them into tuple pairs"""
	date_tuples = []
	dates = date_splits(start_date, end_date, delta=timedelta(days=30))
	front_day = next(dates)
	for back_day in dates:
		date_tuples.append((front_day, back_day))
		front_day = back_day
	return date_tuples
		

def get_stock_url(market, stock, start_date, end_date):
	""" take a pair of datetime objects and get the url for the matching stock data table"""
	""" note for international stocks google currently shows a maximum of 30 days per page"""
	params = {'q': '{}:{}'.format(market, stock), 'startdate':start_date, 'enddate':end_date}
	url = 'https://finance.google.com/finance/historical'
	r = requests.get(url=url, params=params)
	return r.url

def get_international_stock_prices(market, stock, start_date, end_date):
	""" for a given stock market and stock, query google finance and build a 
		dataframe with the data between the two dates given"""
	#retrieve the datetime pairs
	date_intervals = date_pairs(start_date, end_date)
	stock_data = DataFrame(columns = ['Date','Open','High','Low','Close','Volume'])
	for pair in date_intervals:
		#get the url for the pair
		historical_price_page = get_stock_url(market, stock, pair[0], pair[1])
		stock_dat = urlopen(historical_price_page)
		#then parse the table with BS 
		historical_page = BeautifulSoup(stock_dat,'lxml')
		table_dat = historical_page.find('table',{'class':'gf-table historical_price'})
		rows = table_dat.findAll('td',{'class':'lm'})
		dates = [x.get_text().rstrip() for x in rows]
		#get datetime formatted dates
		datetime_dates = [datetime.strptime(x, '%b %d, %Y') for x in dates]
		prices = []
		#iterate and grab column data
		for num, row in enumerate(rows):
			row_dat = [datetime_dates[num]] #first column is the dates
			for i in row.next_siblings: 
				row_dat.append(i.get_text().rstrip()) 
			prices.append(row_dat) #add the row to the list of rows
		window_data = DataFrame(prices,columns = ['Date','Open','High','Low','Close','Volume'])
		#cleanup, set index and make volume integers
		window_data["Volume"] = window_data["Volume"].apply(lambda x: int(x.replace(',','')))
		stock_data = stock_data.append(window_data)
	
	#change the other columns to floating point values
	for col in ['Open','High','Low','Close']:
		stock_data[col] = stock_data[col].apply(lambda x: float(x))
	stock_data = stock_data.set_index('Date')
	stock_data = stock_data.sort_index() #sort the index so it is oldest to newest
	return stock_data

def get_american_stock_dat(stock_of_interest, start_time, now_time):
	""" get a dataframe for an american stock of interest """
	f_dat = web.DataReader(stock_of_interest, 'google', start_time, now_time)
	return f_dat



if __name__ == '__main__':

	#Demonstration of how the date iteration works
	now_time = datetime.now() 

	start_time = datetime(now_time.year , now_time.month - 9, now_time.day)

	intervals = date_pairs(start_time,now_time)

	#url retrevial test
	url_test = get_stock_url('TSE','RY', intervals[0][0], intervals[0][1])
	print(url_test)


	get_international_stock_prices('TSE','RY', start_time, now_time)
