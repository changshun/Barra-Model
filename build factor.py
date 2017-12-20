import numpy as np
import pandas as pd
import datetime as dt
from datetime import timedelta
import statsmodels.api as sm
import scipy.stats.mstats as ssm
import pdb
import math

#property copyright "Shiying Cui"
#property version   "5.0"
#property private!!!
######1 ATR 2.Beta50 3. 收盘 4. 自由流通股本 5. 最高价 6. 所属行业wind代码 7. 最低价 8.总市值 9. 开盘价 10.收益率 11. 前n名重仓股票市值合 12.  净资产收益率TTM 13. 企业账面权益 14. 企业总负债  15. 企业总资产  16. 企业长期负债 17.换手率 18.成交量 19.一致预测净利润2年复合增长率  20.  同比增长率

class style_fac(object):
    def __init__(self,data,index):
        self.data = data
        self.index = index
    ##存各指数价格，上证指数为0，沪深300为1，中证500为2，中证800为3，中证1000为4

###1
    def bigsize(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Size\\bigsize.csv")
        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end = len(self.data)
        for i in range(start,end):
######################################################
            cap = self.data.iloc[i,:,7]
            size = cap.map(math.log)
            temp.loc[self.data.items.values[i],:] = size

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Size\\bigsize.csv")
###2
    def medsize(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Size\\medsize.csv")
        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end = len(self.data)
        for i in range(start, end):
            cap = self.data.iloc[i, :, 7]
            size = cap ** 3
            temp.loc[self.data.items.values[i],:] = size

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Size\\medsize.csv")
###3
    def high_low(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Volatility\\hml.csv")
        temp_h = (self.data.iloc[:,:,4]).T
        temp_l = (self.data.iloc[:,:,6]).T
        temp_c = (self.data.iloc[:,:,2]).T
        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end  = len(self.data)
        for i in range(start,end):
            a = temp_h.iloc[i-20:i,:]/temp_c.iloc[i-21:i-1,:]
            b = temp_l.iloc[i-20:i,:]/temp_c.iloc[i-21:i-1,:]
            temp.loc[self.data.items.values[i],:] = (a.std() - b.std())

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Volatility\\hml.csv")
###4
    def retv(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Volatility\\retv.csv")
        temp_r = (self.data.iloc[:,:,9]).T
        date = temp.columns.values[-1]
        start = self.data.items.get_loc[date] + 1
        end = len(self.data)
        for i in range(start,end):
            a = temp_r.iloc[i-20:i,:]
            temp.loc[self.data.items.values[i], :] = a.std()

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Volatility\\retv.csv")
###5
    def turn(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Turn\\turn.csv")
        temp_t = (self.data.iloc[:,:,16]).T
        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end = len(self.data)
        for i in range(start,end):
            a = temp_t.iloc[i-20:i,:]
            temp.loc[self.data.items.values[i], :] = a.std()

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Turn\\turn.csv")
###6
    def wgt_rt(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Momentum\\wgt_rt.csv")
        temp_r = (self.data.iloc[:,:,9]).T
        temp_t = (self.data.iloc[:,:,16]).T
        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end = len(self.data)
        for i in range(start,end):
            a = temp_t.iloc[i-20:i,:]
            b = temp_r.iloc[i-20:i,:]
            c = (a * b).mean()
            temp.loc[self.data.items.values[i], :] = c

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Momentum\\wgt_rt.csv")
###7
    def halpha(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Momentum\\halpha.csv")
        temp_r = self.data.iloc[:,:,9]
        temp50 = self.index.iloc[:,0]
        def regress(ser):
            start = temp50.items.get_iloc[ser.index.values[0]]
            end = temp50.items.get_iloc[ser.index.values[-1]]
            y = (temp50.iloc[start:end]).values.tolist
            ser = ser.values
            if (len(ser)):
                x = sm.add_constant(ser)
                fit = sm.OLS(y,x.astype(float)).fit()
                alpha = fit.params[0]
                return alpha
            else:
                return 0

        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end = len(self.data)
        for i in range(start, end):
            a = temp_r[i-240:i,:]
            b = a.apply(regress(axis=1))
            temp.loc[self.data.items.values[i], :] = b

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Momentum\\halpha.csv")
###8
    def vol(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\TA\\vol.csv")
        temp_v = (self.data.iloc[:, :, 17]).T
        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end = len(self.data)
        for i in range(start,end):
            a = temp_v.iloc[i-20:i,:]
            temp.loc[self.data.items.values[i], :] = a.std()

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\TA\\vol.csv")
###9
    def CAGR(self):
        temp = (self.data.iloc[:,:,18]).T
        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Growth\\CAGR.csv")
###10
    def ROE(self):
        temp = (self.data.iloc[:,:,11]).T
        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Growth\\ROE.csv")
###11
    def topstock(self):
        temp = (self.data.iloc[:,:,10]).T
        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\value\\topstock.csv")
###12
    def increase(self):
        temp = (self.data.iloc[:,:,19]).T
        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Growth\\increase.csv")
###13
    def EY(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\EY\\EY.csv")
        temp_e = (self.data.iloc[:,:,11]).T
        temp_f = (self.data.iloc[:,:,3]).T
        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end = len(self.data)
        for i in range(start, end):
            temp.loc[self.data.items.values[i], :] = temp_e.iloc[i,:]/temp_f.iloc[i,:]

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\EY\\EY.csv")
###14
    def MLEV(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Leverage\\MLEV.csv")
        temp_me = (self.data.iloc[:, :, 14]).T
        temp_ld = (self.data.iloc[:, :, 15]).T
        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end = len(self.data)
        for i in range(start, end):
            temp.loc[self.data.items.values[i], :] = (temp_me.iloc[i,:] + temp_ld.iloc[i,:]) / (temp_me.iloc[i,:]).astype(float)

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Leverage\\MLEV.csv")
###15
    def DTOA(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Leverage\\DTOA.csv")
        temp_td = (self.data.iloc[:, :, 13]).T
        temp_ta = (self.data.iloc[:, :, 14]).T
        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end = len(self.data)
        for i in range(start, end):
            temp.loc[self.data.items.values[i], :] = temp_td.iloc[i,:] / (temp_ta.iloc[i,:]).astype(float)

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Leverage\\DTOA.csv")
###16
    def BLEV(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Leverage\\BLEV.csv")
        temp_be = (self.data.iloc[:, :, 12]).T
        temp_ld = (self.data.iloc[:, :, 15]).T
        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end = len(self.data)
        for i in range(start, end):
            temp.loc[self.data.items.values[i], :] = (temp_be.iloc[i,:] + temp_ld.iloc[i,:]) / (temp_be.iloc[i,:]).astype(float
                                                                                                                          )

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Leverage\\BLEV.csv")
###17
    def B300(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Beta\\B300.csv")
        temp300 = self.index.iloc[:,1]
        temp_r = self.data.iloc[:,:,9]
        temp_r = temp_r.ewm(halflife=63).mean()
        temp300 = temp300.ewm(halflife=63).mean()
        def regress(ser):
            start = temp300.items.get_iloc[ser.index.values[0]]
            end = temp300.items.get_iloc[ser.index.values[-1]]
            x = (temp300.iloc[start:end]).values.tolist
            ser = ser.values
            if (len(ser)):
                x = sm.add_constant(x)
                fit = sm.OLS(ser,x.astype(float)).fit()
                beta = fit.params[1]
                return beta
            else:
                return 0

        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end = len(self.data)
        for i in range(start, end):
            a = temp_r[i-252:i,:]
            b = a.apply(regress(axis=1))
            temp.loc[self.data.items.values[i], :] = b

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Beta\\B300")
###18
    def B500(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Beta\\B500.csv")
        temp500 = self.index.iloc[:,1]
        temp_r = self.data.iloc[:,:,9]
        temp_r = temp_r.ewm(halflife=63).mean()
        temp500 = temp500.ewm(halflife=63).mean()
        def regress(ser):
            start = temp500.items.get_iloc[ser.index.values[0]]
            end = temp500.items.get_iloc[ser.index.values[-1]]
            x = (temp500.iloc[start:end]).values.tolist
            ser = ser.values
            if (len(ser)):
                x = sm.add_constant(x)
                fit = sm.OLS(ser,x.astype(float)).fit()
                beta = fit.params[1]
                return beta
            else:
                return 0

        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end = len(self.data)
        for i in range(start, end):
            a = temp_r[i-252:i,:]
            b = a.apply(regress(axis=1))
            temp.loc[self.data.items.values[i], :] = b

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Beta\\B500")
###19
    def B800(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Beta\\B800.csv")
        temp800 = self.index.iloc[:,1]
        temp_r = self.data.iloc[:,:,9]
        temp_r = temp_r.ewm(halflife=63).mean()
        temp800 = temp800.ewm(halflife=63).mean()
        def regress(ser):
            start = temp800.items.get_iloc[ser.index.values[0]]
            end = temp800.items.get_iloc[ser.index.values[-1]]
            x = (temp800.iloc[start:end]).values.tolist
            ser = ser.values
            if (len(ser)):
                x = sm.add_constant(x)
                fit = sm.OLS(ser,x.astype(float)).fit()
                beta = fit.params[1]
                return beta
            else:
                return 0

        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end = len(self.data)
        for i in range(start, end):
            a = temp_r[i-252:i,:]
            b = a.apply(regress(axis=1))
            temp.loc[self.data.items.values[i], :] = b

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Beta\\B800")
###20
    def B1000(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Beta\\B1000.csv")
        temp1000 = self.index.iloc[:,1]
        temp_r = self.data.iloc[:,:,9]
        temp_r = temp_r.ewm(halflife=63).mean()
        temp1000 = temp1000.ewm(halflife=63).mean()
        def regress(ser):
            start = temp1000.items.get_iloc[ser.index.values[0]]
            end = temp1000.items.get_iloc[ser.index.values[-1]]
            x = (temp1000.iloc[start:end]).values.tolist
            ser = ser.values
            if (len(ser)):
                x = sm.add_constant(x)
                fit = sm.OLS(ser,x.astype(float)).fit()
                beta = fit.params[1]
                return beta
            else:
                return 0

        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end = len(self.data)
        for i in range(start, end):
            a = temp_r[i-252:i,:]
            b = a.apply(regress(axis=1))
            temp.loc[self.data.items.values[i], :] = b

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Beta\\B1000")
###21
    def R300(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Residual\\R300.csv")
        temp300 = self.index.iloc[:,1]
        temp_r = self.data.iloc[:,:,9]
        temp_r = temp_r.ewm(halflife=63).mean()
        temp300 = temp300.ewm(halflife=63).mean()
        def regress(ser):
            start = temp300.items.get_iloc[ser.index.values[0]]
            end = temp300.items.get_iloc[ser.index.values[-1]]
            x = (temp300.iloc[start:end]).values.tolist
            ser = ser.values
            if (len(ser)):
                x = sm.add_constant(x)
                fit = sm.OLS(ser,x.astype(float)).fit()
                resid = fit.resid
                resid = resid.std()
                return resid
            else:
                return 0

        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end = len(self.data)
        for i in range(start, end):
            a = temp_r[i-252:i,:]
            b = a.apply(regress(axis=1))
            temp.loc[self.data.items.values[i], :] = b

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Residual\\R300")
###22
    def R500(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Residual\\R500.csv")
        temp500 = self.index.iloc[:,1]
        temp_r = self.data.iloc[:,:,9]
        temp_r = temp_r.ewm(halflife=63).mean()
        temp500 = temp500.ewm(halflife=63).mean()
        def regress(ser):
            start = temp500.items.get_iloc[ser.index.values[0]]
            end = temp500.items.get_iloc[ser.index.values[-1]]
            x = (temp500.iloc[start:end]).values.tolist
            ser = ser.values
            if (len(ser)):
                x = sm.add_constant(x)
                fit = sm.OLS(ser,x.astype(float)).fit()
                resid = fit.resid
                resid = resid.std()
                return resid
            else:
                return 0

        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end = len(self.data)
        for i in range(start, end):
            a = temp_r[i-252:i,:]
            b = a.apply(regress(axis=1))
            temp.loc[self.data.items.values[i], :] = b

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Residual\\R500")
###23
    def R800(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Residual\\R800.csv")
        temp800 = self.index.iloc[:,1]
        temp_r = self.data.iloc[:,:,9]
        temp_r = temp_r.ewm(halflife=63).mean()
        temp800 = temp800.ewm(halflife=63).mean()
        def regress(ser):
            start = temp800.items.get_iloc[ser.index.values[0]]
            end = temp800.items.get_iloc[ser.index.values[-1]]
            x = (temp800.iloc[start:end]).values.tolist
            ser = ser.values
            if (len(ser)):
                x = sm.add_constant(x)
                fit = sm.OLS(ser,x.astype(float)).fit()
                resid = fit.resid
                resid = resid.std()
                return resid
            else:
                return 0

        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end = len(self.data)
        for i in range(start, end):
            a = temp_r[i-252:i,:]
            b = a.apply(regress(axis=1))
            temp.loc[self.data.items.values[i], :] = b

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Residual\\R800")
###24
    def R1000(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Residual\\R1000.csv")
        temp1000 = self.index.iloc[:,1]
        temp_r = self.data.iloc[:,:,9]
        temp_r = temp_r.ewm(halflife=63).mean()
        temp1000 = temp1000.ewm(halflife=63).mean()
        def regress(ser):
            start = temp1000.items.get_iloc[ser.index.values[0]]
            end = temp1000.items.get_iloc[ser.index.values[-1]]
            x = (temp1000.iloc[start:end]).values.tolist
            ser = ser.values
            if (len(ser)):
                x = sm.add_constant(x)
                fit = sm.OLS(ser,x.astype(float)).fit()
                resid = fit.resid
                resid = resid.std()
                return resid
            else:
                return 0

        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end = len(self.data)
        for i in range(start, end):
            a = temp_r[i-252:i,:]
            b = a.apply(regress(axis=1))
            temp.loc[self.data.items.values[i], :] = b

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Residual\\R1000")
###25
    def ASI(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Tech\\ASI.csv")
        temp_h = (self.data.iloc[:,:,4]).T
        temp_l = (self.data.iloc[:,:,6]).T
        temp_c = (self.data.iloc[:,:,2]).T
        temp_o = (self.data.iloc[:,:,8]).T
        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end  = len(self.data)
        for i in range(start,end):
            DHP = temp_h.iloc[i-20:i,:]
            REFDCloP = temp_c.iloc[i-21:i-1,:]
            DLP = temp_l.iloc[i-20:i,:]
            REFDLP = temp_l.iloc[i-21:i-1,:]
            REFDOpenP = temp_o.iloc[i-21:i-1,:]
            DCloP = temp_c.iloc[i-20:i,:]
            DOpenP = temp_o.iloc[i-20:i,:]
            REFDCloP.index = DCloP.index
            REFDOpenP.index =DOpenP.index
            REFDLP.index = DLP.index
            aa = abs(DHP - REFDCloP)
            bb = abs(DLP - REFDCloP)
            cc = abs(DHP - REFDLP)
            dd = abs(REFDCloP - REFDOpenP)
            r = cc + dd * 0.25
            r[(aa > bb) & (aa > cc)] = aa + bb * 0.5 + dd * 0.25
            r[(bb > cc) & (bb > aa)] = bb + aa * 0.5 + dd * 0.25
            x = DCloP * 1.5 - DOpenP * 0.5 - REFDOpenP
            aa[aa < bb] = bb
            si = 16 * x * aa / r
            asi = si.sum()
            temp.loc[self.data.items.values[i],:] = asi

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Tech\\ASI.csv")
###26
    def DDI(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Tech\\DDI.csv")
        temp_h = (self.data.iloc[:,:,4]).T
        temp_l = (self.data.iloc[:,:,6]).T
        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end  = len(self.data)
        for i in range(start,end):
            DHP = temp_h.iloc[i-20:i,:]
            REFDHP = temp_h.iloc[i-21:i-1,:]
            DLP = temp_l.iloc[i-20:i,:]
            REFDLP = temp_l.iloc[i-21:i-1,:]
            REFDLP.index = DLP.index
            REFDHP.index = DHP.index
            df1 = abs(DHP - REFDHP)
            df2 = abs(DLP - REFDLP)
            df1[df1 < df2] = df2
            DMZ=df1.copy()
            DMF=df2.copy()
            DMZ[(DHP+DLP<REFDHP+REFDLP)] = 0
            DMF[(DHP+DLP>=REFDHP+REFDLP)] = 0
            x1 = DMZ.mean()
            x2 = DMF.mean()
            DIZ = x1/(x1+x2)
            DIF = x2/(x1+x2)
            ddi = DIZ-DIF
            temp.loc[self.data.items.values[i],:] = ddi

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Tech\\DDI.csv")
###27
    def Hurst(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Tech\\Hurst.csv")
        temp_c = (self.data.iloc[:,:,2]).T
        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end  = len(self.data)
        for i in range(start,end):
            DCloP = temp_c.iloc[i-40:i,:]
            m = pd.rolling_mean(DCloP,5,min_periods=1)
            y = DCloP - m
            z = y.cumsum()
            r = z.max() - z.min()
            s = DCloP.std()
            hurst = r/s
            temp.loc[self.data.items.values[i],:] = hurst

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Tech\\Hurst.csv")
###28
##########P1,P2默认值为3#############
    def KDJ(self,P1,P2):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Tech\\KDJ.csv")
        temp_c = (self.data.iloc[:,:,2]).T
        temp_h = (self.data.iloc[:,:,4]).T
        temp_l = (self.data.iloc[:,:,6]).T
        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end  = len(self.data)
        for i in range(start,end):
            DCloP = temp_c.iloc[i-40:i,:]
            DLP = temp_l.iloc[i-40:i,:]
            DHP = temp_h.iloc[i - 40:i, :]
            lv = pd.rolling_min(DLP,5,1)
            hv = pd.rolling_max(DHP,5,1)
            rsv = 100*(DCloP-lv)/(hv-lv)
            k1 = (rsv.iloc[len(rsv)-2,:]*(P1-1) + rsv.iloc[len(rsv)-1,:])/P1
            k2 = (rsv.iloc[len(rsv)-3,:]*(P1-1) + rsv.iloc[len(rsv)-2,:])/P1
            d = k2*(P2-1)+k1/P2
            j = k1 * 3 - d * 2
            temp.loc[self.data.items.values[i],:] = j

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Tech\\KDJ.csv")
###29
    def MFI(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Tech\\MFI.csv")
        temp_c = (self.data.iloc[:,:,2]).T
        temp_h = (self.data.iloc[:,:,4]).T
        temp_l = (self.data.iloc[:,:,6]).T
        temp_v = (self.data.iloc[:,:,17]).T
        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end  = len(self.data)
        for i in range(start,end):
            DCloP = temp_c.iloc[i-30:i,:]
            DHP = temp_h.iloc[i - 30:i, :]
            DLP = temp_l.iloc[i - 30:i, :]
            DVol = temp_v.iloc[i - 30:i, :]
            REFDCloP = temp_c.iloc[i - 31:i-1, :]
            REFDHP = temp_h.iloc[i - 31:i-1, :]
            REFDLP = temp_l.iloc[i - 31:i-1, :]
            REFDCloP.index = DCloP.index
            REFDHP.index = DHP.index
            REFDLP.index = DLP.index
            typ = (DCloP+DHP+DLP)/3
            reftyp = (REFDCloP+REFDHP+REFDLP)/3
            typ1 = typ*DVol
            typ2 = typ1.copy()
            typ1[typ <= reftyp] = 0
            typ2[typ >= reftyp] = 0
            x1 = pd.rolling_mean(typ1, 10, min_periods=1)
            x2 = pd.rolling_mean(typ2, 10, min_periods=1)
            x1 = x1.iloc[-1,:]
            x2 = x2.iloc[-1,:]
            v1 = x1/x2
            mfi = 100-(100/(1+v1))
            temp.loc[self.data.items.values[i],:] = mfi

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Tech\\MFI.csv")
###30
    def Ulcer(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Tech\\Ulcer.csv")
        def likevar(ser):
            ser = ser.astype(float)
            ser2 = ser.copy()
            ind = ser.index
            for i in range(len(ind)):
                ser1 = ser[ind[0]:ind[i]]
                ser2[ind[i]] = ((ser1 ** 2).sum() / (i + 1)) ** 0.5
            return ser2
        temp_c = (self.data.iloc[:,:,2]).T
        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end  = len(self.data)
        for i in range(start,end):
            DCloP = temp_c.iloc[i-20,:]
            mp = DCloP.max()
            ri = 100 * (DCloP-mp)/mp
            ulcer = likevar(ri)
            temp.loc[self.data.items.values[i],:] = ulcer

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Tech\\Ulcer.csv")
###31
    def BR(self):
        temp = pd.read_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Tech\\BR.csv")
        temp_c = (self.data.iloc[:, :, 2]).T
        temp_h = (self.data.iloc[:,:,4]).T
        temp_l = (self.data.iloc[:,:,6]).T
        date = temp.index.values[-1]
        start = self.data.items.get_loc[date] + 1
        end  = len(self.data)
        for i in range(start,end):
            DHP = temp_h.iloc[i-10:i,:]
            DLP = temp_l.iloc[i-10:i,:]
            REFDCloP = temp_c.iloc[i-11:i-1,:]
            REFDCloP.index = DLP.index
            df1 = (DHP - REFDCloP)
            df1[df1<0]=0
            df2 = (REFDCloP-DLP)
            df2[df2<0]=0
            x1 = pd.rolling_sum(df1,5,min_periods=1)
            x2 = pd.rolling_sum(df2, 5, min_periods=1)
            y = x1/x2
            br = y.iloc[-1,:]
            temp.loc[self.data.items.values[i],:] = br

        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Tech\\BR.csv")
###B50
    def B50(self):
        temp = (self.data.iloc[:,:,1]).T
        temp.to_csv(r"C:\\Dell\\internship\\CICC\\Barra\\Database\\Beta\\B50csv")
###industry
    def industry(self):
        refe = pd.read_excel(r"C:\DELL\internship\CICC\Trans\industry\industryZX.xlsx", index_col=1)
        temp_i = self.data[:,:,5]
        for ind in refe.index:
            name = "C://DELL//internship//CICC//Trans//industry//" + refe.loc[ind, "中信一级"]
            wind = refe.loc[ind,"WIND代码"]
            temp = pd.read_pickle(name)
            temp = temp.T
            date = temp.index.values[-1]
            start = self.data.items.get_loc[date] + 1
            end = len(self.data)
            for i in range(start,end):
                ser = temp_i.iloc[i,:]
                ind = pd.Series()
                ind[ind!=wind]=0
                ind[ind==wind]=1
                temp.loc[self.data.items.values[i], :] = ind
            temp.to_pickle(name)
###netrt
###met-return
###将各股收益率存入表中
    def netrt(self):
        temp = self.data.iloc[:, :, 9]
        temp.to_csv(r"C:\\Dell\\internship\\Barra\\Database\\Return\\Ret.csv")
