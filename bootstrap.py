import numpy as np
import csv
import datetime
import matplotlib.pyplot as plt

bdate= '09-01-2017' #Date of Bond Data
Bdate= datetime.datetime.strptime(bdate,'%d-%m-%Y') #Convert bond date into datetime object

data = np.genfromtxt(bdate+'.csv', delimiter=',', dtype=None) #Read entire CSV into array
data = [el for el in data if el[0]=='Canada' and datetime.datetime.strptime(el[2],'%Y-%b-%d').year<2022] #Keep only the Canada bonds up to 2022


#If two bonds have the same maturity, keep only the one appearing first in the list
seen = set()
data = [el for el in data if not (el[2] in seen or seen.add(el[2]))]

#For debugging keep track of interpolated coupon rates
crates = []

sdata= [] #Structured Data (years to maturity, coupon, bond price)
for el in data:
	edate=datetime.datetime.strptime(el[2],'%Y-%b-%d') #Datetime object for current bond maturity
	diff= (edate-Bdate).total_seconds()/31536000 #Difference in days, expressed in years
	#Now make the prices 'Dirty' by finding the time since last coupon payment and bond data date
	coupon = el[1]
	cleanprice = el[3]
	lpay= np.ceil(diff/0.5)/2-diff #Years from last coupon payment (Note: Bounded below 0.5)
	dirtyprice = cleanprice+coupon*lpay
	#A coupon-bond makes a coupon payment at its date of maturity. A coupon bond 
	#with less than 6mo to maturity can be viewed as a zero coupon bond, with the
	#last coupon payment added to the face value.
	#Finding zero coupon yields for such bonds requires the dirtyprice, coupon,
	#years to maturity	
	if diff<0.5 :#single payment bonds
		zyield=-np.log(dirtyprice/(100+coupon/2))/diff
	else :#subtract coupon payments from dirtyprice discounted at z-y rate
		diff2=diff
		dpdim=dirtyprice #diminished dirtyprice
		while diff2>0.5:
			#cdate=date of coupon payment
			m=(edate.month-6)%12
			if m==0:
				m=12
				cdate=edate.replace(month=m, year=edate.year-1)
			elif m>6:
				cdate=edate.replace(month=m, year=edate.year-1)
			else:
				cdate=edate.replace(month=m)
			#calculate zero yield at that coupon payment by linear interpolation
			#first look for zero yield closest to cdate in previously studied bonds
			
			for em in sdata:
				if em[0]==cdate:
					zycdate=em[4] #z-y rate was already known
					break
				elif em[0]<cdate:	
					d1=em[0]
					zy1=em[4]	
				elif em[0]>cdate:
					d2=em[0]
					zy2=em[4]					
					#if d2>d1:#find time from cdate to d2 as fraction of d2-d1 (bounded 0-1)
					d=(d2-cdate).total_seconds()/(d2-d1).total_seconds()
					zycdate=(1-d)*zy2+d*zy1 #this is z-y rate interpolated to coupon date
					break
			crates.append([cdate,zycdate])
			diffc= (cdate-Bdate).total_seconds()/31536000
			cf=(coupon/2)*np.exp(-zycdate*diffc)#discounted cashflow (Ask Jesse..)		        
			dpdim=dpdim-cf
			diff2=diff2-0.5	#go back 6 months and discout that coupon
		
		zyield=-np.log(dpdim/(100+coupon/2))/diff
	sdata.append([edate, diff, coupon, dirtyprice, zyield])
#Remove duplicates in rates for coupons
seen2 = set()
crates = [el for el in crates if not (el[0] in seen2 or seen2.add(el[0]))]
	
dates= [el[0] for el in sdata]
yields = [el[4] for el in sdata]

plt.plot(dates,yields, 'b*')
plt.plot([el[0] for el in crates],[el[1] for el in crates],'r.')
for el in crates:
	print el[0], el[1]
plt.gcf().autofmt_xdate()
plt.show()

#TODO: After 2022 we only have bond data for 1 yr increments, so we can't calculate half year coupon payments at zero yield rates. 





