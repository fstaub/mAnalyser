import numpy as np
import math
import analyse
import datetime
import matplotlib.pyplot as plt
import mpld3


def formatter(**kwargs):
        dist = abs(np.array(x) - kwargs['x'])
        i = dist.argmin()
        labels = attendance if kwargs['bottom'] == 0 else attendance2
        return '\n'.join(labels[i])


def HistPlot(in_data,keywords,start,end,bar):
    # data to plot
    sum_all = analyse.summary_months(in_data,list(keywords.keys()))
    dates = analyse.find_dates(sum_all)
    dates = [d for d in dates if ( datetime.datetime.strptime(end, "%m.%Y").date() >=  datetime.datetime.strptime(d, "%m.%Y").date()>=  datetime.datetime.strptime(start, "%m.%Y").date())]

    arranged = analyse.arrange_sum_by_data2(sum_all,dates)
    data = [[abs(x) for x in y] for y in arranged]

    dim = len(data[0])
    w = 2.
    # dimw = w / dim
    dimw = 2
    target, ax = plt.subplots()
    x = 3*np.arange(len(data))
    bot = [0 for x in data]

    for i in range(len(data[0])):
        y = [d[i] for d in data]
#        b = ax.bar(x + i * dimw, y, dimw, bottom=1.,label=list(keywords.keys())[i])
        if (bar):
            b = ax.bar(x, y, dimw, bottom=0,label=list(keywords.keys())[i])
            bot += y
        else:    
            b = ax.plot(x, y, label=list(keywords.keys())[i])

        #ax.set_xticks(x + dimw / 2, map(str, x))
    ax.set_xticks(x + dimw / 2, dates)    
    #ax.set_yscale('log')

    ax.set_xlabel('Month')
    ax.set_ylabel('Euro')

    plt.xticks(x,dates)
    #plt.legend(loc='upper center', bbox_to_anchor=(1.25, 1), shadow=True, ncol=1)
    target.set_size_inches(8,3.5)
    #plt.figure(num=target,figsize=(1,1))        
    # plt.draw()
    # datacursor(hover=True, formatter=formatter)
    # tooltip = mpld3.plugins.PointLabelTooltip(ax, labels=list(keywords.keys()))
    # mpld3.plugins.connect(target, tooltip)
    # mpld3.show()
    return target, ax

    