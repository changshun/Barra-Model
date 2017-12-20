import numpy as np
import pandas as pd
import datetime as dt
from datetime import timedelta
import statsmodels.api as sm
import scipy.stats.mstats as ssm

class regress(object):
    def __init__(self,today,data,hold,tot_ret):
        self.today = today
        self.data = data
        self.tot_ret = tot_ret
        self.hold = hold

        ###########win1默认为2天，win2默认为8天

    def date_win(self, win1, win2):
        self.cap = self.data.iloc[:, :, 4]
        date_list = []
        for x in self.ret.columns:
            if x in self.cap.columns:
                data_list.append(x)
            else:
                pass
        spec_date1 = self.today - timedelta(days=win1)
        spec_date2 = self.today - timedelta(days=win2)
        date_list_temp1 = [abs(spec_date1 - x) for x in date_list]
        temp = date_list_temp1.index(min(date_list_temp1))
        self.date1 = date_list[temp]
        date_list_temp2 = [abs(spec_date2 - x) for x in date_list]
        temp = date_list_temp2.index(min(date_list_temp2))
        self.date2 = date_list[temp]

    def pre(self,low_limit,up_limit):
        self.bigsize = pd.read_csv(r"C:\\Dell\\internship\\Barra\\Database\\Size\\bigsize")
        self.medsize = pd.read_csv(r"C:\\Dell\\internship\\Barra\\Database\\Size\\medsize")
        self.retv = pd.read_csv(r"C:\\Dell\\internship\\Barra\\Database\\Volatility\\retv")
        self.turn = pd.read_csv(r"C:\\Dell\\internship\\Barra\\Database\\Turn\\turn")
        self.wgt_rt = pd.read_csv(r"C:\\Dell\\internship\\Barra\\Database\\Momentum\\wgt_rt")
        #self.halpha = pd.read_csv(r"C:\\Dell\\internship\\Barra\\Database\\Momentum\\halpha")
        self.increase = pd.read_csv(r"C:\\Dell\\internship\\Barra\\Database\\Growth\\increase")
        self.EY = pd.read_csv(r"C:\\Dell\\internship\\Barra\\Database\\EY\\EY")
        self.ROE = pd.read_csv(r"C:\\Dell\\internship\\Barra\\Database\\Growth\\ROE")
        #self.BLEV = pd.read_csv(r"C:\\Dell\\internship\\Barra\\Database\\Leverage\\BLEV")
        #self.B800 =  pd.read_csv(r"C:\\Dell\\internship\\Barra\\Database\\Beta\\B800")
        #self.R800 = pd.read_csv(r"C:\\Dell\\internship\\Barra\\Database\\Residual\\R800")
        self.KDJ = pd.read_csv(r"C:\\Dell\\internship\\Barra\\Database\\Tech\\KDJ")
        #########
        self.bigsize_tr = self.bigsize.T.loc[:,self.date2:self.date2]
        self.df_bigsize = self.bigsize_tr.unstack()
        if len(self.df_bigsize):
            temp = ssm.winsorize(self.df_bigsize[self.df_bigsize.notnull()], [low_limit, up_limit])
            df_temp = pd.Series(temp.data, index=self.df_bigsize[self.df_bigsize.notnull()].index)
            self.df_bigsize = df_temp.combine_first(self.df_bigsize)
            self.df_bigsize = (self.df_bigsize - self.df_bigsize.mean()) / self.df_bigsize.std()
        else:
            pass
        self.medsize_tr = self.medsize.T.loc[:,self.date2:self.date2]
        self.df_medsize = self.medsize_tr.unstack()
        if len(self.df_medsize):
            temp = ssm.winsorize(self.df_medsize[self.df_medsize.notnull()], [low_limit, up_limit])
            df_temp = pd.Series(temp.data, index=self.df_medsize[self.df_medsize.notnull()].index)
            self.df_medsize = df_temp.combine_first(self.df_medsize)
            self.df_medsize = (self.df_medsize - self.df_medsize.mean()) / self.df_medsize.std()
        else:
            pass
        self.retv_tr = self.retv.T.loc[:,self.date1:self.date1]
        self.df_retv = self.m=retv_tr.unstack()
        if len(self.df_retv):
            temp = ssm.winsorize(self.df_retv[self.df_retv.notnull()], [low_limit, up_limit])
            df_temp = pd.Series(temp.data, index=self.df_retv[self.df_retv.notnull()].index)
            self.df_retv = df_temp.combine_first(self.df_retv)
            self.df_retv = (self.df_retv - self.df_retv.mean()) / self.df_retv.std()
        else:
            pass
        self.turn_tr = self.turn.T.loc[:,self.date1:self.date1]
        self.df_turn = self.turn_tr.unstack()
        if len(self.df_turn):
            temp = ssm.winsorize(self.df_turn[self.df_turn.notnull()], [low_limit, up_limit])
            df_temp = pd.Series(temp.data, index=self.df_turn[self.df_turn.notnull()].index)
            self.df_turn = df_temp.combine_first(self.df_turn)
            self.df_turn = (self.df_turn - self.df_turn.mean()) / self.df_turn.std()
        else:
            pass
        self.wgt_rt_tr = self.wgt_rt.T.loc[:,self.date1:self.date1]
        self.df_wgt_rt = self.wgt_rt_tr.unstack()
        if len(self.df_wgt_rt):
            temp = ssm.winsorize(self.df_wgt_rt[self.df_wgt_rt.notnull()], [low_limit, up_limit])
            df_temp = pd.Series(temp.data, index=self.df_wgt_rt[self.df_wgt_rt.notnull()].index)
            self.df_wgt_rt = df_temp.combine_first(self.df_wgt_rt)
            self.df_wgt_rt = (self.df_wgt_rt - self.df_wgt_rt.mean()) / self.df_wgt_rt.std()
        else:
            pass
        self.halpha_tr = self.halpha.T.loc[:,self.date1:self.date1]
        self.df_halpha = self.halpha_tr.unstack()
        if len(self.df_halpha):
            temp = ssm.winsorize(self.df_halpha[self.df_halpha.notnull()], [low_limit, up_limit])
            df_temp = pd.Series(temp.data, index=self.df_halpha[self.df_halpha.notnull()].index)
            self.df_halpha = df_temp.combine_first(self.df_halpha)
            self.df_halpha = (self.df_halpha - self.df_halpha.mean()) / self.df_halpha.std()
        else:
            pass
        self.increase_tr = self.increase.T.loc[:,self.date2:self.date2]
        self.df_increase = self.increase_tr.unstack()
        if len(self.df_increase):
            temp = ssm.winsorize(self.df_increase[self.df_increase.notnull()], [low_limit, up_limit])
            df_temp = pd.Series(temp.data, index=self.df_increase[self.df_increase.notnull()].index)
            self.df_increase = df_temp.combine_first(self.df_increase)
            self.df_increase = (self.df_increase - self.df_increase.mean()) / self.df_increase.std()
        else:
            pass
        self.EY_tr = self.EY.T.loc[:, self.date2:self.date2]
        self.df_EY = self.EY_tr.unstack()
        if len(self.df_EY):
            temp = ssm.winsorize(self.df_EY[self.df_EY.notnull()], [low_limit, up_limit])
            df_temp = pd.Series(temp.data, index=self.df_EY[self.df_EY.notnull()].index)
            self.df_EY = df_temp.combine_first(self.df_EY)
            self.df_EY = (self.df_EY - self.df_EY.mean()) / self.df_EY.std()
        else:
            pass
        self.ROE_tr = self.ROE.T.loc[:, self.date2:self.date2]
        self.df_ROE = self.ROE_tr.unstack()
        if len(self.df_ROE):
            temp = ssm.winsorize(self.df_ROE[self.df_ROE.notnull()], [low_limit, up_limit])
            df_temp = pd.Series(temp.data, index=self.df_ROE[self.df_ROE.notnull()].index)
            self.df_ROE = df_temp.combine_first(self.df_ROE)
            self.df_ROE = (self.df_ROE - self.df_ROE.mean()) / self.df_ROE.std()
        else:
            pass
        self.BLEV_tr = self.BLEV.T.loc[:, self.date2:self.date2]
        self.df_BLEV = self.BLEV_tr.unstack()
        if len(self.df_BLEV):
            temp = ssm.winsorize(self.df_BLEV[self.df_BLEV.notnull()], [low_limit, up_limit])
            df_temp = pd.Series(temp.data, index=self.df_BLEV[self.df_BLEV.notnull()].index)
            self.df_BLEV = df_temp.combine_first(self.df_BLEV)
            self.df_BLEV = (self.df_BLEV - self.df_BLEV.mean()) / self.df_BLEV.std()
        else:
            pass
        self.B800_tr = self.B800.T.loc[:, self.date1:self.date1]
        self.df_B800 = self.B800_tr.unstack()
        if len(self.df_B800):
            temp = ssm.winsorize(self.df_B800[self.df_B800.notnull()], [low_limit, up_limit])
            df_temp = pd.Series(temp.data, index=self.df_B800[self.df_B800.notnull()].index)
            self.df_B800 = df_temp.combine_first(self.df_B800)
            self.df_B800 = (self.df_B800 - self.df_B800.mean()) / self.df_B800.std()
        else:
            pass
        self.R800_tr = self.R800.T.loc[:, self.date1:self.date1]
        self.df_R800 = self.R800_tr.unstack()
        if len(self.df_R800):
            temp = ssm.winsorize(self.df_R800[self.df_R800.notnull()], [low_limit, up_limit])
            df_temp = pd.Series(temp.data, index=self.df_R800[self.df_R800.notnull()].index)
            self.df_R800 = df_temp.combine_first(self.df_R800)
            self.df_R800 = (self.df_R800 - self.df_R800.mean()) / self.df_R800.std()
        else:
            pass
        self.KDJ_tr = self.KDJ.T.loc[:, self.date1:self.date1]
        self.df_KDJ = self.KDJ_tr.unstack()
        if len(self.df_KDJ):
            temp = ssm.winsorize(self.df_KDJ[self.df_KDJ.notnull()], [low_limit, up_limit])
            df_temp = pd.Series(temp.data, index=self.df_KDJ[self.df_KDJ.notnull()].index)
            self.df_KDJ = df_temp.combine_first(self.df_KDJ)
            self.df_KDJ = (self.df_KDJ - self.df_KDJ.mean()) / self.df_KDJ.std()
        else:
            pass

    def industry(self):
        self.Industry = []
        refe = pd.read_excel(r"C:\DELL\internship\CICC\Trans\industry\industryZX.xlsx", index_col=1)
        for ind in refe.index:
            name = "C://DELL//internship//CICC//Trans//industry//" + refe.loc[ind, "中信一级"]
            df = pd.read_pickle(name)
            df.index.name = refe.loc[ind, "中信一级"]
            df_tr = df.loc[:, self.date:self.date]
            df_tr = df_tr.unstack()
            self.Industry.append(df_tr)

    def factor_ret(self):
        weight = self.cap ** 0.5
        weight = 1/weight
        weight_tr = weight.loc[:, self.today:self.today]
        df_weight = weight_tr.unstack()
        self.rtn = []
        self.pct = []
        self.expos = []
        ret_tr = self.data.iloc[self.today:self.today,:,6]
        self.df_ret = ret_tr.unstack()
        self.tot_ret = self.ret.loc["ret_pct",self.today]

        if (len(ret_tr)) and len(self.bigsize) and len(self.medsize) \
                and len(self.retv) and len(self.turn) and len(self.wgt_rt) \
                and len(self.halpha) and len(self.increase) and len(self.EY) \
                and len(self.ROE) and len(self.BLEV) and len(self.B800) \
                and len(self.R800) and len(self.KDJ):
            df_regression = pd.DataFrame([self.df_ret.values,self.df_bigsize.values,
                                          self.df_medsize.values,self.df_retv.values,
                                          self.df_turn.values,self.df_wgt_rt.values,
                                          self.df_halpha.values,self.df_increase.values,
                                          self.df_EY.values,self.df_ROE.values,self.df_BLEV.values,
                                          self.df_B800.values,self.df_R800.values,self.df_KDJ.values],index=['ret','bigsize',
                                         'medsize','retv','turn','wgt_rt','halpha','increase','EY','ROE','BLEV','B800','R800','KDJ'])
            df_regression = df_regression.T
            for i in range(0, len(self.Industry)):
                df_regression[self.Industry[i].unstack().T.index.name] = self.Industry[i].values
            df_regression['weight'] = df_weight.values
            df_regression = df_regression.dropna()
            y = df_regression.iloc[:, 0].tolist()
            temp = []
            for i in range(1, df_regression.shape[1] - 1):
                temp.append(df_regression.iloc[:, i].tolist())
            X = np.column_stack(temp)
            W = df_regression.iloc[:, -1].tolist()
            fit = sm.WLS(y, X, weight=W).fit()
            self.pfl_W = self.hold.iloc[:,self.today:self.today]
            if (self.pfl_W.empty == False):
                exp_bigsize = np.dot(self.pfl_W.iloc[:, 0].values,self.df_bigsize.fillna(0).values)
                ret_bigsize = exp_bigsize * fit.params[0]
                pct_bigsize = ret_bigsize/self.tot_ret
                self.rtn.append(ret_bigsize)
                self.pct.append(pct_bigsize)
                self.expos.append(exp_bigsize)

                exp_medsize = np.dot(self.pfl_W.iloc[:, 0].values,self.df_medsize.fillna(0).values)
                ret_medsize = exp_medsize * fit.params[1]
                pct_medsize = ret_medsize/self.tot_ret
                self.rtn.append(ret_medsize)
                self.pct.append(pct_medsize)
                self.expos.append(exp_medsize)

                exp_retv = np.dot(self.pfl_W.iloc[:, 0].values,self.df_retv.fillna(0).values)
                ret_retv = exp_retv * fit.params[2]
                pct_retv = ret_retv/self.tot_ret
                self.rtn.append(ret_retv)
                self.pct.append(pct_retv)
                self.expos.append(exp_retv)

                exp_turn = np.dot(self.pfl_W.iloc[:, 0].values,self.df_turn.fillna(0).values)
                ret_turn = exp_turn * fit.params[3]
                pct_turn = ret_turn/self.tot_ret
                self.rtn.append(ret_turn)
                self.pct.append(pct_turn)
                self.expos.append(exp_turn)

                exp_wgt_rt = np.dot(self.pfl_W.iloc[:, 0].values,self.df_wgt_rt.fillna(0).values)
                ret_wgt_rt = exp_wgt_rt * fit.params[4]
                pct_wgt_rt = ret_wgt_rt/self.tot_ret
                self.rtn.append(ret_wgt_rt)
                self.pct.append(pct_wgt_rt)
                self.expos.append(exp_wgt_rt)

                exp_halpha = np.dot(self.pfl_W.iloc[:, 0].values,self.df_halpha.fillna(0).values)
                ret_halpha = exp_halpha * fit.params[5]
                pct_halpha = ret_halpha/self.tot_ret
                self.rtn.append(ret_halpha)
                self.pct.append(pct_halpha)
                self.expos.append(exp_halpha)

                exp_increase = np.dot(self.pfl_W.iloc[:, 0].values,self.df_increase.fillna(0).values)
                ret_increase = exp_increase * fit.params[6]
                pct_increase = ret_increase/self.tot_ret
                self.rtn.append(ret_increase)
                self.pct.append(pct_increase)
                self.expos.append(exp_increase)

                exp_EY = np.dot(self.pfl_W.iloc[:, 0].values,self.df_EY.fillna(0).values)
                ret_EY = exp_EY * fit.params[7]
                pct_EY = ret_EY/self.tot_ret
                self.rtn.append(ret_EY)
                self.pct.append(pct_EY)
                self.expos.append(exp_EY)

                exp_ROE = np.dot(self.pfl_W.iloc[:, 0].values, self.df_ROE.fillna(0).values)
                ret_ROE = exp_ROE * fit.params[8]
                pct_ROE = ret_ROE / self.tot_ret
                self.rtn.append(ret_ROE)
                self.pct.append(pct_ROE)
                self.expos.append(exp_ROE)

                exp_BLEV = np.dot(self.pfl_W.iloc[:, 0].values, self.df_BLEV.fillna(0).values)
                ret_BLEV = exp_BLEV * fit.params[9]
                pct_BLEV = ret_BLEV / self.tot_ret
                self.rtn.append(ret_BLEV)
                self.pct.append(pct_BLEV)
                self.expos.append(exp_BLEV)

                exp_B800 = np.dot(self.pfl_W.iloc[:, 0].values, self.df_B800.fillna(0).values)
                ret_B800 = exp_B800 * fit.params[10]
                pct_B800 = ret_B800 / self.tot_ret
                self.rtn.append(ret_B800)
                self.pct.append(pct_B800)
                self.expos.append(exp_B800)

                exp_R800 = np.dot(self.pfl_W.iloc[:, 0].values, self.df_R800.fillna(0).values)
                ret_R800 = exp_R800 * fit.params[11]
                pct_R800 = ret_R800 / self.tot_ret
                self.rtn.append(ret_R800)
                self.pct.append(pct_R800)
                self.expos.append(exp_R800)

                exp_KDJ = np.dot(self.pfl_W.iloc[:, 0].values, self.df_KDJ.fillna(0).values)
                ret_KDJ = exp_KDJ * fit.params[12]
                pct_KDJ = ret_KDJ / self.tot_ret
                self.rtn.append(ret_KDJ)
                self.pct.append(pct_KDJ)
                self.expos.append(exp_KDJ)

                for i in range(0, len(self.Industry)):
                    exp_tr = np.dot(self.pfl_W.iloc[:, 0].values, self.Industry[i].fillna(0).values)
                    ret_tr = exp_tr * fit.params[i + 13]
                    pct_tr = ret_tr/self.tot_ret
                    self.rtn.append(ret_tr)
                    self.pct.append(pct_tr)
                    self.expos.append(exp_tr)

                self.result = pd.read_excel(r"C:\DELL\internship\CICC\Trans\result\rtn.xlsx", sheetname=0,
                                            index_col=0)
                self.percentage = pd.read_excel(r"C:\DELL\internship\CICC\Trans\result\pct.xlsx", sheetname=0,
                                                index_col=0)
                self.exposure = pd.read_excel(r"C:\DELL\internship\CICC\Trans\result\expos.xlsx", sheetname=0,
                                              index_col=0)

                self.result[format(self.today, "%Y-%m-%d")] = self.rtn
                self.result.to_excel(r"C:\DELL\internship\CICC\Trans\result\rtn.xlsx")
                self.percentage[format(self.today, "%Y-%m-%d")] = self.pct
                self.percentage.to_excel(r"C:\DELL\internship\CICC\Trans\result\pct.xlsx")
                self.exposure[format(self.today, "%Y-%m-%d")] = self.expos
                self.exposure.to_excel(r"C:\DELL\internship\CICC\Trans\result\expos.xlsx")
            else:
                pass
        else:
            pass
