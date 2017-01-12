import numpy as np
import datetime

bdate= '09-01-2017' #Date of Bond Data
Bdate= datetime.datetime.strptime(bdate,'%d-%m-%Y') #Convert bond date into datetime object

data = np.genfromtxt(bdate+'.csv', delimiter=',', dtype=None) #Read entire CSV into array
data = [el for el in data if el[0]=='Canada'] #Keep only the Canada bonds

sdata= [] #Structured Data (years to maturity, coupon, bond price)
for el in data:
	edate=datetime.datetime.strptime(el[2],'%Y-%b-%d') #Datetime object for current bond maturity
	diff= (edate-Bdate).total_seconds()/31536000 #Difference in days, expressed in years
	
	#Now make the prices 'Dirty' by finding the time since last coupon payment and bond data date
	coupon = el[1]
	cleanprice = el[3]
	lpay= np.ceil(diff/0.5)/2-diff #Years from last coupon payment (Note: Bounded below 0.5)
	dirtyprice = cleanprice+coupon*lpay
	sdata.append([diff, coupon, dirtyprice])

for el in sdata: print el #Debugging

#TODO: Find any duplicate time to maturity and randomly keep one while discarding the others





