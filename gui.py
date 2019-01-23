"""
===============
Embedding In Tk
===============

"""

# import tkinter as tk
# import tkinter.ttk as ttk

# from matplotlib.backends.backend_tkagg import (
#     FigureCanvasTkAgg, NavigationToolbar2Tk)
# # Implement the default Matplotlib key bindings.
# from matplotlib.backend_bases import key_press_handler
# from matplotlib.figure import Figure


from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

# import matplotlib.pyplot as plt

import sys
import analyse
import datetime
import mplcursors
 
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget,QMainWindow,QToolButton,QMenu,QTableWidgetItem,QHeaderView)
from PyQt5.QtGui import QIcon, QStandardItemModel
from PyQt5.QtCore import Qt


import plot
import numpy as np

import random

class Detail_Window(QDialog):
    def __init__(self, data, title):
        super().__init__()
        # self.frame = QGroupBox("Details")
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(3)

        header = self.table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        self.title = title
        self.left = 2
        self.top = 2        
        self.width = 600
        self.height = 600

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        count = 0
        for e in data:
            self.table.setItem(count,0,QTableWidgetItem(e[0]))
            self.table.setItem(count,1,QTableWidgetItem(str(e[1])) )     
            self.table.setItem(count,2,QTableWidgetItem("{:10.2f} Eur".format(e[2])))  
            count += 1
            self.table.setRowCount(count+1)
        self.table.show()
        layout.addWidget(self.table)
        self.setLayout(layout)

class Second(QDialog):
    def __init__(self, keys):
        super().__init__()
        settings_frame = QGroupBox("Settings")
        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        # self.tabs.resize(350,200)


        # Add tabs
        self.tabs.addTab(self.tab1,"Einnahmen")
        self.tabs.addTab(self.tab2,"Ausgaben")
        
        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        for  k in keys.IN.keys():
            cb = QCheckBox(k, self)
            self.tab1.layout.addWidget(cb)  
        self.tab1.setLayout(self.tab1.layout)

        # Create second tab
        self.tab2.layout = QVBoxLayout(self)
        for  k in keys.OUT.keys():
            cb = QCheckBox(k, self)
            self.tab2.layout.addWidget(cb)  
        self.tab2.setLayout(self.tab2.layout)


        layout.addWidget(self.tabs)
        layout.addStretch()
        settings_frame.setLayout(layout) 


        mainLayout = QGridLayout()
        mainLayout.addWidget(settings_frame, 1, 0)
        self.setLayout(mainLayout)

        # self.setLayout(mainLayout)
        # self.show()  

def QColumn(w1,w2):
        group = QGroupBox()
        layout = QHBoxLayout()
        layout.addWidget(w1)
        layout.addWidget(w2)
        group.setLayout(layout)
        return group   

class App(QDialog):
    def __init__(self,input_data,keywords):
        super().__init__()
        # For the window
        self.left = 2
        self.top = 2
        self.title = 'mAnalyser - explore your bank accounts'
        self.width = 1200
        self.height = 800

        self.DATA = input_data  
        self.KEYS = keywords  

        # for the data
        self.used_date_start = ""
        self.used_date_end = ""
        self.used_type = ""
        self.all_dates = analyse.find_dates(analyse.summary_months(self.DATA.IN,list(self.KEYS.IN.keys())))

        self.initUI()

    def on_pushButton_clicked(self):
            self.dialog.show()

    def add_selection_inout(self,main_layout):
        self.add_sel1(main_layout)
        self.add_sel2(main_layout)
        self.add_sel3(main_layout)
        self.add_sel4(main_layout)

    def add_sel1(self,main_layout):
        self.ComboBoxInOut = QComboBox()
        for i,key in enumerate(['Einnahmen','Ausgaben']):
            self.ComboBoxInOut.addItem(key)
            item = self.ComboBoxInOut.model().item(i, 0)
            item.setCheckState(Qt.Unchecked)
        main_layout.addWidget(QColumn(QLabel("Geldfluss"),self.ComboBoxInOut))

    def add_sel2(self,main_layout):
        self.pushButton = QPushButton("Config")
        self.pushButton.clicked.connect(self.on_pushButton_clicked)
        main_layout.addWidget(QColumn(QLabel("Kategorien"),self.pushButton))

    def add_sel3(self,main_layout):
        inner_group = QGroupBox()
        inner_layout = QHBoxLayout()
        self.ComboBoxStart = QComboBox()
        for i,key in enumerate(self.all_dates):
            self.ComboBoxStart.addItem(key)
        inner_layout.addWidget(self.ComboBoxStart)
        inner_layout.addWidget(QLabel("-"))            
        self.ComboBoxEnd = QComboBox()
        for i,key in enumerate(self.all_dates):
            self.ComboBoxEnd.addItem(key)
        self.ComboBoxEnd.setCurrentIndex(len(self.all_dates)-1)
        inner_layout.addWidget(self.ComboBoxEnd)
        inner_group.setLayout(inner_layout)
        main_layout.addWidget(QColumn(QLabel("Zeitraum"),inner_group)) 

    def add_sel4(self,main_layout):
        self.radioPlot1 = QRadioButton("Bar-Plot")
        self.radioPlot2 = QRadioButton("Line-Plot")
        self.radioPlot1.setChecked(True) 
        main_layout.addWidget(QColumn(self.radioPlot1, self.radioPlot2 ))


    def add_selection_stocks(self,main_layout):
#        self.add_sel1(main_layout)
#        self.add_sel2(main_layout)
        self.add_sel3(main_layout)
 #       self.add_sel4(main_layout)

    def add_selection_accounts(self,main_layout):
#        self.add_sel1(main_layout)
#        self.add_sel2(main_layout)
        self.add_sel3(main_layout)
 #

    def add_selection_group(self):
        self.selection_frame = QGroupBox("Optionen")

        main_layout = QVBoxLayout()       
        main_tabs = QTabWidget()
        tab_main1 = QWidget()
        tab_main2 = QWidget()
        tab_main3 = QWidget()
        # main_tabs.resize(200,700)

                # Add tabs
        main_tabs.addTab(tab_main1,"Einnahmen/Ausgaben")
        main_tabs.addTab(tab_main2,"Konten")
        main_tabs.addTab(tab_main3,"Aktien")

        # Tab: In Out
        layout = QVBoxLayout()        
        self.add_selection_inout(layout)
        self.button_inout=QPushButton('OK')
        self.button_inout.clicked.connect(self.on_pushButton_inout)
        layout.addWidget(QLabel(""))
        layout.addWidget(self.button_inout)
        tab_main1.setLayout(layout)        


        # Tab: Accounts
        layout = QVBoxLayout()  
        self.add_selection_stocks(layout)      
        self.button_accounts=QPushButton('OK')
        self.button_accounts.clicked.connect(self.on_pushButton_accounts)
        layout.addWidget(QLabel(""))
        layout.addWidget(self.button_accounts)
        tab_main2.setLayout(layout)

        # Tab: Stocks
        layout = QVBoxLayout() 
        self.add_selection_accounts(layout)       
        self.button_stocks=QPushButton('OK')
        self.button_stocks.clicked.connect(self.on_pushButton_stocks)
        layout.addWidget(QLabel(""))
        layout.addWidget(self.button_stocks)
        tab_main3.setLayout(layout)



        # layout.addWidget(QLabel(""))
        # layout.addWidget(self.run1)
        # tab_main1.setLayout(layout)
    
        layout.addStretch(0)
        main_tabs.resize(300,700)
        main_layout.addWidget(main_tabs)
        main_layout.addStretch(1)
        self.selection_frame.setLayout(main_layout)

    # def make_show_details(self,entries,date,title):
    #     def show_details():
    #         if date =="all":
    #             to_show = entries
    #         else:
    #             to_show = [d for d in entries if (d[0][3:] == date)]                
    #         self.dw = Detail_Window(to_show,title)
    #         self.dw.show()
    #     return show_details  

    def update_data(self,in_data,keywords,start,end):
        # arranged = analyse.arrange_sum_by_data(sum_all)
        dates = analyse.generate_dates(start,end)
        use_data = analyse.group_data_by_month(in_data,dates)
        # dates.append("Summe und Durchschnitt")    

        use_data['Durchschnitt'] = analyse.average_months(in_data,start,end)

        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",use_data['Durchschnitt'])
        print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB",use_data['03.2018'])
        data_tab = DataTabs(self.data_main_tab, use_data)


        # self.data_main_tab.clear()  

        # # average
        # entry_sum = {}

        # for i,d in enumerate(dates):
        #     new_tab=QWidget()
        #     layout = QVBoxLayout()
        #     table = QTableWidget()
        #     table.setRowCount(1)
        #     table.setColumnCount(3)

        #     header = table.horizontalHeader()       
        #     header.setSectionResizeMode(0, QHeaderView.Stretch)
        #     header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        #     header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        #     count = 0
        #     for e in list(keywords.keys()):
        #         if d in sum_all[e]:
        #             table.setItem(count,0,QTableWidgetItem(e))
        #             table.setItem(count,1,QTableWidgetItem("{:10.2f} Eur".format(abs(sum_all[e][d]))))
        #             detail_button = QPushButton("Details")
        #             detail_button.clicked.connect(self.make_show_details(in_data[e],d,str(e)+" in "+str(d)))
        #             table.setCellWidget(count,2,detail_button)
        #             count += 1
        #             table.setRowCount(count+1)
        #             if e in entry_sum:
        #                 entry_sum[e] += abs(sum_all[e][d])
        #             else: 
        #                 entry_sum[e] = abs(sum_all[e][d])
        #     table.sortItems(1)
        #     table.show()
        #     layout.addWidget(table)
        #     new_tab.setLayout(layout)
        #     self.data_main_tab.addTab(new_tab,d)
        
        # # now the average 
        # new_tab=QWidget()
        # layout = QVBoxLayout()
        # table = QTableWidget()
        # table.setRowCount(1)
        # table.setColumnCount(4)
        # count = 0
        # for e in list(keywords.keys()):
        #     table.setItem(count,0,QTableWidgetItem(e))
        #     table.setItem(count,1,QTableWidgetItem("{:10.2f} Eur".format(abs(entry_sum[e]))))
        #     table.setItem(count,2,QTableWidgetItem("{:10.2f} Eur".format(entry_sum[e]/len(dates))))
        #     detail_button = QPushButton("Details")
        #     detail_button.clicked.connect(self.make_show_details(in_data[e],"all",str(e)+" (Gesamt) "))
        #     table.setCellWidget(count,3,detail_button)

        #     count += 1
        #     table.setRowCount(count+1)
        # header = table.horizontalHeader()       
        # header.setSectionResizeMode(0, QHeaderView.Stretch)
        # header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(2, QHeaderView.ResizeToContents)            
        # table.show()
        # layout.addWidget(table)
        # new_tab.setLayout(layout)
        # self.data_main_tab.addTab(new_tab,"Summe und Durchschnitt")    
        # self.data_main_tab.setCurrentIndex(len(dates))




    def on_pushButton_inout(self):
        if self.radioPlot1.isChecked():
            style = "Bar"
        else:
            style = "Linear"

        if (self.ComboBoxInOut.currentText() == "Einnahmen"):
            arguments = [self.DATA.IN, self.KEYS.IN,
                self.ComboBoxStart.currentText(), self.ComboBoxEnd.currentText()]
            self.update_data(self.DATA.IN, self.KEYS.IN,self.ComboBoxStart.currentText(), self.ComboBoxEnd.currentText())
        else:           
            arguments = [self.DATA.OUT, self.KEYS.OUT,
                self.ComboBoxStart.currentText(), self.ComboBoxEnd.currentText()]
            self.update_data(self.DATA.OUT, self.KEYS.OUT,self.ComboBoxStart.currentText(), self.ComboBoxEnd.currentText())    
        self.PLOT_UP.update_plot(*arguments,style) 
        self.PLOT_DOWN_LEFT.update_plot(*arguments,"Pie")
        self.PLOT_DOWN_RIGHT.update_plot(*arguments,"BarAverage")  

        self.canvas_down_frame.setTitle("Monatsdurchschnitt")
        self.canvas_frame.setTitle("Monatswerte")


    def on_pushButton_accounts(self):  
        self.PLOT_UP.update_plot_account(self.DATA.changes, self.KEYS.OUT,self.ComboBoxStart.currentText(), self.ComboBoxEnd.currentText(),"Bar")                    
        self.PLOT_DOWN_RIGHT.update_plot_account(self.DATA.changes, self.KEYS.OUT,self.ComboBoxStart.currentText(), self.ComboBoxEnd.currentText(),"Diff")                    

    def on_pushButton_stocks(self):  
        pass                    


    def add_data_group(self):
        self.data_frame = QGroupBox("Data")
        layout = QVBoxLayout()
        self.data_main_tab = QTabWidget()
        layout.addWidget(self.data_main_tab)
        layout.addStretch()
        self.data_frame.setLayout(layout)        


    def add_plot_canvas(self):
        # # Main
        self.canvas_frame = QGroupBox("")
        layout = QVBoxLayout() 

        # # TOP
        self.PLOT_UP = PlotCanvas(self.canvas_frame, width=7, height=4)
        layout.addWidget(self.PLOT_UP)

        # # # Bottom
        self.canvas_down_frame = QGroupBox("")        
        layout_down = QHBoxLayout()
        self.canvas_DL_frame = QGroupBox("")        
        self.canvas_DR_frame = QGroupBox("")        
        self.PLOT_DOWN_LEFT = PlotCanvas(self.canvas_DL_frame, width=3, height=4)
        self.PLOT_DOWN_RIGHT = PlotCanvas(self.canvas_DR_frame, width=4, height=4)
        layout_down.addWidget(self.PLOT_DOWN_LEFT)
        layout_down.addWidget(self.PLOT_DOWN_RIGHT)
        self.canvas_down_frame.setLayout(layout_down)

        # # Main again
        # layout.addWidget(self.canvas_frame)
        layout.addWidget(self.canvas_down_frame)
        self.canvas_frame.setLayout(layout)

        # self.canvas_frame = QGroupBox("Plott")
        # layout = QVBoxLayout() 
        # self.PLOT = PlotCanvas(self.canvas_frame, width=7, height=4)
        # self.toolbar = NavigationToolbar(self.PLOT, self)
        # layout.addWidget(self.PLOT)
        # self.canvas_frame.setLayout(layout)


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.add_plot_canvas()
        self.add_selection_group()
        self.add_data_group()

        # window.show()

        # mainLayout = QGridLayout()
        # mainLayout.addWidget(self.selection_frame, 1, 0)
        # mainLayout.addWidget(self.canvas_frame, 3, 0)
        # self.setLayout(mainLayout)

        self.canvas_frame.setFixedHeight(self.height)
        mainLayout = QHBoxLayout()
#        mainLayout.addWidget(self.selection_frame)

        self.left_frame = QGroupBox("")
        layout_left = QVBoxLayout()
        self.left_frame.setFixedWidth(350)
        layout_left.addWidget(self.selection_frame)
        layout_left.addWidget(self.data_frame)
        self.left_frame.setLayout(layout_left)
        mainLayout.addWidget(self.left_frame)




        self.right_frame = QGroupBox("")
        layout_right = QVBoxLayout()
        layout_right.addWidget(self.canvas_frame)
#        layout_right.addWidget(self.data_frame)
        self.right_frame.setLayout(layout_right)
        mainLayout.addWidget(self.right_frame)
        self.setLayout(mainLayout)
        # mainLayout

        self.show()        


class DataTabs():
    def __init__(self, tab, tabs):
        self.tab = tab
        self.tab.clear()  

        self.generate_tab_content(tabs)

    def generate_tab_content(self, tabs):
            for t in tabs.keys():
                new_tab=QWidget()
                layout = QVBoxLayout()
                table = QTableWidget()
                table.setRowCount(1)
                table.setColumnCount(3)

                header = table.horizontalHeader()       
                header.setSectionResizeMode(0, QHeaderView.Stretch)
                header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
                header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

                count = 0
                for d in tabs[t].keys():
                    if (abs(tabs[t][d]['sum'])) > 0:
                        table.setItem(count,0,QTableWidgetItem(d))
                        table.setItem(count,1,QTableWidgetItem("{:10.2f} Eur".format(tabs[t][d]['sum'])))
                        detail_button = QPushButton("Details")
                        detail_button.clicked.connect(self.make_show_details(tabs[t][d]['entries'],str(d)+" in "+str(t)))
                        table.setCellWidget(count,2,detail_button)
                        count += 1
                        table.setRowCount(count+1)
                table.sortItems(1)
                table.show()
                layout.addWidget(table)
                new_tab.setLayout(layout)
                self.tab.addTab(new_tab,t)    
                self.tab.setCurrentIndex(count)



            # for e in entries:
            #     if d in short_data[e]:
            #         table.setItem(count,0,QTableWidgetItem(e))
            #         table.setItem(count,1,QTableWidgetItem("{:10.2f} Eur".format(abs(short_data[e][d]))))
            #         detail_button = QPushButton("Details")
            #         detail_button.clicked.connect(self.make_show_details(full_data[e],str(e)+" in "+str(d)))
            #         table.setCellWidget(count,2,detail_button)
            #         count += 1
            #         table.setRowCount(count+1)

    # def make_show_details(self,entries,date,title):
    #     def show_details():
    #         if date =="all":
    #             to_show = entries
    #         else:
    #             to_show = [d for d in entries if (d[0][3:] == date)]                
    #         self.dw = Detail_Window(to_show,title)
    #         self.dw.show()
    #     return show_details  
    def make_show_details(self,to_show,title):
        def show_details():
            # if date =="all":
            #     to_show = entries
            # else:
            #     to_show = [d for d in entries if (d[0][3:] == date)]                
            self.dw = Detail_Window(to_show,title)
            self.dw.show()
        return show_details 


 
class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4):
        fig = Figure(figsize=(width, height))
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        # FigureCanvas.setSizePolicy(self,
        #         QSizePolicy.Expanding,
        #         QSizePolicy.Expanding)
        # FigureCanvas.updateGeometry(self)
        fig.tight_layout()
        self.plot()
 
 
    def plot(self):
        data = [0]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        # ax.set_title('PyQt Matplotlib Example')
        self.draw()

    def update_plot(self,data,keywords,start,end,style):
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        if style == "Bar":
            self.figure, ax = plot.HistPlot_InOut(data,keywords,start,end,True)
        elif style == "Linear":
            self.figure, ax = plot.HistPlot_InOut(data,keywords,start,end,False)
        elif style == "Pie":
            self.figure, ax = plot.PieChart(data,keywords,start,end,3.5,4) 
        elif style == "BarAverage":
            self.figure, ax = plot.BarAverage_InOut(data,keywords,start,end,4,3.5)                        
        # new_legend.show()

        self.draw()    
        self.show() 

    def update_plot_account(self,data,keywords,start,end,style):
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        if style == "Bar":
            self.figure, ax = plot.HistPlot_Account(data,start,end,True)
        elif style == "Linear":
            self.figure, ax = plot.HistPlot_Account(data,start,end,False)
        elif style == "Pie":
            self.figure, ax = plot.HistPlot_Changes(data,start,end,3.5,4) 
        elif style == "Diff":
            self.figure, ax = plot.HistPlot_Changes(data,start,end,4,3.5)                        
        # new_legend.show()

        self.draw()    
        self.show()        

    #     self.mpl_connect('button_press_event', self.mouseClick)
    #     self.mpl_connect('motion_notify_event', self.mouseMove)
    #     # self.mpl_connect('motion_notify_event', self.mouseOver)

    # def mouseClick(self, event):
    #     print(event)

    # def mouseMove(self, event):
    #     print(event)        
