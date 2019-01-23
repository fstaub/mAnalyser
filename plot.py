import numpy as np
import math
import analyse
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplcursors


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

def formatter(**kwargs):
        dist = abs(np.array(x) - kwargs['x'])
        i = dist.argmin()
        labels = attendance if kwargs['bottom'] == 0 else attendance2
        return '\n'.join(labels[i])

def HistPlot_Account(in_data, start, end, bar, w, h):
    dates = analyse.find_dates2(in_data)
    dates = [d for d in dates if ( datetime.datetime.strptime(end, "%m.%Y").date() >=  datetime.datetime.strptime(d, "%m.%Y").date()>=  datetime.datetime.strptime(start, "%m.%Y").date())]

    data = []
    for x in list(in_data.values()):
        data.append([abs(sum(x[d] for d in dates[:i])) for i in range(1,len(dates)+1)])
    
    data = list(np.array(data).T)
    labels = list(in_data.keys())

    return HistPlot(data, dates, labels, bar, w, h)

def HistPlot_Changes(in_data, start, end, w, h):
    dates = analyse.generate_dates(start, end)
    data = analyse.group_data_by_month(in_data, dates)
    out = []
    for x in data.keys():
        out += [sum(x['sum'] for x in list(data[x].values()))]


    # dates = [d for d in dates if ( datetime.datetime.strptime(end, "%m.%Y").date() >=  datetime.datetime.strptime(d, "%m.%Y").date()>=  datetime.datetime.strptime(start, "%m.%Y").date())]

    # data = []
    # for x in list(in_data.values()):
    #     data.append([abs(sum(x[d] for d in dates[:i])) for i in range(1,len(dates)+1)])
    
    # data = [sum(d) for d in data]
    print(out, dates)
    return BarPlot(out, dates)    

def HistPlot_InOut(in_data, keywords, start, end, bar, w, h):
    sum_all = analyse.summary_months(in_data, list(keywords.keys()))
    dates = analyse.find_dates(sum_all)
    dates = [d for d in dates if ( datetime.datetime.strptime(end, "%m.%Y").date() >=  datetime.datetime.strptime(d, "%m.%Y").date()>=  datetime.datetime.strptime(start, "%m.%Y").date())]

    arranged = analyse.arrange_sum_by_data2(sum_all,dates)
    data = [[abs(x) for x in y] for y in arranged]
    labels = list(in_data.keys())

    return HistPlot(data, dates, labels, bar, w, h)    

def HistPlot(data, dates, labels, bar, width, height):
    dim = len(data[0])
    w = 2.
    # dimw = w / dim
    dimw = 2
    target, ax = plt.subplots()
    x = 3*np.arange(len(data))
    bot = [0 for x in data]
    for i in range(len(labels)):
        y = [d[i] for d in data]
        print(i, x, y, labels[i])
        if (bar):
            b = ax.bar(x, y, dimw, color=use_colors[i], bottom=0,label=labels[i])
            bot += y
        else:    
            b = ax.plot(x, y, color=use_colors[i], label=labels[i])

    ax.set_xticks(x + dimw / 2, dates)    
    ax.set_ylabel('Euro')

    plt.xticks(x,[d.replace(".20","/") for d in dates])
    target.set_size_inches(width, height)
    return target, ax

def BarPlot(data, dates):
    dim = len(data)
    w = 2.
    # dimw = w / dim
    dimw = 2
    target, ax = plt.subplots()
    x = 3*np.arange(len(data))
    b = ax.bar(x, data, dimw, color=['green' if i>0 else 'red' for i in data])

    ax.set_xticks(x + dimw / 2, dates)    
    ax.set_ylabel('Euro')

    plt.xticks(x,[d.replace(".20","/") for d in dates])
    target.set_size_inches(8,3.5)
    return target, ax    


def PieChart(in_data,keywords,start,end,w,h):
    # data to plot
    sum_all = analyse.summary_months(in_data,list(keywords.keys()))
    dates = analyse.find_dates(sum_all)
    dates = [d for d in dates if ( datetime.datetime.strptime(end, "%m.%Y").date() >=  datetime.datetime.strptime(d, "%m.%Y").date()>=  datetime.datetime.strptime(start, "%m.%Y").date())]

    sizes = [abs(sum([x for x in s.values()])) for s in sum_all.values()]
    sizes = [s/len(dates) for s in sizes]

    target, ax = plt.subplots()
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


    def func(pct, allvals):
        absolute = int(pct/100.*np.sum(allvals))
        #print(pct,aboslute)
        if pct > 2:
            # return "{:.1f}%\n({:d} Eur)".format(pct, absolute)
            return "{:.1f}%".format(pct)
        else:
            return ""

    wedges, texts, autotexts = ax.pie(sizes, autopct=lambda pct: func(pct, sizes),
                                  textprops=dict(color="w"), colors=use_colors)
    target.set_size_inches(w,h)                                  

    return target, ax  

def BarAverage(data, dates, labels, w, h):

    target, ax = plt.subplots()
    target.set_size_inches(w,h)        

    x = np.arange(len(data))
    val = [abs(sum([x for x in y.values()]))/(1*len(dates)) for y in data]
    for i in range(len(x)):
        b = ax.barh(x[i], val[i], 0.75, color=use_colors[i])

    ax.set_xscale('log')    
    ax.tick_params(axis='y',  which='both', left=False, right=False, labelleft=False)

    for i,k in enumerate(labels):
        plt.text(3.5, x[i]-0.2, str(k)+" ("+str(int(val[i]))+" Eur)",size=10)
    return target, ax 

def BarAverage_InOut(in_data,keywords,start,end,w,h):
    # data to plot
    sum_all = analyse.summary_months(in_data,list(keywords.keys()))
    dates = analyse.find_dates(sum_all)
    dates = [d for d in dates if (
         datetime.datetime.strptime(end, "%m.%Y").date() >=
          datetime.datetime.strptime(d, "%m.%Y").date() >=
            datetime.datetime.strptime(start, "%m.%Y").date()
            )]

    arranged = analyse.arrange_sum_by_data2(sum_all,dates)
    labels = list(sum_all.keys())
    return BarAverage(sum_all.values(), dates, labels, w, h) 

def BarAverage_Accounts(in_data,start,end,w,h):
    val = []
    for x in in_data.keys():
        val.append(sum(in_data[x].values()))

    labels = list(in_data.keys())


    target, ax = plt.subplots()
    target.set_size_inches(w,h) 
    
    x = np.arange(len(in_data))
    print(x,val)
    for i in range(len(x)):
        b = ax.barh(x[i], val[i], 0.75, color=use_colors[i])

    # ax.set_xscale('log')    
    ax.tick_params(axis='y',  which='both', left=False, right=False, labelleft=False)

    for i,k in enumerate(labels):
        print(k)
        plt.text(0, x[i], str(k)+" ("+str(int(val[i]))+" Eur)",size=10)
    return target, ax

def ScatterDatePlot(dates, values,width, height, bar):
    # fig = plt.figure(figsize=(20,10))
    target, ax = plt.subplots()
    target.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
    target.gca().xaxis.set_major_locator(mdates.MonthLocator()  )
    if bar:
        plt.bar(dates,values,color=['green' if i>0 else 'red' for i in values])
    else:
        plt.scatter(dates,values,s=10,c=['green' if i>0 else 'red' for i in values])
    plt.grid(color='gray', linestyle='-', linewidth=0.2)
    plt.gcf().autofmt_xdate()    

    target.set_size_inches(width, height)
    return target, ax
