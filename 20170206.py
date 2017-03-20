
##---(Thu Jan 26 17:56:48 2017)---
import pandas as pd
from math import log
#import math
from pandas import DataFrame
import time

test=pd.read_csv('./test_distance.csv')
a=test.groupby('pathid',as_index=False).sum()
b=test.groupby('pathid',as_index=False).count()
c=test[test.distance<30]
c=c.groupby('pathid',as_index=False).count()
c=pd.DataFrame(c,columns=['pathid',time])
b=pd.DataFrame(b,columns=['pathid',time])

b=test.groupby('pathid',as_index=False).count()
b=pd.DataFrame(b,columns=['pathid','time'])
c=c.groupby('pathid',as_index=False).count()
c=pd.DataFrame(c,columns=['pathid','time'])
b.columns=['pathid','t1']
c.columns=['pathid','t2']
a=pd.merge(a,b,how='left',on='pathid')
a=pd.merge(a,c,how='left',on='pathid')
c=c.groupby('pathid',as_index=False).count()
c=test[test.distance<30]
c=c.groupby('pathid',as_index=False).count()
c=pd.DataFrame(c,columns=['pathid','time'])
c.columns=['pathid','t2']
del a['t2']
a=pd.merge(a,c,how='left',on='pathid')
a=a.fillna(0)


e=test.groupby(['pathid','ps'],as_index=False).count()

del e['ps']
del e['distance']
del e['time']
del e['ID']

e1=e[e.index%2==0]
e2=e[e.index%2==1]
del e1['lon']
del e2['lat']
e3=pd.merge(e1,e2,how='outer',on='pathid')
e3.columns=['pathid','k','m']
e3=e3.fillna(0)
e3['h']=e3.k+e3.m
e3.m=e3.m/e3.h
e3.k=e3.k/e3.h
a=pd.merge(a,e3,how='left',on='pathid')


a['time']=a.distance*0.014+a.distance.apply(lambda x:350*log(x))+a.t1*3.1+a.t2*70+a.k*30-1902
a.time.mean()
d=pd.DataFrame(a,columns=['pathid','time'])
d.to_csv('./result.csv',index=False)