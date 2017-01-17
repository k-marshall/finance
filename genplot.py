import matplotlib.pyplot as plt
from bootstrap import bootstrap

x=[]
for i in range(10,17):
    bdate=str(i)+'-01-2017'
    x.append(bdate)
    dates,yields=bootstrap(bdate)
    plt.plot(dates,yields)

plt.gcf().autofmt_xdate()
plt.show()


