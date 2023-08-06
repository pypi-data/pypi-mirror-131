from pandas import DataFrame
import pandas
import json
import requests
from datamemorys.core import SYCM_DATAS

import time
class DMDataFrame(DataFrame):
    def __init__(self,DM_tablename="",loginnNickName="",data=None,index=None,columns=None,dtype=None,copy=False,**args):
        if DM_tablename=="" and loginnNickName=="" and  len(data)>=0:
            super().__init__(data,index,columns,dtype,copy)            
        else:
            loginnNickName=loginnNickName.split(":")[0]
            t1=time.time()
            print('开始取数')
            j=requests.get(SYCM_DATAS[DM_tablename].format(loginnNickName)).json()
            t2=time.time()
            print('从接口取数完毕一共{}行耗时{}'.format(str(len(j['data'])),str(t2-t1)))
            if j['code']!=0:            
                super().__init__()
            else:
                d=j['data']
                c=j['comments']
                ks={}
                for x in c:
                    ks[x]=c[x]['cName']                 
                df_=DataFrame(d)       
                df_=df_.rename(columns=ks)   
                for x in args:
                    if c[x]['cName'] in df_.keys():                    
                        df_=df_[df_[c[x]['cName']]==args[x]]
                super().__init__(data=df_.to_dict('records'))


            


    def Mysqlsqlstr(self,tablename):
        if len(self)==0:
            return ''
        df=self.astype(str)
        kk=df.keys()
        d=[[df[y][x].replace("'","''") for y in kk] for x in df.index]
        d=["('"+"','".join(x)+"')" for x in d]
        sql="insert into {}(`".format(tablename)+"`,`".join(kk)+"`) values"+ ",".join(d)
        return sql