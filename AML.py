# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 11:58:57 2021

@author: sma
"""



import pandas as pd
import numpy as np


# Read the transaction data from excel

AML_data = pd.read_excel('C://Users//sma//Desktop//AML//SQL//AML.xlsx',sheet_name='DATA')
AML_data


# To prepare the master table

Rule_TM003 = pd.DataFrame(columns=['Rule','id','var1','var2'])

for i in (AML_data['PB']+'&'+AML_data['Type']+'&'+AML_data['Risk']).unique():
    Rule_TM003 = Rule_TM003.append(pd.DataFrame({'Rule':'TM003',
                                                   'id': [i],
                                                   'var1':'交易金额',
                                                   'var2':'当天累计交易总额'}))

# To prepare the percentile table 

Percentile = pd.DataFrame(columns=['Rule','var1_per','var2_per'])
# Percentile =Percentile.reset_index(drop=True)


for u in range(70,100):
    for v in range(70,100):
        Percentile = Percentile.append(pd.DataFrame({'Rule':'TM003',
                                                     'var1_per':[u/100],
                                                     'var2_per':[v/100]}))


# To prepare Percentile_TM003 

Percentile_TM003 = pd.merge(Rule_TM003,Percentile,on=['Rule'])
Percentile_TM003





def get_var1_value(x,u):
    return np.percentile(AML_data.loc[(AML_data['PB']+'&'+AML_data['Type']+'&'+AML_data['Risk']==x),:]['交易金额'],u*100)

# get_var1_value('non-PB&个人&L',0.99)

Percentile_TM003['var1_value'] = Percentile_TM003.apply(lambda x: get_var1_value(x.id,x.var1_per), axis=1)

# Test function
# AML_data['PB']+AML_data['Type']+AML_data['Risk']
# print(np.percentile(AML_data.loc[(AML_data['PB']=='PB') & (AML_data['Type']=='个人')& (AML_data['Risk']=='L'),:]['交易金额'],50))
# print(AML_data.loc[(AML_data['PB']=='PB') & (AML_data['Type']=='个人')& (AML_data['Risk']=='L'),:]['交易金额'].median())
# print(get_var1_value('PB&个人&L',0.5))


# Percentile_TM003
# AML_data


def Cal_Accm_Amount(x,y):
    return AML_data.loc[(AML_data['客户号码']==x)&(AML_data['交易日期']==y),:]['交易金额'].sum()

# check
# Cal_Accm_Amount(1528,'2020-07-22')

AML_data['Accm_Amount'] = AML_data.apply(lambda x: Cal_Accm_Amount(x.客户号码,x.交易日期),axis=1)

# check
# AML_data.loc[AML_data['客户号码']==1528,['交易日期','交易金额','Accm_Amount']] 
# AML_data
# Percentile_TM003


def get_var2_value(x,u):
    return np.percentile(AML_data.loc[(AML_data['PB']+'&'+AML_data['Type']+'&'+AML_data['Risk']==x),:]['Accm_Amount'],u*100)    

# get_var2_value('non-PB&个人&L',0.91)

Percentile_TM003['var2_value'] = Percentile_TM003.apply(lambda x: get_var2_value(x.id,x.var2_per), axis=1)

Percentile_TM003



# len(AML_data.loc[(AML_data['PB']+'&'+AML_data['Type']+'&'+AML_data['Risk']=='non-PB&个人&L')&(AML_data['交易金额']>9030000),:])

# temp = AML_data.loc[(AML_data['PB']+'&'+AML_data['Type']+'&'+AML_data['Risk']=='non-PB&个人&L'),:]
# temp.to_excel('temp_data_python.xlsx')



def CalTotalCount(x):
    return len(
        AML_data.loc[(AML_data['PB']+'&'+AML_data['Type']+'&'+AML_data['Risk']==x),:]
        )


def CalPositiveCount(x,y,z):
    return len(
        AML_data.loc[(AML_data['PB']+'&'+AML_data['Type']+'&'+AML_data['Risk']==x)&((AML_data['交易金额']>=y)|(AML_data['Accm_Amount']>=z)),:]
        )

def CalRMCount(x,y,z):
    return len(
        AML_data.loc[(AML_data['PB']+'&'+AML_data['Type']+'&'+AML_data['Risk']==x)&((AML_data['交易金额']>=y)|(AML_data['Accm_Amount']>=z))&(AML_data['RM']=='RM'),:]
        )
    


Percentile_TM003['TotalCount'] = Percentile_TM003.apply(lambda x: CalTotalCount(x.id), axis=1)

Percentile_TM003['TotalPositiveCount'] = Percentile_TM003.apply(lambda x: CalPositiveCount(x.id,x.var1_value,x.var2_value), axis=1)

Percentile_TM003['TotalRMCount'] = Percentile_TM003.apply(lambda x: CalRMCount(x.id,x.var1_value,x.var2_value), axis=1)

Percentile_TM003.to_excel('Percentile_TM003_Result2.xlsx')













