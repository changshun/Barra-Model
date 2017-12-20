# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prototype.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
from PyQt5.QtCore import pyqtSlot

matplotlib.use("Qt5Agg")  # 声明使用QT5

class Ui_MainWindow(object):
    def __init__(self):
        self.path = r'C:\DELL\internship\CICC\Barra\Presentation'
        self.df_exp = pd.read_excel(self.path + r'\expos2.xlsx')
        self.df_rtn = pd.read_excel(self.path + r'\rtn2.xlsx')
        self.df_rtn.set_index('factor', inplace=True)
        self.df_rtn = self.df_rtn.sort_index(axis=1)
        self.df_pct = pd.read_excel(self.path + r'\pct2.xlsx')
        self.df_pct.set_index('factor', inplace=True)
        self.df_pct = self.df_pct.sort_index(axis=1)
        self.df_win = pd.read_excel(self.path + r'\pct5win40.xlsx')
        self.df_win.set_index('factor', inplace=True)
        self.df_win = self.df_win.sort_index(axis=1)

        self.factor_list = self.df_exp['factor']# 因子名单
        self.input_factor_text = '' # 选择的因子
    def setupUi(self, MainWindow):
        plt.style.use('ggplot')
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(841, 587)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(350, 10, 201, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setObjectName("title")

        # 更新行情按钮
        self.update_market = QtWidgets.QPushButton(self.centralwidget)
        self.update_market.setGeometry(QtCore.QRect(40, 60, 75, 23))
        self.update_market.setObjectName("update_market")
        self.update_market.clicked.connect(self.MarketProgress)
        # 更新行情进度条
        self.market_progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.market_progressBar.setGeometry(QtCore.QRect(150, 60, 361, 23))
        self.market_progressBar.setProperty("value", 0)
        self.market_progressBar.setObjectName("market_progressBar")
        # 更新因子按钮
        self.update_factor = QtWidgets.QPushButton(self.centralwidget)
        self.update_factor.setGeometry(QtCore.QRect(40, 100, 75, 23))
        self.update_factor.setObjectName("update_factor")
        self.update_factor.clicked.connect(self.FactorProgress)
        # 更新因子进度条
        self.factor_progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.factor_progressBar.setGeometry(QtCore.QRect(150, 100, 361, 23))
        self.factor_progressBar.setProperty("value", 0)
        self.factor_progressBar.setObjectName("factor_progressBar")

        # 因子名称
        self.factor_name = QtWidgets.QLabel(self.centralwidget)
        self.factor_name.setGeometry(QtCore.QRect(570, 60, 81, 41))
        self.factor_name.setObjectName("factor_name")

        # 导入按钮
        self.import_from = QtWidgets.QPushButton(self.centralwidget)
        self.import_from.setGeometry(QtCore.QRect(10, 340, 75, 23))
        self.import_from.setObjectName("import_from")
        self.import_from.clicked.connect(self.ImportFile)

        self.factor_input_label = QtWidgets.QLabel(self.centralwidget)
        self.factor_input_label.setGeometry(QtCore.QRect(10, 380, 71, 21))
        self.factor_input_label.setObjectName("factor_input_label")

        self.input_factor = QtWidgets.QComboBox(self.centralwidget)
        self.input_factor.setGeometry(QtCore.QRect(2, 400, 96, 22))
        self.input_factor.setObjectName("comboBox")
        self.input_factor.addItems(self.factor_list)

        # 归因按钮
        self.attribute = QtWidgets.QPushButton(self.centralwidget)
        self.attribute.setGeometry(QtCore.QRect(10, 440, 75, 23))
        self.attribute.setObjectName("attribute")
        self.attribute.clicked.connect(self.AttributeTo)

        # 可变区域，存放图表
        self.figure = QtWidgets.QTabWidget(self.centralwidget)
        self.figure.setGeometry(QtCore.QRect(120, 150, 701, 391))
        self.figure.setObjectName("figure")

        self.exposure_style_name = QtWidgets.QWidget()
        self.exposure_style_name.setObjectName("exposure_style_name")
        self.exposure_style = QtWidgets.QGraphicsView(self.exposure_style_name)
        self.exposure_style.setGeometry(QtCore.QRect(0, 0, 701, 371))
        self.exposure_style.setObjectName("exposure_style")
        self.figure.addTab(self.exposure_style_name, "风格因子风险敞口")

        self.exposure_industry_name = QtWidgets.QWidget()
        self.exposure_industry_name.setObjectName("exposure_industry_name")
        self.exposure_industry = QtWidgets.QGraphicsView(self.exposure_industry_name)
        self.exposure_industry.setGeometry(QtCore.QRect(0, 0, 701, 371))
        self.exposure_industry.setObjectName("exposure_industry")
        self.figure.addTab(self.exposure_industry, "行业因子风险敞口")

        self.accumulate_name = QtWidgets.QWidget()
        self.accumulate_name.setObjectName("accumulate_name")
        self.accumulate = QtWidgets.QGraphicsView(self.accumulate_name)
        self.accumulate.setGeometry(QtCore.QRect(0, 0, 701, 371))
        self.accumulate.setObjectName("accumulate")
        self.figure.addTab(self.accumulate, "因子贡献累计")

        self.factor_plot_name = QtWidgets.QWidget()
        self.factor_plot_name.setObjectName("factor_plot_name")
        self.factor_plot = QtWidgets.QGraphicsView(self.factor_plot_name)
        self.factor_plot.setGeometry(QtCore.QRect(0, 0, 701, 371))
        self.factor_plot.setObjectName("factor_plot")
        self.figure.addTab(self.factor_plot, "因子贡献曲线")

        # 5 win图
        self.factor_win_name = QtWidgets.QWidget()
        self.factor_win_name.setObjectName("factor_win_name")
        self.factor_win = QtWidgets.QGraphicsView(self.factor_win_name)
        self.factor_win.setGeometry(QtCore.QRect(0, 0, 701, 371))
        self.factor_win.setObjectName("factor_win")
        self.figure.addTab(self.factor_win, "因子贡献win")


        # 表

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 841, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.update_market.setText(_translate("MainWindow", "更新行情"))
        self.title.setText(_translate("MainWindow", "BARRA"))
        self.update_factor.setText(_translate("MainWindow", "更新因子"))
        self.factor_name.setText(_translate("MainWindow", "factor"))
        self.import_from.setText(_translate("MainWindow", "导入"))
        self.factor_input_label.setText(_translate("MainWindow", "输入因子名称"))
        self.attribute.setText(_translate("MainWindow", "归因"))
        #self.figure.setTabText(self.figure.indexOf(self.exposure_style_name), _translate("MainWindow", "风格因子风险敞口"))
        #self.figure.setTabText(self.figure.indexOf(self.exposure_industry_name), _translate("MainWindow", "行业因子风险敞口"))
        #self.figure.setTabText(self.figure.indexOf(self.accumulate_name), _translate("MainWindow", "因子贡献累计"))
        #self.figure.setTabText(self.figure.indexOf(self.factor_plot_name), _translate("MainWindow", "因子贡献曲线"))
        #self.figure.setTabText(self.figure.indexOf(self.factor_win_name), _translate("MainWindow", "因子贡献win"))


        # 绘图
        self.graph_exposure_style()
        self.graph_exposure_industry()
        # 列表填值
    #-------------------------------------------按钮-------------------------------------------------------
    # 按钮导入功能
    def ImportFile(self):
        # 设置文件扩展名过滤,注意用双分号间隔
        fileName1, filetype= QFileDialog.getOpenFileName(self.centralwidget,"选取文件","C:/","All Files (*);;Text Files (*.txt)")
        print(r'你选择的文件是：%s'%fileName1)
        #self.tb(self.factor_table,fileName1)

    def AttributeTo(self):
        self.input_factor_text = self.input_factor.currentText()
        self.graph_factor_accumulate() # 画累计图
        self.graph_factor_plot() # 画曲线图
        self.graph_factor_win() # 画win图



    #@pyqtSlot()
    def test(self):
        #self.factor_name.setText("factor")
        print('hello')

    # 更新行情进度函数
    def MarketProgress(self):
        Num = 101
        for i in range(Num):
            self.market_progressBar.setValue(i)
            QtCore.QThread.msleep(100)
    # 更新因子进度函数
    def FactorProgress(self):
        Num = 101
        for i in range(Num):
            self.factor_progressBar.setValue(i)
            QtCore.QThread.msleep(100)



    def draw_exposure_style(self,dr):
        # 风格因子敞口图
        df = self.df_exp.iloc[:10,[0,-1]]
        x = range(len(df))
        label = df['factor'].values
        y = df['2017-07-04'].values
        dr.axes.bar(x, y)
        dr.axes.set_xticks(x)
        dr.axes.set_xticklabels(label,rotation='vertical')
        #dr.axes.xaxis.set_ticks_position('top')
    def draw_exposure_industry(self,dr):
        # 行业因子敞口图
        df = self.df_exp.iloc[10:,[0,-1]]
        x = range(len(df))
        label = df['factor'].values
        y = df['2017-07-04'].values
        dr.axes.bar(x, y)
        dr.axes.set_xticks(x)
        dr.axes.set_xticklabels(label,rotation='vertical')
    def draw_factor_accumulate(self,dr):
        # 因子累计图
        self.input_factor_text = self.input_factor.currentText()
        ser = self.df_rtn.loc[self.input_factor_text, :]
        ser = ser.cumsum()
        x = range(len(ser))
        label = ser.index.str[-5:].get_values()
        label = label[[0,20,40,60,80,100]]
        y = ser.values
        dr.axes.plot(x, y)
        #dr.axes.set_xticks(x)
        dr.axes.set_xticklabels(label)
    def draw_factor_plot(self,dr):
        # 因子曲线图
        self.input_factor_text = self.input_factor.currentText()
        ser = self.df_pct.loc[self.input_factor_text, :]
        x = range(len(ser))
        label = ser.index.str[-5:].get_values()
        label = label[[0, 20, 40, 60, 80, 100]]
        y = ser.values
        dr.axes.plot(x, y)
        #dr.axes.set_xticks(x)
        dr.axes.set_xticklabels(label)

    def draw_factor_win(self,dr):
        # 因子win图
        self.input_factor_text = self.input_factor.currentText()
        ser = self.df_win.loc[self.input_factor_text, :]
        x = range(len(ser))
        label = ser.index.str[-5:].get_values()
        label = label[list(range(0,90,10))]
        y = ser.values
        dr.axes.plot(x, y)
        #dr.axes.set_xticks(x)
        dr.axes.set_xticklabels(label)

    # 画图函数
    def graph_exposure_style(self): # 因子贡献图
        dr = Figure_Canvas(width=6.5,height=4.6)
        self.draw_exposure_style(dr)
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(dr)
        self.exposure_style.setScene(graphicscene)
        self.exposure_style.show()
    def graph_exposure_industry(self): # 因子暴露图
        dr = Figure_Canvas(width=6.5, height=4.6)
        self.draw_exposure_industry(dr)
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(dr)
        self.exposure_industry.setScene(graphicscene)
        self.exposure_industry.show()
    def graph_factor_accumulate(self): # 因子累计图
        dr = Figure_Canvas(width=6.5, height=4.6)
        self.draw_factor_accumulate(dr)
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(dr)
        self.accumulate.setScene(graphicscene)
        self.accumulate.show()
    def graph_factor_plot(self): # 因子累计图
        dr = Figure_Canvas(width=6.5, height=4.6)
        self.draw_factor_plot(dr)
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(dr)
        self.factor_plot.setScene(graphicscene)
        self.factor_plot.show()
    def graph_factor_win(self): # 因子累计图
        dr = Figure_Canvas(width=6.5, height=4.6)
        self.draw_factor_win(dr)
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(dr)
        self.factor_win.setScene(graphicscene)
        self.factor_win.show()



    # 列表
    def tb(self,tv,path):
        #path = r'E:\PythonData\test\test.csv'
        try:
            df = pd.read_csv(path)
        except:
            df = pd.read_csv(path,encoding='gbk')
        df.index.name = 'index'
        model = PandasModel(df)
        tv.setModel(model)

# 用于画图的类
class Figure_Canvas(FigureCanvas):
    '''通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，
       又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplotlib的关键'''
    def __init__(self, parent=None, width=11, height=5, dpi=100):
        # 创建一个Figure，注意：该Figure为matplotlib下的figure，不是matplotlib.pyplot下面的figure
        fig = Figure(figsize=(width, height), dpi=100)
        FigureCanvas.__init__(self, fig) # 初始化父类
        self.setParent(parent)
        # 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法
        self.axes = fig.add_subplot(111)
    def test(self):
        x = [1,2,3,4,5,6,7,8,9]
        y = [23,21,32,13,3,132,13,3,1]
        self.axes.plot(x, y)

class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, df = pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        return QtCore.QVariant(str(self._df.ix[index.row(), index.column()]))

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()
