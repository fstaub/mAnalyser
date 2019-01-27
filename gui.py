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


# import matplotlib.pyplot as plt
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import mplcursors
from mpldatacursor import datacursor

# import matplotlib.pyplot as plt

import sys
import analyse
import datetime
import calendar
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
    ''' Creates a new window which displays in a table 
        all items belonging to a given category/month  
    '''
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
            self.table.setItem(count,0,QTableWidgetItem(e[0].strftime("%d.%m.%Y")))
            self.table.setItem(count,1,QTableWidgetItem(str(e[1])) )     
            self.table.setItem(count,2,QTableWidgetItem("{:10.2f} Eur".format(e[2])))  
            count += 1
            self.table.setRowCount(count+1)
        self.table.show()
        layout.addWidget(self.table)
        self.setLayout(layout)

class Data_Window(QDialog):
    ''' Creates a new window which displays in a table 
        all items belonging to a given category/month  
    '''
    def __init__(self, all_data, title):
        super().__init__()
        # self.frame = QGroupBox("Details")
           

        self.title = title
        self.left = 2
        self.top = 2        
        self.width = 600
        self.height = 600

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.generate_tables(all_data)
    
    def generate_tables(self, all_data):
        self.layout = QVBoxLayout()

        self.tabs = QTabWidget()

        for i in all_data:
          for k in i.keys():   
        # Add tabs
            new_tab = QWidget()
            self.tabs.addTab(new_tab, k)
            tab_layout = QVBoxLayout()
            table = QTableWidget()
            table.setRowCount(1)
            table.setColumnCount(3)
            header = table.horizontalHeader()       
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

            count = 0
            for e in i[k]:
                table.setItem(count,0,QTableWidgetItem(e[0].strftime("%d.%m.%Y")))
                table.setItem(count,1,QTableWidgetItem(str(e[1])) )     
                table.setItem(count,2,QTableWidgetItem("{:10.2f} Eur".format(e[2])))  
                count += 1
                table.setRowCount(count+1)
            table.show()
            tab_layout.addWidget(table)
            new_tab.setLayout(tab_layout)            


        self.layout.addWidget(self.tabs)

        self.setLayout(self.layout)        



class NewPlotWindow(QDialog):
    ''' Creates a new window which contains the plots
    '''
    def __init__(self, arg1=[], arg2=[], arg3=[], arg4=[], title=""):
        super().__init__()
        # self.frame = QGroupBox("Details")
        layout = QVBoxLayout()
        self.title = title
        self.left = 300
        self.top = 2        
        self.width = 1300
        self.height = 1000

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.add_plot_canvas_new4(arg1, arg2, arg3, arg4)                                    
        layout.addWidget(self.canvas_frame)
        self.setLayout(layout)      

    def add_plot_canvas_new4(self, arg1, arg2, arg3, arg4):
        # # Main
        self.canvas_frame = QGroupBox("")

        layout = QVBoxLayout() 
        layout_top = QHBoxLayout() 
        layout_down = QHBoxLayout() 
        frame_top = QGroupBox()
        frame_down = QGroupBox()


        if (arg1 != []):
            self.PLOT_TOP_LEFT = plot.NewPlotCanvas(arg1[0], in_arg=arg1[1:], width=7, height=4)
            layout_top.addWidget(self.PLOT_TOP_LEFT)

        if (arg3 != []):
            self.PLOT_TOP_RIGHT = plot.NewPlotCanvas(arg3[0], in_arg=arg3[1:], width=7, height=4)
            layout_top.addWidget(self.PLOT_TOP_RIGHT)

        if (arg2 != []):
            self.PLOT_DOWN_LEFT = plot.NewPlotCanvas(arg2[0], in_arg=arg2[1:], width=7, height=4)
            layout_down.addWidget(self.PLOT_DOWN_LEFT)

        if (arg4 != []):
            self.PLOT_DOWN_RIGHT = plot.NewPlotCanvas(arg4[0], in_arg=arg4[1:], width=7, height=4)
            layout_down.addWidget(self.PLOT_DOWN_RIGHT)

        # layout = QGridLayout() 
        # layout.addWidget(self.PLOT_TOP_LEFT,0,0)
        # layout.addWidget(self.PLOT_TOP_RIGHT,0,1)
        # layout.addWidget(self.PLOT_DOWN_LEFT,1,0)
        # layout.addWidget(self.PLOT_DOWN_RIGHT,1,1)

        frame_top.setLayout(layout_top)
        frame_down.setLayout(layout_down)
        layout.addWidget(frame_top)
        layout.addWidget(frame_down)

        self.canvas_frame.setLayout(layout)           


class ConfigWindow(QDialog):
    ''' opens a new window to configure/select 
        what keys are included in the plots
    '''
    def __init__(self, grandparent, keys, titles, ref_object):
        super().__init__()
        # settings_frame = QGroupBox("Configuration")
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        self.single_tabs = []
        self.boxes = []
        self.box_labels = []
        self.ref = ref_object
        self.is_selected = ref_object.is_included
        self.grandparent = grandparent

        for i, k in enumerate(keys):
        # Add tabs
            self.single_tabs.append(QWidget())
            self.tabs.addTab(self.single_tabs[-1], titles[i])
            tab_layout = QVBoxLayout(self)
            for  kk in k.keys():
                self.boxes.append(QCheckBox(kk,self))
                self.box_labels.append(kk)
                # if kk in self.grandparent.parent.KEYS.is_included:
                if kk in self.is_selected:
                    self.boxes[-1].setChecked(True)
                tab_layout.addWidget(self.boxes[-1])  
            self.single_tabs[-1].setLayout(tab_layout)

        buttons = QGroupBox("")
        button_layout = QHBoxLayout()        
        self.button_ok=QPushButton('OK')
        self.button_ok.clicked.connect(self.on_pushButton_ok)
        button_layout.addWidget(self.button_ok)

        self.button_cancel=QPushButton('Cancel')
        self.button_cancel.clicked.connect(self.on_pushButton_cancel)
        button_layout.addWidget(self.button_cancel)
        buttons.setLayout(button_layout)

        layout.addWidget(self.tabs)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def on_pushButton_ok(self):
        self.is_selected = []
        for i, n in zip(self.boxes, self.box_labels):
            if i.isChecked() is True:
                self.is_selected.append(n)
        self.ref.is_included = self.is_selected
        self.close()

    def on_pushButton_cancel(self):
        self.close()


def QColumn(w1,w2):
        ''' command to arrange two given widgets in a line'''
        group = QGroupBox()
        layout = QHBoxLayout()
        layout.addWidget(w1)
        layout.addWidget(w2)
        group.setLayout(layout)
        return group   


class OptionsWidget(QWidget):
    ''' main class to create the tabs containing the
        different options to steer the analysis'''
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QVBoxLayout()
        self.group = QGroupBox()
        self.add_contents()
        self.group.setLayout(self.layout)
        self.setLayout(self.layout)

    def add_contents(self):
        pass 

    def add_start_button(self):
        pushButton = QPushButton("Start")
        pushButton.clicked.connect(self.on_pushButton_start)
        self.layout.addWidget(pushButton)

    def add_time_period(self):
        inner_group = QGroupBox()
        inner_layout = QHBoxLayout()
        self.ComboBoxStart = QComboBox()
        for i,key in enumerate(self.parent.all_dates):
            self.ComboBoxStart.addItem(key)
        inner_layout.addWidget(self.ComboBoxStart)

        inner_layout.addWidget(QLabel("-"))            
        
        self.ComboBoxEnd = QComboBox()
        for i,key in enumerate(self.parent.all_dates):
            self.ComboBoxEnd.addItem(key)
        self.ComboBoxEnd.setCurrentIndex(len(self.parent.all_dates)-1)
        inner_layout.addWidget(self.ComboBoxEnd)
        inner_group.setLayout(inner_layout)
        self.layout.addWidget(QColumn(QLabel("Zeitraum"),inner_group))         

    def add_configure(self):
        pushButton = QPushButton("Auswahl")
        pushButton.clicked.connect(self.on_pushButton_config)
        self.layout.addWidget(QColumn(QLabel("Kategorien"), pushButton))

    def on_pushButton_start(self):
        pass

    def on_pushButton_config(self):
        pass    

    def set_dates(self):
        self.date_start = analyse.go_to_last_day(datetime.datetime.strptime(self.ComboBoxStart.currentText() ,"%m/%Y").date())
        self.date_end = analyse.go_to_last_day(datetime.datetime.strptime(self.ComboBoxEnd.currentText() ,"%m/%Y").date())
        
    
class InOutTab(OptionsWidget):
    def __init__(self, parent):
        super().__init__(parent)

    def add_contents(self):
        self.add_categories()
        self.add_time_period()
        self.add_configure()
        self.add_radio()
        self.add_button_data()
        self.add_start_button()

    def add_categories(self):
        self.ComboBox = QComboBox()
        for i,key in enumerate(['Einnahmen', 'Ausgaben']):
            self.ComboBox.addItem(key)
            item = self.ComboBox.model().item(i, 0)
            item.setCheckState(Qt.Unchecked)
        self.layout.addWidget(QColumn(QLabel("Geldfluss"),self.ComboBox))

    def add_button_data(self):   
        self.pushButton = QPushButton("Show Data")
        self.pushButton.clicked.connect(self.on_pushButton_data)
        self.layout.addWidget(self.pushButton)  

    def on_pushButton_data(self):
        self.data_window = Data_Window([self.parent.DATA.IN, self.parent.DATA.OUT, 
            {'Not Categorised (Einkommen)': self.parent.DATA.missing_in,
            'Not Categorised (Ausgaben)': self.parent.DATA.missing_out,
            'Internal': self.parent.DATA.internal}],
            "Input Data")
        self.data_window.show()         


    def add_radio(self):	
        self.radioPlot1 = QRadioButton("Linear")	 
        self.radioPlot2 = QRadioButton("Log")	 
        self.radioPlot1.setChecked(True) 	   
        self.layout.addWidget(QColumn(self.radioPlot1, self.radioPlot2 ))

    def on_pushButton_config(self):
        self.cw = ConfigWindow(self, [self.parent.KEYS.IN, self.parent.KEYS.OUT], 
            ["Einnahmen","Ausgaben"], self.parent.KEYS)
        self.cw.show()

    def update_data(self, in_data, keywords, start, end):
        dates = analyse.generate_dates(start, end)
        use_data = analyse.group_data_by_month(in_data, dates)
        use_data['Durchschnitt'] = analyse.average_months(in_data, start, end)
        data_tab = DataTabs(self.parent.data_main_tab, use_data)

    def on_pushButton_start(self):
        self.set_dates()

        if (self.ComboBox.currentText() == "Einnahmen"):
                all_keys = self.parent.KEYS.IN
                all_data = self.parent.DATA.IN
        else:
                all_keys = self.parent.KEYS.OUT
                all_data = self.parent.DATA.OUT
        s_inout = self.ComboBox.currentText()

        selected_keys =  {key:value for key, value in all_keys.items() if key in self.parent.KEYS.is_included }
        arguments = [all_data, selected_keys, self.date_start, self.date_end]

        self.update_data(*arguments)    

        if self.radioPlot1.isChecked():
            style1 = "StackedBar"
            style2 = "HorizontalBar"
        else:
            style1 = "StackedBarLog"
            style2 = "HorizontalBarLog"

        self.new_plot_window = NewPlotWindow( 
                arg4=[style1, *analyse.prepare_stacked_bar(*arguments), s_inout + " pro Monat"],
                arg2 = [],
                arg3=["PieChart", *analyse.prepare_pie_chart(*arguments), "Prozentuale Verteilung der " + s_inout], 
                arg1=[style2, *analyse.prepare_horizontal_bar(*arguments), "Durchschnittliche " + s_inout], 
                title="Plots")

        self.new_plot_window.show()
        # self.new_plot_window.canvas_down_frame.setTitle("Monatsdurchschnitt")
        # self.new_plot_window.canvas_frame.setTitle("Monatswerte")

class AccountTab(OptionsWidget):
    def __init__(self, parent):
        super().__init__(parent)

    def add_contents(self):
        self.add_time_period()
        self.add_configure()        
        self.add_start_button()

    def on_pushButton_config(self):
        to_dict = lambda x: {y: 1 for y in x}
        self.cw = ConfigWindow(self, [to_dict(self.parent.DATA.names)], 
            ["Konten"], self.parent.DATA)
        self.cw.show()

    def on_pushButton_start(self):
        self.set_dates()        

        # self.update_data(self.parent.DATA.inout_account, self.parent.KEYS.OUT,
        #     self.date_start, self.date_end) 

        self.update_data(self.parent.DATA.transfers, self.parent.DATA.changes, self.parent.KEYS.OUT,
            self.date_start, self.date_end)               

        arguments = [{**self.parent.DATA.changes, **{"Depot": self.parent.DEPOT.current_values_total}}, 
                self.parent.DATA.is_included,
                self.date_start, self.date_end]

        arguments_diff = [{**self.parent.DATA.transfers,
                 **{"Depot": self.parent.DEPOT.current_changes_total}}, self.parent.DATA.is_included,
                self.date_start, self.date_end]

        self.new_plot_window = NewPlotWindow(
            arg1=["StackedBar", *analyse.prepare_stacked_bar_accounts(*arguments), "Kontostände pro Monat"],
            arg2=["PlusMinusBar",*analyse.prepare_plusminus_bar(*arguments_diff), "Monatliche Veränderungen"], 
            arg3=["HorizontalBar",*analyse.prepare_horizontal_bar_accounts(*arguments), "Letzte Kontostände"],                         
            arg4=["PieChart",*analyse.prepare_horizontal_bar_accounts(*arguments), "Prozentuale Verteilung des Vermögens"],
            title="Plots")
        self.new_plot_window.show()

    def update_data(self, in_data1, in_data2, keywords, start, end):
        dates = analyse.generate_dates(start, end)
        use_data1 = analyse.group_data_by_month(in_data1, dates)
        use_data2 = analyse.last_of_month(in_data2, dates)
        temp = use_data1
        for k1 in temp.keys():
            for k2 in temp[k1].keys():
                use_data1[k1][k2]['sum'] = [use_data1[k1][k2]['sum'], use_data2[k1][k2]['sum']]
        
        use_data = use_data1
        for k in use_data1.keys():
                new_sum0 = 0
                new_sum1 = 0
                new_all = []
                for kk in use_data1[k].keys():
                    new_sum0 += use_data1[k][kk]['sum'][0]
                    new_sum1 += use_data1[k][kk]['sum'][1]
                    new_all += use_data1[k][kk]['entries']
        use_data[k]['Gesamt'] = {}
        use_data[k]['Gesamt']['sum'] = [new_sum0, new_sum1]
        use_data[k]['Gesamt']['entries'] = new_all
        data_tab = DataTabs(self.parent.data_main_tab, use_data, rows=4)



class StockTab(OptionsWidget):
    def __init__(self, parent):
        super().__init__(parent)

    def add_contents(self):
        self.add_time_period()
        self.add_configure() 
        self.add_choice()       
        self.add_radio()       
        self.add_start_button()

    def add_choice(self):
        self.checkAktien = QCheckBox("Aktien")
        self.checkFonds = QCheckBox("Fonds")
        self.checkAktien.setChecked(True) 
        self.checkFonds.setChecked(True) 
        self.layout.addWidget(QColumn(self.checkAktien, self.checkFonds ))   

    def add_radio(self):	
        self.radioPlot2 = QRadioButton("Absolut")	 
        self.radioPlot1 = QRadioButton("Relativ")	 
        self.radioPlot2.setChecked(True) 	   
        self.layout.addWidget(QColumn(self.radioPlot1, self.radioPlot2 ))


    def on_pushButton_config(self):
        to_dict = lambda x: {y: 1 for y in x}
        self.cw = ConfigWindow(self, [to_dict(self.parent.DEPOT.stocks), to_dict(self.parent.DEPOT.fonds)], 
            ["Aktien","Fonds"], self.parent.DEPOT)
        self.cw.show()        

    def on_pushButton_start(self):
        self.set_dates()        
        all_keys = []
        if self.checkFonds.isChecked():
            all_keys += self.parent.DEPOT.fonds 
        if self.checkAktien.isChecked():
            all_keys += self.parent.DEPOT.stocks 

        selected_keys = [x for x in all_keys if x in self.parent.DEPOT.is_included]

        if self.radioPlot1.isChecked():
            relativ = True
        else:
            relativ = False

        arguments = [self.parent.DEPOT.all_information,
                    self.parent.DEPOT.current_values_total,
                     selected_keys,
                self.date_start, self.date_end, relativ]
        arguments_total = [self.parent.DEPOT.current_values, selected_keys,
                self.date_start, self.date_end]   

        self.update_data(*arguments_total)                              

        self.new_plot_window = NewPlotWindow(
            arg1=["ScatterPlot", *analyse.prepare_scatter_total_change_stocks(*arguments), "Gesamte Veränderung des Depots"],
            arg2=["ScatterPlotBar", *analyse.prepare_scatter_daily_changes_stocks(*arguments), "Tägliche Veränderung des Depots"],                                     
            arg3=["StackedBar", *analyse.prepare_stacked_bar_accounts(*arguments_total), "Absolute Zusammensetzung des Depots"], 
            arg4=["PieChart", *analyse.prepare_pie_total_stocks(*arguments_total), "Prozentuale Zusammensetzung des Depots"],
            title="Plots")
        self.new_plot_window.show()   

    def update_data(self, in_data, keywords, start, end):
        dates = analyse.generate_dates(start, end)
        use_data = analyse.last_of_month(in_data,dates)
        use_data['Depotwert'] = analyse.depot_value(use_data)
        data_tab = DataTabs(self.parent.data_main_tab, use_data)          


class App(QDialog):
    def __init__(self, input_depot, input_data, keywords, plots):
        super().__init__()
        # For the window
        self.left = 2
        self.top = 2
        self.title = 'mAnalyser - explore your bank accounts'
        self.width = 400
        self.height = 800

        self.DEPOT = input_depot
        self.DATA = input_data  
        self.KEYS = keywords  

        # for the data
        self.used_date_start = ""
        self.used_date_end = ""
        self.used_type = ""
        self.all_dates = analyse.find_dates(analyse.summary_months(self.DATA.IN,list(self.KEYS.IN.keys())))

        self.initUI(plots)


    def add_selection_group(self):
        self.selection_frame = QGroupBox("Optionen")

        main_layout = QVBoxLayout()       
        main_tabs = QTabWidget()
        tab_main1 = InOutTab(self)
        tab_main2 = AccountTab(self)
        tab_main3 = StockTab(self)

        # Add tabs
        main_tabs.addTab(tab_main1,"Einnahmen/Ausgaben")
        main_tabs.addTab(tab_main2,"Konten")
        main_tabs.addTab(tab_main3,"Aktien")

        main_tabs.resize(300,700)
        main_layout.addWidget(main_tabs)
        main_layout.addStretch(1)
        self.selection_frame.setLayout(main_layout)

    def add_data_group(self):
        self.data_frame = QGroupBox("Data")
        layout = QVBoxLayout()
        self.data_main_tab = QTabWidget()
        layout.addWidget(self.data_main_tab)
        layout.addStretch()
        self.data_frame.setLayout(layout)  


    def initUI(self, plots):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.add_selection_group()
        self.add_data_group()
        # self.add_button_data()

        self.mainLayout = QHBoxLayout()
        self.left_frame = QGroupBox("")
        layout_left = QVBoxLayout()
        self.left_frame.setFixedWidth(350)
        # layout_left.addWidget(self.pushButton)            
        layout_left.addWidget(self.selection_frame)
        layout_left.addWidget(self.data_frame)
 
        self.left_frame.setLayout(layout_left)

        self.mainLayout.addWidget(self.left_frame)


        self.setLayout(self.mainLayout)
        # mainLayout

        self.show()  




class DataTabs():
    def __init__(self, tab, tabs, rows=3):
        self.tab = tab
        self.tab.clear()  

        self.generate_tab_content(tabs,rows=rows)

    def generate_tab_content(self, tabs,rows=3):
            for t in tabs.keys():
                new_tab=QWidget()
                layout = QVBoxLayout()
                table = QTableWidget()
                table.setRowCount(1)
                table.setColumnCount(rows)

                header = table.horizontalHeader()       
                header.setSectionResizeMode(0, QHeaderView.Stretch)
                for r in range(rows):
                    header.setSectionResizeMode(r, QHeaderView.ResizeToContents)

                count = 0
                for d in tabs[t].keys():
                    if rows == 3:
                        if (abs(tabs[t][d]['sum'])) > 0:
                            table.setItem(count,0,QTableWidgetItem(d))
                            table.setItem(count,1,QTableWidgetItem("{:10.2f} Eur".format(tabs[t][d]['sum'])))
                            detail_button = QPushButton("Details")
                            detail_button.clicked.connect(self.make_show_details(tabs[t][d]['entries'],str(d)+" in "+str(t)))
                            table.setCellWidget(count,2,detail_button)
                            count += 1
                            table.setRowCount(count+1)
                    else:
                        if (abs(tabs[t][d]['sum'][0])) > 0:
                            table.setItem(count,0,QTableWidgetItem(d))
                            count_s = 1
                            for sum_entry in tabs[t][d]['sum']:
                                table.setItem(count,count_s,QTableWidgetItem("{:10.2f} Eur".format(sum_entry)))
                                count_s +=1
                            detail_button = QPushButton("Details")
                            detail_button.clicked.connect(self.make_show_details(tabs[t][d]['entries'],str(d)+" in "+str(t)))
                            table.setCellWidget(count,count_s,detail_button)
                            count += 1
                            table.setRowCount(count+1)


                table.sortItems(1)
                table.show()
                layout.addWidget(table)
                new_tab.setLayout(layout)
                if type(t) is str:
                    self.tab.addTab(new_tab,t)    
                else:
                    self.tab.addTab(new_tab,analyse.get_month(t))                     
            self.tab.setCurrentIndex(len(tabs.keys())-1)


    def make_show_details(self,to_show,title):
        def show_details():
            # if date =="all":
            #     to_show = entries
            # else:
            #     to_show = [d for d in entries if (d[0][3:] == date)]                
            self.dw = Detail_Window(to_show,title)
            self.dw.show()
        return show_details 
