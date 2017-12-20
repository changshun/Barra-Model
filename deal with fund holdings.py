# -*- coding: utf-8 -*-
"""
Created on Dec 13 14:45:57 2017

@author: Rebecca Cui
"""

import pandas as pd
import os
path = r'C:\DELL\internship\CICC\Barra\test'
file_list = os.listdir(path) # 指定文件夹中的所有文件
# 删除文件夹中无用的表

def Replace(s):
    dic = {'0101':'.SH','01990':'.SH','07010':'SH',
           '3101':'.SZ','4101':'.SZ','31990':'.SZ','41990':'.SZ','33010':'.SZ'}
    prefix = s[-6:]
    suffix = s[4:8]
    ss = prefix + dic[suffix]
    return ss


def GetEquity(df):  
    start = df[df['科目代码']=='1102'].index[0]
    end = df[df['科目代码']=='1204'].index[0] + 1
    #1102-1204间的数据
    df = df.iloc[start:end,:]
    #科目代码长度为14的数据
    df = df[(df['科目代码'].str[:4]=='1102') & (df['科目代码'].str.len()==14)]
    df = df[~df['科目代码'].str[4:8].isin(['0199','3199','4199','0301','3301','0701'])]
    df['code'] = df['科目代码'].map(Replace)
    df.set_index('code',inplace=True)
    ser = df['市值占净值%']
    ser.name = date
    return ser

def GetValue(df):
    pct = df.loc[df['科目代码']=='110201','市值占净值%'].values[0]/100
    equity = df.loc[df['科目代码']=='累计单位净值:','科目名称'].values[0]
    equity = float(equity)
    value = equity*pct
    return value

#ser = GetNet(df)
rt_equity = pd.DataFrame()
rt_cols = []
rt_vals = []
pt_equity = pd.DataFrame()
pt_cols = []
pt_vals = []

for file in file_list:
    df = pd.read_excel(path+'\\'+file,header=3)
    if not (('1102' in df['科目代码'].values) and ('1204' in df['科目代码'].values)):
        continue
    print(file)
    if len(file)==39:
        date = file[-12:-4]
        rt_cols.append(date)
        rt_vals.append(GetValue(df))
        ser = GetEquity(df)
        df_col = pd.DataFrame(ser)
        rt_equity = pd.concat([rt_equity,df_col],axis=1)
    else:
        date = file[-14:-4].replace('-','')     
        pt_cols.append(date)
        pt_vals.append(GetValue(df))
        ser = GetEquity(df)
        df_col = pd.DataFrame(ser)
        pt_equity = pd.concat([pt_equity,df_col],axis=1)
    
rt_cal = pd.DataFrame(rt_vals,index=rt_cols,columns=['equity'])
rt_cal['pct_chg'] = rt_cal['equity'].pct_change(1)
rt_cal = rt_cal.T
pt_cal = pd.DataFrame(pt_vals,index=pt_cols,columns=['equity'])
pt_cal['pct_chg'] = pt_cal['equity'].pct_change(1)
pt_cal = pt_cal.T
pt_equity = pt_equity.fillna(0)
rt_equity = rt_equity.fillna(0)
pt_equity = pt_equity/100.0
rt_equity = rt_equity/100.0
def sstd(ser):
    a = ser.sum()
    b = 1.0/a
    ser = ser * b
    return ser
pt_equity = pt_equity.apply(sstd)
rt_equity = rt_equity.apply(sstd)
# 看rt_equity,rt_cal,pt_equity,pt_cal这4个变量
rt_equity.to_csv('C:\DELL\internship\CICC\Barra\\raw data\\rt_hold.csv')
rt_cal.to_csv('C:\DELL\internship\CICC\Barra\\raw data\\rt_net.csv')
pt_cal.to_csv('C:\DELL\internship\CICC\Barra\\raw data\\pt_net.csv')
pt_equity.to_csv('C:\DELL\internship\CICC\Barra\\raw data\\pt_hold.csv')


