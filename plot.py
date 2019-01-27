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
import matplotlib
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


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

bg_color = (0.3, 0.3, 0.3)
bbg_color = (0.1, 0.1, 0.1)
fg_color = (0.9, 0.9, 0.9)
title_color = (0.7, 0.7, 0.7)


class NewPlotCanvas(QMainWindow):
    def __init__(self, style, in_arg=[], parent=None, width=2, height=4):
        QMainWindow.__init__(self, parent)
        self.create_main_frame(style, width, height)

        if (style == "StackedBar"):
            self.on_draw_StackedBar(in_arg[0], in_arg[1], in_arg[2], in_arg[3])
        if (style == "StackedBarLog"):
            self.on_draw_StackedBar(in_arg[0], in_arg[1], in_arg[2], in_arg[3], log=True)            
        if (style == "LogLinear"):
            self.on_draw_LogLinear(in_arg[0], in_arg[1], in_arg[2], in_arg[3])            
        if (style == "PieChart"):
            self.on_draw_PieChart(in_arg[0], in_arg[1], in_arg[2])            
        if (style == "HorizontalBar"):
            self.on_draw_HorizontalBar(in_arg[0], in_arg[1], in_arg[2]) 
        if (style == "PlusMinusBar"):
            self.on_draw_PlusMinusBar(in_arg[0], in_arg[1], in_arg[2])                                  
        if (style == "HorizontalBarLog"):
            self.on_draw_HorizontalBar(in_arg[0], in_arg[1], in_arg[2], log=True)  
        if (style == "ScatterPlot"):
            self.on_draw_ScatterDatePlot(in_arg[0], in_arg[1], in_arg[2],bar=False)
        if (style == "ScatterPlotBar"):
            self.on_draw_ScatterDatePlot(in_arg[0], in_arg[1], in_arg[2],bar=True)

                  
    def create_main_frame(self, style, w, h):
        self.main_frame = QWidget()

        if (style == "PieChart"):
            self.fig = Figure(figsize=(w, h), tight_layout=True, dpi=100, facecolor=bg_color, edgecolor=bg_color)
        else: 
            self.fig = Figure(figsize=(w, h), tight_layout=True, dpi=100, facecolor=bbg_color, edgecolor=bg_color)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.canvas.setFocusPolicy( Qt.ClickFocus )
        self.canvas.setFocus()
        # self.canvas.setWidth(w)
        self.canvas.updateGeometry()

        if (style == "StackedBar"):
            self.canvas.mpl_connect("motion_notify_event", self.hover_bar)
        if (style == "StackedBarLog"):
            self.canvas.mpl_connect("motion_notify_event", self.hover_bar)            
        if (style == "HorizontalBar"):
            self.canvas.mpl_connect("motion_notify_event", self.hover_bar) 

        vbox = QVBoxLayout()
        vbox.addWidget(self.canvas)         # the matplotlib canvas
        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)

    def on_draw_StackedBar(self, data, labels, dates, ptitle, log=False):
        bot = [0 for x in data]
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        self.sc = []
        self.all_label = []
        dimw = 25
        if (log is True):
            dimw = dimw/len(labels)
        for i in range(len(labels)):
            self.label_store={}
            y = [d[i] for d in data]
            if (log is True):
                new_dates = [d +datetime.timedelta(days=2*(int(len(labels)/2)+i)) for d in dates]
            else:
                new_dates = dates
            self.sc.append(self.axes.bar(new_dates , y, dimw, color=use_colors[i], bottom=bot, label=labels[i], alpha=0.75))
            for bar in self.sc[-1]:
                  self.label_store[bar] = labels[i] 
            if log is False:
                bot = [bot[j] + y[j] for j in range(len(y))]
            self.all_label.append(self.label_store)

        if (log is True):
            self.axes.set_yscale('log')

        self.axes.set_title(ptitle, color=title_color)

        self.axes.set_facecolor(bg_color)
        self.axes.xaxis.set_tick_params(color=fg_color, labelcolor=fg_color)
        self.axes.yaxis.set_tick_params(color=fg_color, labelcolor=fg_color)
        for spine in self.axes.spines.values():
            spine.set_color(fg_color)       
        self.axes.grid(color='gray', linestyle='-', linewidth=0.2)                 

        self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))  
        self.axes.xaxis.set_major_locator(mdates.MonthLocator()) 
        self.fig.autofmt_xdate()

        self.annot = self.axes.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                            bbox=dict(fc="w"),
                            arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)
        self.canvas.draw() 

    def on_draw_LogLinear(self, data, labels,ptitle, dates):
        bot = [0 for x in data]

        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        self.sc = []
        self.all_label = []
        for i in range(len(labels)):
            self.label_store={}
            y = [d[i] for d in data]
            self.sc.append(self.axes.plot(dates, y, color=use_colors[i], label=labels[i]))

        # self.annot = self.axes.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
        #                     bbox=dict(fc="w"),
        #                     arrowprops=dict(arrowstyle="->"))
        # self.annot.set_visible(False)

        self.axes.set_facecolor(bg_color)
        self.axes.xaxis.set_tick_params(color=fg_color, labelcolor=fg_color)
        self.axes.yaxis.set_tick_params(color=fg_color, labelcolor=fg_color)
        for spine in self.axes.spines.values():
            spine.set_color(fg_color)       
        self.axes.grid(color='gray', linestyle='-', linewidth=0.2)        

        self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))  
        self.axes.xaxis.set_major_locator(mdates.MonthLocator()) 
        self.fig.autofmt_xdate()

        self.axes.set_yscale('log') 
        self.axes.set_title(ptitle, color=title_color)
        self.canvas.draw()                 

    def on_draw_PieChart(self,data, labels, ptitle):
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)
        # self.axes.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


        def func(pct, allvals):
            absolute = int(pct/100.*np.sum(allvals))
            if pct > 5:
                return "{:.1f}%".format(pct)
            else:
                return ""

        wedges, texts, autotexts = self.axes.pie(data, autopct=lambda pct: func(pct, data),
                                    textprops=dict(color="w"), colors=use_colors)
        
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),
                  bbox=bbox_props, zorder=0, va="center")
        for i, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1)/2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ang)
            kw["arrowprops"].update({"connectionstyle": connectionstyle, "color": fg_color})
            if 0.001 < (data[i]/np.sum(data)):
                if (data[i]/np.sum(data)) < 0.05:
                    this_label = str(labels[i])[:min([15,len(labels[i])])]+" "+"{:.1f}%".format(100*data[i]/np.sum(data))
                elif (data[i]/np.sum(data)) >= 0.05:
                    this_label = (labels[i])[:min([15,len(labels[i])])]
                self.axes.annotate(this_label, xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                     horizontalalignment=horizontalalignment, **kw)
        self.axes.set_title(ptitle, color=title_color)
        self.canvas.draw()  

    def on_draw_HorizontalBar(self, data, labels, ptitle, log=False): 
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

        self.axes.set_facecolor(bg_color)
        self.axes.xaxis.set_tick_params(color=fg_color, labelcolor=fg_color)
        self.axes.yaxis.set_tick_params(color=fg_color, labelcolor=fg_color)
        for spine in self.axes.spines.values():
            spine.set_color(fg_color)       
        self.axes.grid(color='gray', linestyle='-', linewidth=0.2)        

        for i,k in enumerate(labels):
            self.axes.text(3.5, x[i]-0.2, str(k)+" ("+str(int(data[i]))+" Eur)",size=10)
        self.annot = self.axes.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                            bbox=dict(fc="w"),
                            arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)      
        self.axes.set_title(ptitle, color=title_color)
        self.canvas.draw()          

    def on_draw_PlusMinusBar(self, data, dates, ptitle):
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)   

        x = 3*np.arange(len(data))
        b = self.axes.bar(dates, data, 20, color=['green' if i>0 else 'red' for i in data])

        self.axes.set_facecolor(bg_color)
        self.axes.xaxis.set_tick_params(color=fg_color, labelcolor=fg_color)
        self.axes.yaxis.set_tick_params(color=fg_color, labelcolor=fg_color)
        for spine in self.axes.spines.values():
            spine.set_color(fg_color)       
        self.axes.grid(color='gray', linestyle='-', linewidth=0.2)


        self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))  
        self.axes.xaxis.set_major_locator(mdates.MonthLocator()) 
        self.fig.autofmt_xdate()

        self.axes.set_title(ptitle, color=title_color)

        # self.axes.xticks(x,[d.replace(".20","/") for d in dates])
        self.canvas.draw()                     

    def on_draw_ScatterDatePlot(self, data, dates, ptitle, bar = False):
        self.fig.clear()
        self.axes = self.fig.add_subplot(111)  
        self.fig.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
        self.fig.gca().xaxis.set_major_locator(mdates.MonthLocator()  )
        if bar:
            self.axes.bar(dates, data, color=['green' if i>0 else 'red' for i in data])
        else:
            self.axes.scatter(dates, data, s=3,c=['green' if i>0 else 'red' for i in data])
        self.axes.grid(color='gray', linestyle='-', linewidth=0.2)

        self.axes.set_facecolor(bg_color)
        self.axes.xaxis.set_tick_params(color=fg_color, labelcolor=fg_color)
        self.axes.yaxis.set_tick_params(color=fg_color, labelcolor=fg_color)
        for spine in self.axes.spines.values():
            spine.set_color(fg_color)       
        self.axes.grid(color='gray', linestyle='-', linewidth=0.2)        

        self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))  
        self.axes.xaxis.set_major_locator(mdates.MonthLocator()) 
        self.fig.autofmt_xdate()
        self.axes.set_title(ptitle, color=title_color)
        self.canvas.draw()                     

    def update_annot_bar(self,bar,label):
        x = bar.get_x()+bar.get_width()/2.
        y = bar.get_y()+bar.get_height()/2
        y_val = bar.get_height()
        self.annot.xy = (x,y)
        text = label+"\n" + "({:.2f}Eur)".format(y_val) #"#self.label_store[bar]
        self.annot.set_text(text)
        self.annot.get_bbox_patch().set_alpha(0.4)        


    def hover_bar(self,event):
        vis = self.annot.get_visible()
        if event.inaxes == self.axes:
            for s, l in zip(self.sc, self.all_label):  
                for bar in s:  
                    cont, ind = bar.contains(event)
                    if cont:
                        self.update_annot_bar(bar, l[bar])
                        self.annot.set_visible(True)
                        self.fig.canvas.draw_idle()
                else:
                    if vis:
                        self.annot.set_visible(False)
                        self.fig.canvas.draw_idle()

