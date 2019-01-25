import numpy as np
import math
import analyse
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplcursors

from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget,QMainWindow,QToolButton,QMenu,QTableWidgetItem,QHeaderView)
from PyQt5.QtGui import QIcon, QStandardItemModel
from PyQt5.QtCore import Qt

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar



# use_colors = [
#      (0.1, 0.2, 0.5),
#      (0.5, 0.1, 0.5),
#      (0.5, 0.5, 0.5),
#      (0.9, 0.9, 0.9),
#      (0.9, 0.1, 0.1),
#      (0.1, 0.9, 0.1),
#      (0.1, 0.1, 0.9),
#      (0.9, 0.9, 0.1),
#      (0.9, 0.1, 0.9),
#      (0.1, 0.9, 0.9),
#      (0.8, 0.5, 0.2),
#      (0.7, 0.3, 0.4),
#      (0.4, 0.3, 0.7),
#      (0.4, 0.7, 0.3),
#      (0.1, 0.1, 0.1),
#      (0.9, 0.5, 0.7)
# ]

use_colors = [
   (0.561,0.188,0.357),
   (0.839,0.561,0.686),
#    (0.702,0.349,0.51),
   (0.42,0.071,0.231),
   (0.278,0,0.129),
   (0.447,0.612,0.204),
   (0.792,0.918,0.612),
#    (0.608,0.765,0.384),
   (0.302,0.459,0.078),
   (0.18,0.306,0),
   (0.42,0.184,0.549),
   (0.702,0.525,0.796),
#    (0.525,0.306,0.643),
   (0.322,0.094,0.447),
   (0.212,0.016,0.318),
   (0.824,0.824,0.243),
   (1,1,0.639),
#    (0.965,0.965,0.431),
   (0.671,0.671,0.11),
   (0.475,0.475,0),

      (0.322,0.094,0.447),
   (0.212,0.016,0.318),
   (0.824,0.824,0.243),
   (1,1,0.639),
#    (0.965,0.965,0.431),
   (0.671,0.671,0.11),
   (0.475,0.475,0)
]

class NewPlotCanvas(QMainWindow):
    def __init__(self, style, in_arg=[], parent=None, width=5, height=4):
    #  def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        #self.x, self.y = self.get_data()
        self.create_main_frame(style, width, height)

        if (style == "StackedBar"):
            self.on_draw_StackedBar(in_arg[0],in_arg[1], width, height)
        if (style == "LogLinear"):
            self.on_draw_LogLinear(in_arg[0],in_arg[1], width, height)            
        if (style == "PieChart"):
            print("Pie", in_arg[0])
            self.on_draw_PieChart(in_arg[0],in_arg[1], width, height)            
        if (style == "HorizontalBar"):
            self.on_draw_HorizontalBar(in_arg[0],in_arg[1], width, height) 
        if (style == "PlusMinusBar"):
            self.on_draw_PlusMinusBar(in_arg[0],in_arg[1], width, height)                                  
        if (style == "HorizontalBarLog"):
            self.on_draw_HorizontalBar(in_arg[0],in_arg[1], width, height, log=True)  
        if (style == "ScatterPlot"):
            self.on_draw_ScatterDatePlot(in_arg[0],in_arg[1], width, height, bar=False)
        if (style == "ScatterPlotBar"):
            self.on_draw_ScatterDatePlot(in_arg[0],in_arg[1], width, height, bar=True)

                  

                                     

    def create_main_frame(self, style, w, h):
        self.main_frame = QWidget()

        self.fig = Figure((w,h ), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.canvas.setFocusPolicy( Qt.ClickFocus )
        self.canvas.setFocus()

        if (style == "StackedBar"):
            self.canvas.mpl_connect("motion_notify_event", self.hover)
        if (style == "HorizontalBar"):
            self.canvas.mpl_connect("motion_notify_event", self.hover) 
        # if (style == "HorizontalBar"):
        #     self.on_draw_HorizontalBar(in_arg[0],in_arg[1], width, height)                       

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)         # the matplotlib canvas
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)

    def on_draw_StackedBar(self, data, labels, width, height):
        x = 3*np.arange(len(data))
        bot = [0 for x in data]

        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        self.sc = []
        self.all_label = []
        for i in range(len(labels)):
            self.label_store={}
            y = [d[i] for d in data]
            self.sc.append(self.axes.bar(x, y, 2, color=use_colors[i], bottom=bot, label=labels[i]))
            for bar in self.sc[-1]:
                  self.label_store[bar] = labels[i] 
            bot = [bot[j] + y[j] for j in range(len(y))]
            self.all_label.append(self.label_store)

        self.annot = self.axes.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                            bbox=dict(fc="w"),
                            arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)
        self.fig.set_size_inches(width, height)
        self.canvas.draw() 

    def on_draw_LogLinear(self, data, labels, width, height):
        x = 3*np.arange(len(data))
        bot = [0 for x in data]

        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        self.sc = []
        self.all_label = []
        for i in range(len(labels)):
            self.label_store={}
            y = [d[i] for d in data]
            self.sc.append(self.axes.plot(x, y, color=use_colors[i], label=labels[i]))
            # for bar in self.sc[-1]:
            #       self.label_store[bar] = labels[i] 
            # bot = [bot[j] + y[j] for j in range(len(y))]
            # self.all_label.append(self.label_store)

        # self.annot = self.axes.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
        #                     bbox=dict(fc="w"),
        #                     arrowprops=dict(arrowstyle="->"))
        # self.annot.set_visible(False)
        self.axes.set_yscale('log') 
        self.fig.set_size_inches(width, height)        
        self.canvas.draw()                 

    def on_draw_PieChart(self,data, labels, width, height):
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        self.axes.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


        def func(pct, allvals):
            absolute = int(pct/100.*np.sum(allvals))
            if pct > 2:
                return "{:.1f}%".format(pct)
            else:
                return ""

        wedges, texts, autotexts = self.axes.pie(data, autopct=lambda pct: func(pct, data),
                                    textprops=dict(color="w"), colors=use_colors)
        # target.set_size_inches(w,h)                                  
        self.annot = self.axes.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                            bbox=dict(fc="w"),
                            arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)
        self.fig.set_size_inches(width, height)        
        self.canvas.draw()  

    def on_draw_HorizontalBar(self, data, labels, width, height, log=False): 
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)        

        x = np.arange(len(data))
        # val = [abs(sum([x for x in y.values()]))/(1*len(dates)) for y in data]
        self.sc = []
        self.all_label = []
        for i in range(len(x)):
            self.label_store={}
            self.sc.append(self.axes.barh(x[i], data[i], 0.75, color=use_colors[i]))
            for bar in self.sc[-1]:
                  self.label_store[bar] = labels[i]   
            self.all_label.append(self.label_store)

        if (log):
            self.axes.set_xscale('log')    
        self.axes.tick_params(axis='y',  which='both', left=False, right=False, labelleft=False)

        for i,k in enumerate(labels):
            self.axes.text(3.5, x[i]-0.2, str(k)+" ("+str(int(data[i]))+" Eur)",size=10)
        self.annot = self.axes.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                            bbox=dict(fc="w"),
                            arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)      
        self.fig.set_size_inches(width, height)              
        self.canvas.draw()          

    def on_draw_PlusMinusBar(self, data, dates,  width, height):
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)   

        x = 3*np.arange(len(data))
        b = self.axes.bar(x, data, 2, color=['green' if i>0 else 'red' for i in data])

        self.axes.set_xticks(x + 1, dates)    
        # self.axes.set_ylabel('Euro')

        # self.axes.xticks(x,[d.replace(".20","/") for d in dates])
        self.fig.set_size_inches(width, height)
        self.canvas.draw()                     

    def on_draw_ScatterDatePlot(self, data, dates, width, height, bar = False):
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)  
        self.fig.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
        self.fig.gca().xaxis.set_major_locator(mdates.MonthLocator()  )
        if bar:
            self.axes.bar(dates, data, color=['green' if i>0 else 'red' for i in data])
        else:
            self.axes.scatter(dates, data, s=3,c=['green' if i>0 else 'red' for i in data])
        self.axes.grid(color='gray', linestyle='-', linewidth=0.2)
        # self.axes.gcf().autofmt_xdate()    

        self.fig.set_size_inches(width, height)
        self.canvas.draw()                     

    def update_annot(self,bar,label):
        x = bar.get_x()+bar.get_width()/2.
        y = bar.get_y()+bar.get_height()/2
        y_val = bar.get_height()
        self.annot.xy = (x,y)
        text = label+"\n" + "({:.2f}Eur)".format(y_val) #"#self.label_store[bar]
        self.annot.set_text(text)
        self.annot.get_bbox_patch().set_alpha(0.4)        


    def hover(self,event):
        vis = self.annot.get_visible()
        if event.inaxes == self.axes:
            for s, l in zip(self.sc, self.all_label):  
                for bar in s:  
                    cont, ind = bar.contains(event)
                    if cont:
                        self.update_annot(bar, l[bar])
                        self.annot.set_visible(True)
                        self.fig.canvas.draw_idle()
                else:
                    if vis:
                        self.annot.set_visible(False)
                        self.fig.canvas.draw_idle()

