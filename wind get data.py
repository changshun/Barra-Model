# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 11:44:29 2017

@author: Rebecca Cui
"""

from WindPy import *
import datetime  #datetime
import pandas as pd
#--------------------------------根据需要修改下面的参数--------------------------
market_cols = ['close','open','high','low','mkt_cap_ard','volume','pct_chg',
               'turn','west_netprofit_CAGR','roe_ttm2',
               'beta_100w','yoyeps_basic','free_float_shares','ATR',
               'industry_gicscode','pe_ttm','tot_liab','cap_stk','tot_assets','longdebttodebt']
index_codes = ['000016.SH','000905.SH','000906.SH','000852.SH','000300.SH']
beginDate = '2017-07-05'
endDate = '2017-08-01'
path = r'C:\\DELL\\internship\\CICC\\Barra\\raw data' # 结果储存路径
#------------------------------------------------------------------------------
today = datetime.date.today().strftime('%Y-%m-%d')
#endDate = (datetime.date.today()-datetime.timedelta(days=1)).strftime('%Y-%m-%d')
w.start()
def GetMarketInfo(code,cols):
    global beginDate
    ipoDate = w.wss(code,'ipo_date').Data[0][0].strftime('%Y-%m-%d')
    if ipoDate > beginDate:
        beginDate = ipoDate
    else:
        beginDate = beginDate
    dailyQuota = w.wsd(code,','.join(cols),beginDate,endDate,"Fill=Previous")
    df = pd.DataFrame(dict(zip(cols,dailyQuota.Data)),index=dailyQuota.Times)
    return df
def Align(code,df):
    df.reset_index(inplace=True)
    df.rename(columns={'index':'datetime'},inplace=True)
    df['code'] = code
    df.set_index(['datetime','code'],inplace=True)
    try:
        df['pct_chg'] /= 100
    except:
        print('无pct_chg字段')
    return df
def Concat(codes,cols):
    dfs = pd.DataFrame()
    for code in codes:
        print('开始下载%s数据'%code)
        df_temp = GetMarketInfo(code,cols)
        df_temp = Align(code,df_temp)
        dfs = dfs.append(df_temp)
        dfs.to_pickle(path+r'\test')
    return dfs
# 通过wset取当前市场全部A股
stockSector = w.wset("sectorconstituent","date="+today+";sector=全部A股")
dates,codes,names = stockSector.Data
#股票数据
dfs = Concat(codes,market_cols)
pl = dfs.to_panel()
pl = pl.transpose(1,2,0)
pl.to_pickle(path+r'\data')
#pl.to_pickle(path+r'\stock')
#指数数据
#df_index = Concat(index_codes,['pct_chg'])
#df_index.to_csv(path+r'\stock_index.csv')
w.stop()



    
