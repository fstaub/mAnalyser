"""
===============
Embedding In Tk
===============

"""


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
        QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator, QButtonGroup,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget,QMainWindow,QToolButton,QMenu,QTableWidgetItem,QHeaderView, QFrame)
from PyQt5.QtGui import QIcon, QStandardItemModel
from PyQt5.QtCore import Qt


import plot
import numpy as np

import random

class Detail_Window(QDialog):
    ''' Creates a new window which displays in a table 
        all items belonging to a given category/month  
    '''
    def __init__(self, data, target):
        super().__init__()
        # self.frame = QGroupBox("Details")
        layout = QVBoxLayout()
        # self.table = QTableWidget()
        target.table.setRowCount(1)
        target.table.setColumnCount(3)
        # self.target = target

        header = target.table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)

        # self.title = title
        # self.left = 2
        # self.top = 2        
        # self.width = 600
        # self.height = 600

        # self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)

        count = 0
        for e in data:
            target.table.setItem(count,0,QTableWidgetItem(e[0].strftime("%d.%m.%Y")))
            target.table.setItem(count,1,QTableWidgetItem(str(e[1])) )     
            target.table.setItem(count,2,QTableWidgetItem("{:10.2f} Eur".format(e[2])))  
            count += 1
            target.table.setRowCount(count+1)
        target.table.show()
        # layout.addWidget(self.table)
        # self.target.frame_details.clear()
        # self.target.frame_details.setLayout(layout)

class Data_Window(QDialog):
    ''' Creates a new window which displays in a table 
        all items belonging to a given category/month  
    '''
    def __init__(self, df, title):
        super().__init__()
        # self.frame = QGroupBox("Details")
           

        self.title = title
        self.left = 2
        self.top = 2        
        self.width = 1000
        self.height = 600

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.generate_tables(df)
    
    def generate_tables(self, df):
        self.layout = QVBoxLayout()

        self.tabs = QTabWidget()

        keys = df['Category1'].unique()

        # for i in all_data:
        #   for k in i.keys():   
        # # Add tabs
        #     new_tab = QWidget()
        #     self.tabs.addTab(new_tab, k)
        #     tab_layout = QVBoxLayout()
        #     table = QTableWidget()
        #     table.setRowCount(1)
        #     table.setColumnCount(3)
        #     header = table.horizontalHeader()       
        #     header.setSectionResizeMode(0, QHeaderView.Stretch)
        #     header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        #     header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        #     count = 0
        #     for e in i[k]:
        #         table.setItem(count,0,QTableWidgetItem(e[0].strftime("%d.%m.%Y")))
        #         table.setItem(count,1,QTableWidgetItem(str(e[1])) )     
        #         table.setItem(count,2,QTableWidgetItem("{:10.2f} Eur".format(e[2])))  
        #         count += 1
        #         table.setRowCount(count+1)
        #     table.show()
        #     tab_layout.addWidget(table)
        #     new_tab.setLayout(tab_layout)   
        # 
        for k in keys:   
        # Add tabs
            new_tab = QWidget()
            self.tabs.addTab(new_tab, k)
            tab_layout = QVBoxLayout()
            table = QTableWidget()
            table.setRowCount(1)
            table.setColumnCount(4)
            header = table.horizontalHeader()       
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

            count = 0

            new_df=df[df['Category1'] == k].sort_values(by=['Date'])
            for index, e in new_df.iterrows():
                table.setItem(count,0,QTableWidgetItem(e['Date'].strftime("%d.%m.%Y")))
                table.setItem(count,1,QTableWidgetItem(str(e['Description'])) )     
                table.setItem(count,2,QTableWidgetItem(str(e['Category0'])) )     
                table.setItem(count,3,QTableWidgetItem("{:10.2f} Eur".format(e['Amount'])))  
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

        self.tabs = QTabWidget()
        self.tab_plots = QWidget()
        self.tab_data = QWidget()       
        self.tab_data_tabs = QTabWidget()       
        self.frame_details = QWidget()

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Plots
        plots_layout = QVBoxLayout()
        self.add_plot_canvas_new4(arg1, arg2, arg3, arg4)                                    
        plots_layout.addWidget(self.canvas_frame)
        self.tab_plots.setLayout(plots_layout)
        self.tabs.addTab(self.tab_plots, "Plots")

        # # data
        data_layout = QHBoxLayout()
        data_layout.addWidget(self.tab_data_tabs)       
        self.frame_layout = QHBoxLayout()
        self.table = QTableWidget()      
        self.frame_layout.addWidget(self.table)
        self.frame_details.setLayout(self.frame_layout)

        data_layout.addWidget(self.frame_details)  
        self.tab_data.setLayout(data_layout)
        self.tabs.addTab(self.tab_data, "Data")


        layout.addWidget(self.tabs)
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

        frame_top.setLayout(layout_top)
        frame_down.setLayout(layout_down)
        layout.addWidget(frame_top)
        layout.addWidget(frame_down)

        self.canvas_frame.setLayout(layout)           


class ConfigWindow(QDialog):
    ''' opens a new window to configure/select 
        what keys are included in the plots
    '''
    def __init__(self, parent, keys, titles, ref_object, depth=1):
        super().__init__()
        # settings_frame = QGroupBox("Configuration")
        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        self.single_tabs = []
        self.boxes = []
        self.box_labels = []
        self.ref = ref_object
        self.is_selected = ref_object.is_included
        self.parent = parent

        self.parent_boxes = []
        self.child_boxes = []
        self.parent_labels = []
        self.child_labels = []

        if depth == 2:
            self.checked = set(self.is_selected[0]+self.is_selected[1])


        if (depth==1):
            for i, k in enumerate(keys):
                self.single_tabs.append(QWidget())
                self.tabs.addTab(self.single_tabs[-1], titles[i])
                tab_layout = QVBoxLayout(self)
                for  kk in k.keys():
                    self.boxes.append(QCheckBox(kk,self))
                    self.box_labels.append(kk)
                    if kk in self.is_selected:
                        self.boxes[-1].setChecked(True)
                    tab_layout.addWidget(self.boxes[-1])  
                self.single_tabs[-1].setLayout(tab_layout)
        else:
            for i, k in enumerate(keys):
                self.single_tabs.append(QWidget())
                self.tabs.addTab(self.single_tabs[-1], titles[i])
                tab_layout = QVBoxLayout(self)
                tree    = QTreeWidget ()
                tree.itemChanged.connect(self.handleItemChanged)                 
                headerItem  = QTreeWidgetItem()
                item    = QTreeWidgetItem()
                
                for  kk in k[1].keys():
                    self.parent_boxes.append(QTreeWidgetItem(tree))
                    self.parent_labels.append(kk)
                    self.parent_boxes[-1].setText(0, kk)
                    self.parent_boxes[-1].setFlags(self.parent_boxes[-1].flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                    for k2 in k[1][kk]:
                        self.child_boxes.append(QTreeWidgetItem(self.parent_boxes[-1]))
                        self.child_labels.append(k2)
                        self.child_boxes[-1].setFlags(self.child_boxes[-1].flags() | Qt.ItemIsUserCheckable)
                        self.child_boxes[-1].setText(0, k2)
                        if kk in self.is_selected[1]:
                            self.child_boxes[-1].setCheckState(0, Qt.Checked)
                        else:
                            self.child_boxes[-1].setCheckState(0, Qt.Unchecked)
                tab_layout.addWidget(tree)
                self.single_tabs[-1].setLayout(tab_layout)


        buttons = QGroupBox("")
        button_layout = QHBoxLayout()        
        self.button_ok=QPushButton('Speichern')
        if (depth==1):
            self.button_ok.clicked.connect(self.on_pushButton_ok)
        else:
            self.button_ok.clicked.connect(self.on_pushButton_ok_depth2)
        button_layout.addWidget(self.button_ok)

        self.button_cancel=QPushButton('Schließen')
        self.button_cancel.clicked.connect(self.on_pushButton_cancel)
        button_layout.addWidget(self.button_cancel)
        buttons.setLayout(button_layout)

        layout.addWidget(self.tabs)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def handleItemChanged(self, item, column):
        if item.checkState(column) == Qt.Checked:
            self.checked.add(item.text(column))
        elif item.checkState(column) == Qt.Unchecked:
            if item.text(column) in self.checked:
                self.checked.remove(item.text(column))

    def on_pushButton_ok(self):
        self.is_selected = []
        for i, n in zip(self.boxes, self.box_labels):
            if i.isChecked() is True:
                self.is_selected.append(n)
        self.ref.is_included = self.is_selected
        self.parent.on_pushButton_start()

    def on_pushButton_ok_depth2(self):
        self.is_selected = [[],[]]
        for n in self.parent_labels:
            if n in self.checked:
                self.is_selected[1].append(n)
        for n in self.child_labels:
            if n in self.checked:
                self.is_selected[0].append(n)

        self.ref.is_included = self.is_selected
        self.parent.on_pushButton_start()
 

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

def QColumn3(w1,w2,w3):
        ''' command to arrange three given widgets in a line'''
        group = QGroupBox()
        layout = QHBoxLayout()
        layout.addWidget(w1)
        layout.addWidget(w2)
        layout.addWidget(w3)
        group.setLayout(layout)
        return group           


class OptionsWidget(QWidget):
    ''' main class to create the tabs containing the
        different options to steer the analysis'''
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.layout = QGridLayout()
        self.group = QGroupBox()
        self.add_contents()
        self.group.setLayout(self.layout)
        self.setLayout(self.layout)

    def add_contents(self):
        pass 

    def add_start_button(self, h):
        pushButton = QPushButton("Start")
        pushButton.clicked.connect(self.on_pushButton_start)
        self.layout.addWidget(pushButton, h, 0, 2, 3)

    def add_detail_button(self, h):
        pushButton = QPushButton("Details")
        pushButton.clicked.connect(self.on_pushButton_details)
        self.layout.addWidget(pushButton, h, 0, 2, 3)        

    def add_time_period(self, h):
        inner_group = QGroupBox()
        inner_layout = QGridLayout()
        self.ComboBoxStart = QComboBox()
        for i,key in enumerate(self.parent.all_dates):
            self.ComboBoxStart.addItem(key)
        inner_layout.addWidget(self.ComboBoxStart, 0, 0)

        inner_layout.addWidget(QLabel("-"), 0, 1)            
        
        self.ComboBoxEnd = QComboBox()
        for i,key in enumerate(self.parent.all_dates):
            self.ComboBoxEnd.addItem(key)
        self.ComboBoxEnd.setCurrentIndex(len(self.parent.all_dates)-1)
        inner_layout.addWidget(self.ComboBoxEnd, 0, 2)
        inner_group.setLayout(inner_layout)
        self.layout.addWidget(QLabel("Zeitraum"), h, 0)
        self.layout.addWidget(inner_group, h, 1, 1, 2)
        # self.layout.addWidget(QColumn(QLabel("Zeitraum"),inner_group)) 
        # 
        newl = QLabel()
        newl.setFrameStyle(QFrame.HLine )
        self.layout.addWidget(newl, h+1, 0, 1, 3)


    def add_configure(self,h):
        pushButton = QPushButton("Auswahl")
        pushButton.clicked.connect(self.on_pushButton_config)
        # self.layout.addWidget(QColumn(QLabel("Kategorien"), pushButton))
        self.layout.addWidget(QLabel("Kategorien"), h, 0)
        self.layout.addWidget(pushButton, h, 1, 1, 2)

        newl = QLabel()
        newl.setFrameStyle(QFrame.HLine )
        self.layout.addWidget(newl, h+1, 0, 1, 3)


    def add_radio_log(self, h, lines=1):	
        plot1_group=QButtonGroup(QWidget(self)) 
        self.radioPlot1 = QRadioButton("Linear")	 
        self.radioPlot2 = QRadioButton("Log")	
        plot1_group.addButton(self.radioPlot1) 
        plot1_group.addButton(self.radioPlot2) 
        self.radioPlot1.setChecked(True) 	   
        # self.layout.addWidget(QColumn3(QLabel("Skala Plot 1"),self.radioPlot1, self.radioPlot2 ))        
        self.layout.addWidget(QLabel("Skala Plot 1"), h, 0)
        self.layout.addWidget(self.radioPlot1, h, 1)
        self.layout.addWidget(self.radioPlot2, h, 2)        
        if lines > 1:
            self.radioPlot1b = QRadioButton("Linear")	 
            self.radioPlot2b = QRadioButton("Log")	 
            self.radioPlot1b.setChecked(True) 	
            plot2_group=QButtonGroup(QWidget(self))            
            plot2_group.addButton(self.radioPlot1b) 
            plot2_group.addButton(self.radioPlot2b)                
            # self.layout.addWidget(QColumn3(QLabel("Skala Plot 2"),self.radioPlot1b, self.radioPlot2b))        
            self.layout.addWidget(QLabel("Skala Plot 2"), h+1, 0)
            self.layout.addWidget(self.radioPlot1b, h+1, 1)
            self.layout.addWidget(self.radioPlot2b, h+1, 2)    

        newl = QLabel()
        newl.setFrameStyle(QFrame.HLine )
        self.layout.addWidget(newl, h+2, 0, 1, 3)


    def add_radio_level(self, h):	
        self.radioLevel1 = QRadioButton("fein")	 
        self.radioLevel2 = QRadioButton("grob")	 
        self.radioLevel2.setChecked(True) 	   
        level_group=QButtonGroup(QWidget(self))            
        level_group.addButton(self.radioLevel1) 
        level_group.addButton(self.radioLevel2)                

        # self.layout.addWidget(QColumn(self.radioLevel1, self.radioLevel2 ))               
        self.layout.addWidget(QLabel("Zusammenfassung"), h, 0)
        self.layout.addWidget(self.radioLevel1, h, 1)
        self.layout.addWidget(self.radioLevel2, h, 2)

    def add_fine_category(self,h):
        self.ComboBoxFine = QComboBox()
        for i,key in enumerate(self.parent.KEYS.OUT[1]):
            self.ComboBoxFine.addItem(key)
            item = self.ComboBoxFine.model().item(i, 0)
            item.setCheckState(Qt.Unchecked)    

        newl = QLabel()
        newl.setFrameStyle(QFrame.HLine )
        self.layout.addWidget(newl, h+1, 0, 1, 3)             

        self.layout.addWidget(QLabel("Details"), h+2, 0)            
        self.layout.addWidget(self.ComboBoxFine, h+2, 1, 1, 2)   


    def on_pushButton_start(self):
        pass

    def on_pushButton_config(self):
        pass    

    def on_pushButton_details(self):
        pass          

    def set_dates(self):
        self.date_start = analyse.go_to_last_day(datetime.datetime.strptime(self.ComboBoxStart.currentText() ,"%m/%Y").date())
        self.date_end = analyse.go_to_last_day(datetime.datetime.strptime(self.ComboBoxEnd.currentText() ,"%m/%Y").date())
        
    
class InOutTab(OptionsWidget):
    def __init__(self, parent):
        super().__init__(parent)

    def add_contents(self):
        self.add_categories(0)
        self.add_configure(2)
        self.add_radio_level(4)        
        self.add_time_period(5)        
        self.add_radio_log(7,lines=2)
        # self.add_button_data(8)
        self.add_start_button(10)

        self.add_fine_category(11)
        self.add_detail_button(14)        


    def add_categories(self, h):
        self.ComboBox = QComboBox()
        for i,key in enumerate(['Einnahmen', 'Ausgaben']):
            self.ComboBox.addItem(key)
            item = self.ComboBox.model().item(i, 0)
            item.setCheckState(Qt.Unchecked)

        self.ComboBoxAccount = QComboBox()
        self.ComboBoxAccount.addItem("Alle")
        item = self.ComboBoxAccount.model().item(0, 0)        
        for i,key in enumerate(self.parent.DATA.names):
            self.ComboBoxAccount.addItem(key)
            item = self.ComboBoxAccount.model().item(i+1, 0)
            item.setCheckState(Qt.Unchecked)      

        self.layout.addWidget(QLabel("Geldfluss"), h, 0)            
        self.layout.addWidget(self.ComboBox, h, 1, 1, 2)            

        self.layout.addWidget(QLabel("Konto"), h+1, 0)            
        self.layout.addWidget(self.ComboBoxAccount, h+1, 1, 1, 2)   

        # new_frame = QFrame()         


        # self.layout.addWidget(QColumn(QLabel("Geldfluss"),self.ComboBox))
        # self.layout.addWidget(QColumn(QLabel("Konto"),self.ComboBoxAccount))

      


    def on_pushButton_config(self):
        self.cw = ConfigWindow(self, [self.parent.KEYS.IN, self.parent.KEYS.OUT], 
            ["Einnahmen","Ausgaben"], self.parent.KEYS, depth=2)
        self.cw.show()

    def update_data(self, target, df, keywords, level, start, end):
        use_data = analyse.last_entry_of_month_inout(df, keywords, level, start, end)
        data_tab = DataTabs(target, use_data)

    def on_pushButton_start(self):
        self.set_dates()

        if self.radioLevel1.isChecked():            
            level = 0
        else:
            level = 1


        if (self.ComboBox.currentText() == "Einnahmen"):
                all_keys = self.parent.KEYS.IN[level]
        else:
                all_keys = self.parent.KEYS.OUT[level]


        if (self.ComboBoxAccount.currentText() == "Alle"):
                used_data = self.parent.DATA.df_transactions
        else:
                print(self.ComboBoxAccount.currentText())
                used_data = self.parent.DATA.df_transactions[self.parent.DATA.df_transactions['Account']==self.ComboBoxAccount.currentText()]
        print("used_data", used_data)

        s_inout = self.ComboBox.currentText()

        selected_keys = [key for key  in all_keys.keys() if key in self.parent.KEYS.is_included[level]]
        arguments = [used_data, selected_keys, level, self.date_start, self.date_end]

        self.new_plot_window = NewPlotWindow( 
                arg1=["StackedBar" if self.radioPlot1.isChecked() else "StackedBarLog", 
                    *analyse.prepare_stacked_bar(*arguments), s_inout + " pro Monat"],
                arg3 = [],
                arg4=["PieChart", *analyse.prepare_pie_chart(*arguments), "Prozentuale Verteilung der " + s_inout], 
                arg2=["HorizontalBar" if  self.radioPlot1b.isChecked() else "HorizontalBarLog", 
                    *analyse.prepare_horizontal_bar(*arguments), "Durchschnittliche " + s_inout], 
                title="Plots")

        self.update_data(self.new_plot_window, *arguments)    

        self.new_plot_window.show()

    def on_pushButton_details(self):
        self.set_dates()

        level = 0
        all_keys = self.parent.KEYS.OUT[level]

        if (self.ComboBoxAccount.currentText() == "Alle"):
                used_data = self.parent.DATA.df_transactions
        else:
                used_data = self.parent.DATA.df_transactions[self.parent.DATA.df_transactions['Account']==self.ComboBoxAccount.currentText()]

        s_inout = self.ComboBox.currentText()

        selected_keys = [key for key  in all_keys.keys() if key in self.parent.KEYS.OUT[1][self.ComboBoxFine.currentText()]]
        arguments = [used_data, selected_keys, level, self.date_start, self.date_end]

        self.new_plot_window = NewPlotWindow( 
                arg1=["StackedBar" if self.radioPlot1.isChecked() else "StackedBarLog", 
                    *analyse.prepare_stacked_bar(*arguments), s_inout + " pro Monat"],
                arg3 = [],
                arg4=["PieChart", *analyse.prepare_pie_chart(*arguments), "Prozentuale Verteilung der " + s_inout], 
                arg2=["HorizontalBar" if  self.radioPlot1b.isChecked() else "HorizontalBarLog", 
                    *analyse.prepare_horizontal_bar(*arguments), "Durchschnittliche " + s_inout], 
                title="Plots")

        self.update_data(self.new_plot_window, *arguments)    

        self.new_plot_window.show()        

class AccountTab(OptionsWidget):
    def __init__(self, parent):
        super().__init__(parent)

    def add_contents(self):
        self.add_configure(1)                
        self.add_time_period(3)
        self.add_radio_log(5,lines=2)       
        self.add_start_button(7)

    def on_pushButton_config(self):
        to_dict = lambda x: {y: 1 for y in x}
        self.cw = ConfigWindow(self, [to_dict(self.parent.DATA.names)], 
            ["Konten"], self.parent.DATA)
        self.cw.show()

    def on_pushButton_start(self):
        self.set_dates()        

        arguments = [self.parent.DATA.df_acc, self.parent.DATA.is_included,
                self.date_start, self.date_end]

        if self.radioPlot1.isChecked():
            style1 = "StackedBar"
            style2 = "HorizontalBar"
        else:
            style1 = "StackedBarLog"
            style2 = "HorizontalBarLog"                


        self.new_plot_window = NewPlotWindow(
            arg1=["StackedBar" if self.radioPlot1.isChecked() else "StackedBarLog", *analyse.prepare_stacked_bar_accounts(*arguments), "Kontostände pro Monat"],
            arg2=["PlusMinusBar",*analyse.prepare_plusminus_bar(*arguments), "Monatliche Veränderungen"], 
            arg3=["HorizontalBar" if self.radioPlot1.isChecked() else "HorizontalBarLog" , *analyse.prepare_horizontal_bar_accounts(*arguments), "Letzte Kontostände"],                         
            arg4=["PieChart",*analyse.prepare_horizontal_bar_accounts(*arguments), "Prozentuale Verteilung des Vermögens"],
            title="Plots")
        self.new_plot_window.show()
        self.update_data(self.new_plot_window, *arguments)        

    def update_data(self, target, df,  keywords, start, end):
        use_data = analyse.last_entry_of_month_accounts(df, keywords, start, end)
        data_tab = DataTabs(target, use_data, rows=4)



class StockTab(OptionsWidget):
    def __init__(self, parent):
        super().__init__(parent)

    def add_contents(self):
        self.add_configure(1)         
        self.add_time_period(3)
        self.add_choice(5)       
        self.add_radio(7)       
        self.add_start_button(9)

    def add_choice(self, h):
        self.checkAktien = QCheckBox("Aktien")
        self.checkFonds = QCheckBox("Fonds")
        self.checkAktien.setChecked(True) 
        self.checkFonds.setChecked(True) 
        self.layout.addWidget(QLabel("Wertpapiere"), h, 0)        
        self.layout.addWidget(self.checkAktien, h, 1)
        self.layout.addWidget(self.checkFonds, h, 2 )

        newl = QLabel()
        newl.setFrameStyle(QFrame.HLine )
        self.layout.addWidget(newl, h+1, 0, 1, 3)


       

    def add_radio(self, h):	
        self.radioPlot2 = QRadioButton("Absolut")	 
        self.radioPlot1 = QRadioButton("Relativ")	 
        self.radioPlot2.setChecked(True) 	   
        # self.layout.addWidget(QColumn(self.radioPlot1, self.radioPlot2 ))
        self.layout.addWidget(QLabel("Veränderungen"), h, 0)
        self.layout.addWidget(self.radioPlot1, h, 1)
        self.layout.addWidget(self.radioPlot2, h, 2 )



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


        arguments_relative = [self.parent.DEPOT.df_depot, selected_keys,
                self.date_start, self.date_end, relativ]             

        arguments = [self.parent.DEPOT.df_depot, selected_keys,
                self.date_start, self.date_end]                

                             

        self.new_plot_window = NewPlotWindow(
            arg1=["ScatterPlot", *analyse.prepare_scatter_total_change_stocks(*arguments_relative), "Gesamte Veränderung des Depots"],
            arg2=["ScatterPlotBar", *analyse.prepare_scatter_daily_changes_stocks(*arguments_relative), "Tägliche Veränderung des Depots"],                                     
            arg3=["StackedBar", *analyse.prepare_stacked_bar_stocks(*arguments), "Absolute Zusammensetzung des Depots"], 
            arg4=["PieChart", *analyse.prepare_pie_total_stocks(*arguments), "Prozentuale Zusammensetzung des Depots"],
            title="Plots")
        self.new_plot_window.show()  
        self.update_data(self.new_plot_window, *arguments)          

    def update_data(self, target, df, keywords, start, end):
        use_data = analyse.last_entry_of_month_stocks(df, keywords, start, end)
        data_tab = DataTabs(target, use_data, rows=4)          


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

        df = self.DATA.df_transactions
        self.all_dates = sorted(analyse.generate_dates(
                    min(df[df['Date'] > datetime.date(2000,1,1)]['Date']), max(df['Date'])
                ))
       
        self.all_dates = [analyse.get_month(d) for d in self.all_dates]

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
        self.this_layout = QGridLayout()
        self.this_layout.addWidget(QLabel("Konten:"), 0, 0)
        self.this_layout.addWidget(QLabel(str(len(self.DATA.df_acc)) + " Kontobewegungen"), 0, 1)
        self.this_layout.addWidget(QLabel("Datensatz:"), 1, 0 )
        self.this_layout.addWidget(QLabel(str(len(self.DATA.df_transactions)) + " Kontobewegungen"), 1, 1)
        self.add_button_data()
        # self.data_main_tab = QTabWidget()
        # layout.addWidget(self.data_main_tab)
        # layout.addStretch()
        self.data_frame.setLayout(self.this_layout)  

    def add_button_data(self):   
        self.pushButton = QPushButton("Show Data")
        self.pushButton.clicked.connect(self.on_pushButton_data)
        self.this_layout.addWidget(self.pushButton, 2, 0, 1, 2)  


    def on_pushButton_data(self):
        # pass
        self.data_window = Data_Window(self.parent.DATA.df_transactions, "Input Data")
        self.data_window.show()           


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
    def __init__(self, target, tabs, rows=3):
        self.target = target
        self.tab = target.tab_data_tabs
        self.tab.clear()  
        self.generate_tab_content(tabs,rows=rows)

    def generate_tab_content(self, tabs,rows=3):
            for t in tabs.keys():
                new_tab = QWidget()
                layout = QVBoxLayout()
                table = QTableWidget()
                table.setRowCount(1)
                table.setColumnCount(rows)

                header = table.horizontalHeader()       
                header.setSectionResizeMode(0, QHeaderView.Stretch)
                for r in range(rows):
                    header.setSectionResizeMode(r, QHeaderView.ResizeToContents)

                count = 0
                summe  = [0 for r in range(rows-2)]
                sum2 = 0
                for d in tabs[t].keys():
                    if rows == 3:
                        if (abs(tabs[t][d]['sum'])) > 0:
                            table.setItem(count,0,QTableWidgetItem(d))
                            table.setItem(count,1,QTableWidgetItem("{:10.2f} Eur".format(tabs[t][d]['sum'])))
                            summe[0] += tabs[t][d]['sum']
                            detail_button = QPushButton("Details")
                            detail_button.clicked.connect(self.make_show_details(tabs[t][d]['entries'],self.target))
                            table.setCellWidget(count,2,detail_button)
                            count += 1
                            table.setRowCount(count+1)
                    else:
                        if (abs(tabs[t][d]['sum'][0])) > 0:
                            table.setItem(count,0,QTableWidgetItem(d))
                            count_s = 1
                            for i, sum_entry in enumerate(tabs[t][d]['sum']):
                                summe[i] += sum_entry
                                table.setItem(count,count_s,QTableWidgetItem("{:10.2f} Eur".format(sum_entry)))
                                count_s +=1
                            detail_button = QPushButton("Details")
                            detail_button.clicked.connect(self.make_show_details(tabs[t][d]['entries'],self.target))
                            table.setCellWidget(count,count_s,detail_button)
                            count += 1
                            table.setRowCount(count+1)
                    table.setItem(count,0,QTableWidgetItem("Gesamt"))
                    for r in range(rows-2):
                        table.setItem(count,r+1,QTableWidgetItem("{:10.2f} Eur".format(summe[r])))
                

                table.show()
                layout.addWidget(table)
                new_tab.setLayout(layout)
                if type(t) is str:
                    self.tab.addTab(new_tab,t)    
                else:
                    self.tab.addTab(new_tab,analyse.get_month(t))                     
            self.tab.setCurrentIndex(len(tabs.keys())-1)


    def make_show_details(self, to_show, target):
        def show_details():
            self.dw = Detail_Window(to_show,target)
            # self.dw.show()
        return show_details 
