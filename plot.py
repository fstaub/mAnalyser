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



use_colors = [
     (0.1, 0.2, 0.5),
     (0.5, 0.1, 0.5),
     (0.5, 0.5, 0.5),
     (0.9, 0.9, 0.9),
     (0.9, 0.1, 0.1),
     (0.1, 0.9, 0.1),
     (0.1, 0.1, 0.9),
     (0.9, 0.9, 0.1),
     (0.9, 0.1, 0.9),
     (0.1, 0.9, 0.9),
     (0.8, 0.5, 0.2),
     (0.7, 0.3, 0.4),
     (0.4, 0.3, 0.7),
     (0.4, 0.7, 0.3),
     (0.1, 0.1, 0.1),
     (0.9, 0.5, 0.7)
]

# def formatter(**kwargs):
#         dist = abs(np.array(x) - kwargs['x'])
#         i = dist.argmin()
#         labels = attendance if kwargs['bottom'] == 0 else attendance2
#         return '\n'.join(labels[i])

# def HistPlot_Account(in_data, start, end, bar, w, h):
#     dates = analyse.find_dates2(in_data)
#     dates = [d for d in dates if ( datetime.datetime.strptime(end, "%m/%Y").date() >=  datetime.datetime.strptime(d, "%m/%Y").date()>=  datetime.datetime.strptime(start, "%m/%Y").date())]

#     data = []
#     for x in list(in_data.values()):
#         data.append([abs(sum(x[d] for d in dates[:i])) for i in range(1,len(dates)+1)])
    
#     data = list(np.array(data).T)
#     labels = list(in_data.keys())

#     return HistPlot(data, dates, labels, bar, w, h)

# def HistPlot_Changes(in_data, start, end, w, h):
#     dates = analyse.generate_dates(start, end)
#     data = analyse.group_data_by_month(in_data, dates)
#     out = []
#     for x in data.keys():
#         out += [sum(x['sum'] for x in list(data[x].values()))]


#     # dates = [d for d in dates if ( datetime.datetime.strptime(end, "%m/%Y").date() >=  datetime.datetime.strptime(d, "%m/%Y").date()>=  datetime.datetime.strptime(start, "%m/%Y").date())]

#     # data = []
#     # for x in list(in_data.values()):
#     #     data.append([abs(sum(x[d] for d in dates[:i])) for i in range(1,len(dates)+1)])
    
#     # data = [sum(d) for d in data]
#     print(out, dates)
#     return BarPlot(out, dates)    

# def HistPlot_InOut(in_data, keywords, start, end, bar, w, h):
#     sum_all = analyse.summary_months(in_data, list(keywords.keys()))
#     dates = analyse.find_dates(sum_all)
#     dates = [d for d in dates if ( datetime.datetime.strptime(end, "%m/%Y").date() >=  datetime.datetime.strptime(d, "%m/%Y").date()>=  datetime.datetime.strptime(start, "%m/%Y").date())]

#     arranged = analyse.arrange_sum_by_data2(sum_all,dates)
#     data = [[abs(x) for x in y] for y in arranged]
#     labels = list(in_data.keys())

#     return HistPlot(data, dates, labels, bar, w, h)    

# def HistPlot(data, dates, labels, bar, width, height):
#     dim = len(data[0])
#     w = 2.
#     # dimw = w / dim
#     dimw = 2
#     target, ax = plt.subplots()
#     x = 3*np.arange(len(data))
#     bot = [0 for x in data]
#     for i in range(len(labels)):
#         y = [d[i] for d in data]
#         print(i, x, y, labels[i])
#         if (bar):
#             b = ax.bar(x, y, dimw, color=use_colors[i], bottom=0,label=labels[i])
#             bot += y
#         else:    
#             b = ax.plot(x, y, color=use_colors[i], label=labels[i])

#     ax.set_xticks(x + dimw / 2, dates)    
#     ax.set_ylabel('Euro')

#     plt.xticks(x,[d.replace(".20","/") for d in dates])
#     target.set_size_inches(width, height)
#     return target, ax

# def BarPlot(data, dates):
#     dim = len(data)
#     w = 2.
#     # dimw = w / dim
#     dimw = 2
#     target, ax = plt.subplots()
#     x = 3*np.arange(len(data))
#     b = ax.bar(x, data, dimw, color=['green' if i>0 else 'red' for i in data])

#     ax.set_xticks(x + dimw / 2, dates)    
#     ax.set_ylabel('Euro')

#     plt.xticks(x,[d.replace(".20","/") for d in dates])
#     target.set_size_inches(8,3.5)
#     return target, ax    


# def PieChart(in_data,keywords,start,end,w,h):
#     # data to plot
#     sum_all = analyse.summary_months(in_data,list(keywords.keys()))
#     dates = analyse.find_dates(sum_all)
#     dates = [d for d in dates if ( datetime.datetime.strptime(end, "%m/%Y").date() >=  datetime.datetime.strptime(d, "%m/%Y").date()>=  datetime.datetime.strptime(start, "%m/%Y").date())]

#     sizes = [abs(sum([x for x in s.values()])) for s in sum_all.values()]
#     sizes = [s/len(dates) for s in sizes]

#     target, ax = plt.subplots()
#     ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


#     def func(pct, allvals):
#         absolute = int(pct/100.*np.sum(allvals))
#         #print(pct,aboslute)
#         if pct > 2:
#             # return "{:.1f}%\n({:d} Eur)".format(pct, absolute)
#             return "{:.1f}%".format(pct)
#         else:
#             return ""

#     wedges, texts, autotexts = ax.pie(sizes, autopct=lambda pct: func(pct, sizes),
#                                   textprops=dict(color="w"), colors=use_colors)
#     target.set_size_inches(w,h)                                  

#     return target, ax  

# def BarAverage(data, dates, labels, w, h):

#     target, ax = plt.subplots()
#     target.set_size_inches(w,h)        

#     x = np.arange(len(data))
#     val = [abs(sum([x for x in y.values()]))/(1*len(dates)) for y in data]
#     for i in range(len(x)):
#         b = ax.barh(x[i], val[i], 0.75, color=use_colors[i])

#     ax.set_xscale('log')    
#     ax.tick_params(axis='y',  which='both', left=False, right=False, labelleft=False)

#     for i,k in enumerate(labels):
#         plt.text(3.5, x[i]-0.2, str(k)+" ("+str(int(val[i]))+" Eur)",size=10)
#     return target, ax 

# def BarAverage_InOut(in_data,keywords,start,end,w,h):
#     # data to plot
#     sum_all = analyse.summary_months(in_data,list(keywords.keys()))
#     dates = analyse.find_dates(sum_all)
#     dates = [d for d in dates if (
#          datetime.datetime.strptime(end, "%m/%Y").date() >=
#           datetime.datetime.strptime(d, "%m/%Y").date() >=
#             datetime.datetime.strptime(start, "%m/%Y").date()
#             )]

#     arranged = analyse.arrange_sum_by_data2(sum_all,dates)
#     labels = list(sum_all.keys())
#     return BarAverage(sum_all.values(), dates, labels, w, h) 

# def BarAverage_Accounts(in_data,start,end,w,h):
#     val = []
#     for x in in_data.keys():
#         val.append(sum(in_data[x].values()))

#     labels = list(in_data.keys())


#     target, ax = plt.subplots()
#     target.set_size_inches(w,h) 
    
#     x = np.arange(len(in_data))
#     print(x,val)
#     for i in range(len(x)):
#         b = ax.barh(x[i], val[i], 0.75, color=use_colors[i])

#     # ax.set_xscale('log')    
#     ax.tick_params(axis='y',  which='both', left=False, right=False, labelleft=False)

#     for i,k in enumerate(labels):
#         print(k)
#         plt.text(0, x[i], str(k)+" ("+str(int(val[i]))+" Eur)",size=10)
#     return target, ax

# def ScatterDatePlot(dates, values,width, height, bar):
#     # fig = plt.figure(figsize=(20,10))
#     target, ax = plt.subplots()
#     target.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
#     target.gca().xaxis.set_major_locator(mdates.MonthLocator()  )
#     if bar:
#         plt.bar(dates,values,color=['green' if i>0 else 'red' for i in values])
#     else:
#         plt.scatter(dates,values,s=10,c=['green' if i>0 else 'red' for i in values])
#     plt.grid(color='gray', linestyle='-', linewidth=0.2)
#     plt.gcf().autofmt_xdate()    

#     target.set_size_inches(width, height)
#     return target, ax


class NewPlotCanvas(QMainWindow):
    def __init__(self, style, in_arg=[], parent=None, width=5, height=4):
    #  def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        #self.x, self.y = self.get_data()
        self.create_main_frame(style)

        if (style == "StackedBar"):
            self.on_draw_StackedBar(in_arg[0],in_arg[1], width, height)
        if (style == "PieChart"):
            self.on_draw_PieChart(in_arg[0],in_arg[1], width, height)            
        if (style == "HorizontalBar"):
            self.on_draw_HorizontalBar(in_arg[0],in_arg[1], width, height)                       

    def create_main_frame(self, style):
        self.main_frame = QWidget()

        self.fig = Figure((5.0, 4.0), dpi=100)
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
            print("BOT", bot)  
            bot = [bot[j] + y[j] for j in range(len(y))]
            self.all_label.append(self.label_store)

        self.annot = self.axes.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                            bbox=dict(fc="w"),
                            arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)
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
        self.canvas.draw()  

    def on_draw_HorizontalBar(self, data, labels, width, height): 
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

        print("DATA", data)
        self.axes.set_xscale('log')    
        self.axes.tick_params(axis='y',  which='both', left=False, right=False, labelleft=False)

        for i,k in enumerate(labels):
            self.axes.text(3.5, x[i]-0.2, str(k)+" ("+str(int(data[i]))+" Eur)",size=10)
        self.annot = self.axes.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                            bbox=dict(fc="w"),
                            arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)            
        self.canvas.draw()                     

    def update_annot(self,bar,label):
        x = bar.get_x()+bar.get_width()/2.
        y = bar.get_y()+bar.get_height()
        self.annot.xy = (x,y)
        text = label+"\n (" + str(y) + " Eur)" #"#self.label_store[bar]
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

