import matplotlib.pyplot as plt
from bootstrap import bootstrap
import glob, os, time, datetime
import numpy as np

os.chdir("./data/")
files = glob.glob('*.csv')
files.sort()
files = [x[:-4] for x in files]
os.chdir("..")
#We are assuming that last bond (longest Maturity) in the first file, covers the range of all bonds in all later files as well
Yields = []
Forwards = []
for tind, bdate in enumerate(files):
    feb1 = datetime.datetime(2017,02, 01)
    period = 182.5 #in days

    dates,yields=bootstrap(bdate)

    udates = [(x - feb1).days  for x in dates]
    idates = np.arange(0,period-udates[-1]%period+udates[-1]+1,period) #interpolated dates values every 6months
    iyields = np.interp(idates, udates, yields)
    Yields.append(iyields)
    idates = [feb1 + datetime.timedelta(days=x) for x in idates] #Convert back to datetimes

    t = datetime.datetime.strptime(bdate,'%d-%m-%Y')
    mlogP = []
    for idx, el in enumerate(idates):
        mlogP.append((el-t).days/365.0 * iyields[idx])

    forwards = []
    forwards.append((mlogP[1]-mlogP[0])/period*365)

    for idx in np.arange(1,len(mlogP)-1,1):
        forwards.append((mlogP[idx+1]-mlogP[idx-1])/(2*period)*365)

    forwards.append((mlogP[-1]-mlogP[-2])/period*365)
    Forwards.append(forwards)

    #plt.plot(dates,yields,'.') #Raw data
    plt.plot(idates,forwards,'.') #Interpolated data
    #plt.plot(idates,np.gradient(mlogP)/period,'r.') #This seems to be the same...

Yields = np.array(Yields).transpose()
Forwards = np.array(Forwards).transpose()

Xijyield= np.array(map(np.diff,[map(np.log,x) for x in Yields]))
Xijforward= np.array(map(np.diff,[map(np.log,x) for x in Forwards]))

ycov = np.cov(Xijyield)
fcov  = np.cov(Xijforward)

yeigs= np.linalg.eigvals(ycov).real
yeigs.sort()
print yeigs

plt.gcf().autofmt_xdate()
plt.show()


