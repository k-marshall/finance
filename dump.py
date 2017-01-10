import csv
import datetime
from bs4 import BeautifulSoup
from urllib2 import urlopen


def fetch_bond_data():
        """Fetchs bond information from pfin.ca and saves it in a csv file
        whose name is just the date on which it was downloaded"""
        

        
        now = datetime.datetime.now()
        soup = BeautifulSoup(urlopen('http://www.pfin.ca/canadianfixedincome/tabs/tabCanada.aspx'),"lxml")

        table = soup.find_all('table')[0]

        rows = []

        for row in table.find_all('tr',attrs={"class": ["normalRow","alternatingRow"]}):
	        rows.append([val.text.encode('utf8') for val in row.find_all('td')])

                with open('{:%d-%m-%Y}'.format(now)+'.csv', 'wb') as f:
	                writer = csv.writer(f)
	                writer.writerows(row for row in rows if row)

