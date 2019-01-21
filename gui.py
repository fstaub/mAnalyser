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
 
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget,QMainWindow,QToolButton,QMenu,QTableWidgetItem)
from PyQt5.QtGui import QIcon, QStandardItemModel
from PyQt5.QtCore import Qt


import plot
import numpy as np

import random

class Detail_Window(QDialog):
    def __init__(self, data,title):
        super().__init__()
        # self.frame = QGroupBox("Details")
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(3)

        self.title = title
        self.left = 2
        self.top = 2        
        self.width = 400
        self.height = 600

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        count = 0
        for e in data:
            self.table.setItem(count,0,QTableWidgetItem(e[0]))
            self.table.setItem(count,1,QTableWidgetItem(str(e[1])) )     
            self.table.setItem(count,2,QTableWidgetItem(str(e[2]))  )  
            count += 1
            self.table.setRowCount(count+1)
        self.table.show()
        layout.addWidget(self.table)
        self.setLayout(layout)
        print(data)

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
        print("all",self.all_dates)


        self.initUI()

    def on_pushButton_clicked(self):
            self.dialog.show()

    def add_sel1(self,main_layout):
        self.ComboBoxInOut = QComboBox()
        for i,key in enumerate(['Einnahmen','Ausgaben']):
            print(i,key)
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
            print(i,key)
            self.ComboBoxStart.addItem(key)
        inner_layout.addWidget(self.ComboBoxStart)
        inner_layout.addWidget(QLabel("-"))            
        self.ComboBoxEnd = QComboBox()
        for i,key in enumerate(self.all_dates):
            print(i,key)
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


    def add_selection_group(self):
        self.selection_frame = QGroupBox("Optionen")

        main_layout = QVBoxLayout()       
        main_tabs = QTabWidget()
        tab_main1 = QWidget()
        tab_main2 = QWidget()
        # main_tabs.resize(200,700)

                # Add tabs
        main_tabs.addTab(tab_main1,"Mehrere Monate")
        main_tabs.addTab(tab_main2,"Ein Monat")

        # Tab 1
        layout = QVBoxLayout()        
        self.add_sel1(layout)
        self.add_sel2(layout)
        self.add_sel3(layout)
        self.add_sel4(layout)
        self.run1=QPushButton('OK')

        self.run1.clicked.connect(self.on_pushButton_plot)

        

        layout.addWidget(QLabel(""))
        layout.addWidget(self.run1)
        tab_main1.setLayout(layout)
    
        layout.addStretch(0)
        main_tabs.resize(300,700)
        main_layout.addWidget(main_tabs)
        main_layout.addStretch(1)
        self.selection_frame.setLayout(main_layout)

    def make_show_details(self,entries,date,title):
        def show_details():
            to_show = [d for d in entries if (d[0][3:] == date)]
            self.dw = Detail_Window(to_show,title)
            self.dw.show()
        return show_details  

    def update_data(self,in_data,keywords,start,end):
        sum_all = analyse.summary_months(in_data,list(keywords.keys()))
        # arranged = analyse.arrange_sum_by_data(sum_all)
        print("arranged",in_data)
        dates = analyse.find_dates(sum_all)
        dates = [d for d in dates if ( 
            datetime.datetime.strptime(end, "%m.%Y").date() 
            >=  datetime.datetime.strptime(d, "%m.%Y").date()
            >=  datetime.datetime.strptime(start, "%m.%Y").date()
            )]
        self.data_main_tab.clear()        
        for i,d in enumerate(dates):
            new_tab=QWidget()
            layout = QVBoxLayout()
            table = QTableWidget()
            table.setRowCount(1)
            table.setColumnCount(3)
            count = 0
            for e in list(keywords.keys()):
                if d in sum_all[e]:
                    table.setItem(count,0,QTableWidgetItem(e))
                    table.setItem(count,1,QTableWidgetItem(str(abs(sum_all[e][d]))))
                    detail_button = QPushButton("Details")
                    detail_button.clicked.connect(self.make_show_details(in_data[e],d,str(e)+" in "+str(d)))
                    table.setCellWidget(count,2,detail_button)
                    print(sum_all[e][d])
                    count += 1
                    table.setRowCount(count+1)
            table.sortItems(1)
            table.show()
            layout.addWidget(table)
            new_tab.setLayout(layout)
            self.data_main_tab.addTab(new_tab,d)



    def on_pushButton_plot(self):
        if (self.ComboBoxInOut.currentText() == "Einnahmen"):
            self.PLOT.update_plot(self.DATA.IN, self.KEYS.IN,
                self.ComboBoxStart.currentText(), self.ComboBoxEnd.currentText(),self.radioPlot1.isChecked())
            self.update_data(self.DATA.IN, self.KEYS.IN,self.ComboBoxStart.currentText(), self.ComboBoxEnd.currentText())    
        else:           
            self.PLOT.update_plot(self.DATA.OUT, self.KEYS.OUT,
                self.ComboBoxStart.currentText(), self.ComboBoxEnd.currentText(),self.radioPlot1.isChecked())
            self.update_data(self.DATA.OUT, self.KEYS.OUT,self.ComboBoxStart.currentText(), self.ComboBoxEnd.currentText())    


    def add_data_group(self):
        self.data_frame = QGroupBox("Data")
        layout = QVBoxLayout()
        self.data_main_tab = QTabWidget()
        layout.addWidget(self.data_main_tab)
        layout.addStretch()
        self.data_frame.setLayout(layout)        


    def add_plot_canvas(self):
        self.canvas_frame = QGroupBox("Plott")
        layout = QVBoxLayout() 
        # layout = QVBoxLayout()
        self.PLOT = PlotCanvas(self.canvas_frame, width=7, height=4)
        # self.PLOT.move(0,0)
 
        # button = QPushButton('PyQt5 button', self)
        # button.setToolTip('This s an example button')
        # button.move(500,0)
        self.toolbar = NavigationToolbar(self.PLOT, self)
        layout.addWidget(self.PLOT)
        layout.addWidget(self.toolbar)
        self.canvas_frame.setLayout(layout)

        # button.resize(140,100)
 
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

        self.selection_frame.setFixedWidth(350)
        self.canvas_frame.setFixedHeight(500)
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.selection_frame)
        self.right_frame = QGroupBox("Data")
        layout_right = QVBoxLayout()
        layout_right.addWidget(self.canvas_frame)
        layout_right.addWidget(self.data_frame)
        self.right_frame.setLayout(layout_right)
        mainLayout.addWidget(self.right_frame)
        self.setLayout(mainLayout)
        # mainLayout

        self.show()        


 
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

    def update_plot(self,data,keywords,start,end,bar):
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        self.figure, ax = plot.HistPlot(data,keywords,start,end,bar)
        # new_legend.show()
        self.draw()            