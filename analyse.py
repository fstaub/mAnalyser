import datetime
import os
import csv
from collections import defaultdict, OrderedDict
import calendar


class Balance():
    def __init__(self,accounts,names,keywords):
        self.collect(accounts,names)
        self.IN, self.missing_in = self.categorise_money_transfers(self.incoming_raw,keywords.IN)
        self.OUT, self.missing_out = self.categorise_money_transfers(self.outgoing_raw,keywords.OUT)        

        self.names = names
        self.get_changes_accounts(accounts)

    def collect(self,accounts,names):
        self.incoming_raw = []
        self.outgoing_raw = []   
        self.inout_account = defaultdict(lambda: 0)
        self.start = defaultdict(lambda: 0)

        for a,n in zip(accounts,names):
            self.inout_account[n] = []
            self.start[n] = a.start
            for e in a.all_information:
                self.inout_account[n].append(e)                
                if e[2]>0:
                    self.incoming_raw.append(e)
                else:
                    self.outgoing_raw.append(e)

    def get_changes_accounts(self,accounts):
        self.changes= defaultdict(lambda: 0) 
        # self.transfers= defaultdict(lambda: 0)
        self.transfers = {}
        for x,y in zip(self.names, accounts):
            # self.changes[x] = self.account_evolution_month(y.internal_transfers[x]+self.inout_account[x])
            self.transfers[x] = self.inout_account[x]+y.internal_transfers
            self.changes[x] = self.account_evolution_month(self.inout_account[x]+y.internal_transfers)

    def account_evolution_month(self,account):
        dates = find_dates_list(account)
        # out = defaultdict(lambda: 0) # {}
        out = []
        remaining = account
        todo = []
        summed = 0        
        for d in dates:
            for k in remaining:
                # if (datetime.datetime.strptime(k[0][3:], "%m.%Y").date() <= datetime.datetime.strptime(d, "%m.%Y").date()):
                if (k[0] <= d):
                    summed += k[-1]
                else:
                    todo.append(k)
            # out[d] = summed
            out.append([d, 'new sum', summed])
            remaining = todo
            todo = []
        return out

    def average(self, data, entries, dates):
        sum_all = summary_months(in_data,entries)
        entry_sum = {}
        for e in entries:
            entry_sum[e]=0
            for d in dates:
                entry_sum[e] += abs(sum_all[e][d])/len(dates)
        return entry_sum

    def categorise_money_transfers(self,data,keywords):
        category = {}
        for k in keywords.keys():
            category[k]=[]
        no_category=[]
        for d in data:
            found = False
            for k in keywords.keys():
                if  max([d[1].find(x) for x in keywords[k]])>-1:
                    found = True
                    category[k].append(d)
            if found is False:
                no_category.append(d)
        return category, no_category                     


# HELPER FUNCTIONS
def sum_up_month(data):
    out = {}
    for d in data:
        # month = d[0][3:]
        month = get_month(d[0])
        if month in out:
            out[month] = d[2]+out[month]
        else:
            out[month] = d[2]
    return out  

flatten = lambda l: [item for sublist in l for item in sublist]

def find_dates(data):
    out = list(set(flatten([list(x.keys()) for x in data.values()])))
#    return sorted(out,key=lambda x: datetime.datetime.strptime(x, "%m.%Y").date())
    return sorted(out)

def find_dates_list(data):
    #out = [y[0][3:] for y in data]
    #return sorted(list(set(out)),key=lambda x: datetime.datetime.strptime(x, "%m.%Y").date())
    out = [y[0] for y in data]
    return sorted(list(set(out)))    

def find_dates2(all_accounts):
    out = list(set(flatten(list([list(x.keys()) for x in list((all_accounts.values()))]))))
    # return  sorted(out,key=lambda x: datetime.datetime.strptime(x, "%m.%Y").date()) 
    return  sorted(out) 

# MAIN FUNCTIONS
def summary_months(data, keywords):
    out = OrderedDict()
    for k in keywords:
        # if k in data:
            out[k] = sum_up_month(data[k])
        # else:
            # out[k] = [{'1':0}]
    return out

def group_data_by_month(in_data, dates):
    out = OrderedDict()
    for d in dates:
        new_main = {}
        for k in in_data.keys():
            new_list = []
            sum_up = 0
            for e in in_data[k]:
                # if e[0][3:] == d:
                if get_month(e[0]) == get_month(d):                
                    new_list.append(e)
                    sum_up +=e[2]
            new_main[k] = {}
            new_main[k]['entries'] =  new_list
            new_main[k]['sum'] =  sum_up
        out[d] = new_main
    return out   

def average_months(in_data,first,last):
    dates = generate_dates(first,last)
    data = group_data_by_month(in_data,dates)
    flat=list(data.values())
    ld = len(dates)
    new_list = {}
    for i in flat:
        for  k in i.keys():
            if k in new_list:
                new_list[k]['sum'] += i[k]['sum']/ld
                new_list[k]['entries'].append(i[k]['entries'])
            else:
                new_list[k]={}
                new_list[k]['sum'] = i[k]['sum']/ld
                new_list[k]['entries']= i[k]['entries']
    return new_list    

def add_months(sourcedate,months):
     month = sourcedate.month - 1 + months
     year = sourcedate.year + month // 12
     month = month % 12 + 1
     day = min(sourcedate.day,calendar.monthrange(year,month)[1])
     return datetime.date(year,month,day)

def generate_dates(first,last):
    out = [first]
    # start = datetime.datetime.strptime(first, "%m.%Y").date()
    # end = datetime.datetime.strptime(last, "%m.%Y").date()
    next_month = add_months(first,1)
    while (next_month <= last):
        # out.append(next_month.strftime("%m.%Y"))
        out.append(next_month)        
        next_month = add_months(next_month,1)
    return out    


# FOR HISTOGRAM
def arrange_sum_by_data(data):
    dates = find_dates(data)
    entries = []
    for k in data.values():
        sub_list=[]
        for d in dates:
            if d in k:
                sub_list.append(k[d])
            else:
                sub_list.append(0.)
        entries.append(sub_list)
    return entries

def arrange_sum_by_data2(data,dates):
#    dates = find_dates(data)
    entries = []
    for d in dates:
        sub_list=[]
        for k in data.values():
            if d in k:
                sub_list.append(k[d])
            else:
                sub_list.append(0.)
        entries.append(sub_list)
    return entries  

def arrange_sum_by_data_datetime(data, dates):
#    dates = find_dates(data)
    entries = []
    for d in dates:
        sub_list=[]
        for k in data.values():
            if get_month(d) in k:
                sub_list.append(k[get_month(d)])
            else:
                sub_list.append(0.)
        entries.append(sub_list)
    return entries


class Depot():
    def __init__(self, stocks):
        self.changes_depot(stocks)
        self.stocks = stocks.stocks 
        self.fonds = stocks.fonds
        
#     def changes_depot(self, stocks):    
# #        dates = sorted(list(stocks.all_information.keys()), key=lambda x: datetime.datetime.strptime(x, "%d.%m.%Y").date())
#         dates = sorted(list(stocks.all_information.keys()))
#         last_win_stocks = 0
#         last_win_fonds = 0
#         self.all_information = []
#         for d in dates:
#             win_stocks = 0
#             win_fonds = 0
#             if len(stocks.all_information[d]) > 0:
#                 for x in stocks.all_information[d]:
#                     if x[0] in stocks.stocks:
#                         win_stocks  += x[1]*(x[3]-x[2])
#                     else:
#                         win_fonds += x[1]*(x[3]-x[2])
#                 self.all_information.append([d,'Fonds',win_fonds-last_win_fonds])
#                 self.all_information.append([d,'Aktien',win_stocks-last_win_stocks])
#                 last_win_fonds = win_fonds
#                 last_win_stocks = win_stocks 
    def changes_depot(self, stocks):    
#        dates = sorted(list(stocks.all_information.keys()), key=lambda x: datetime.datetime.strptime(x, "%d.%m.%Y").date())
        dates = sorted(list(stocks.all_information.keys()))
        # last_win_stocks = 0
        last_win = defaultdict(lambda: 0)
        self.all_information = []
        self.current_values = {}
        self.initial_values = {}
        for d in dates:
            if len(stocks.all_information[d]) > 0:
                for x in stocks.all_information[d]:
                    win  = x[1]*(x[3]-x[2])
                    self.all_information.append([d,x[0],win-last_win[x[0]]])
                    last_win[x[0]] = win
                    if x[0] not in  self.initial_values:
                        self.initial_values[x[0]] = x[1]*x[2]
                        self.current_values[x[0]] = []
                    self.current_values[x[0]].append([d, x[1], self.initial_values[x[0]] + last_win[x[0]]])
                     
    

def get_month(in_date):
    return  in_date.strftime("%m/%Y")
        
                            

# DARA FOR PLOTS

def prepare_stacked_bar(in_data, keywords, start, end):
        sum_all = summary_months(in_data, list(keywords.keys()))
        dates = generate_dates(start, end)
        arranged = arrange_sum_by_data_datetime(sum_all,dates)
        data = [[abs(x) for x in y] for y in arranged]

        return data, list(keywords.keys())

def prepare_stacked_bar_accounts(in_data, keywords, start, end):
        labels = list(in_data.keys())
        vals = list(in_data.values())
        dates = generate_dates(start, end)
        final_val =[]
        for d in dates:
            per_month=[]
            last=0
            for l in vals:
                for b in l:
                    if b[0] <= d:
                        last = b[2]
                per_month.append(last)
            final_val.append(per_month)
            
        return final_val, labels  

def prepare_pie_chart(in_data, keywords, start, end):
    sum_all = summary_months(in_data,list(keywords.keys()))
    dates = generate_dates(start, end)

    sizes = [abs(sum([x for x in s.values()])) for s in sum_all.values()]
    sizes = [s/len(dates) for s in sizes]
    return sizes, list(keywords.keys())

def prepare_horizontal_bar(in_data, keywords, start, end):
    sum_all = summary_months(in_data,list(keywords.keys()))
    dates = generate_dates(start, end)
    arranged = arrange_sum_by_data_datetime(sum_all,dates)
    labels = list(sum_all.keys())
    val = [abs(sum([x for x in y.values()]))/(1*len(dates)) for y in sum_all.values()]
    return val, labels    

def prepare_horizontal_bar_accounts(in_data, keywords, start, end):
    labels = list(in_data.keys())
    vals = list(in_data.values())
    final_val = [v[-1][-1] for v in vals]
    return final_val,labels

def prepare_plusminus_bar(in_data, keywords, start, end):
    dates = generate_dates(start, end)
    data = group_data_by_month(in_data, dates)
    out = []
    for x in data.keys():
        out += [sum(x['sum'] for x in list(data[x].values()))]
    return out, dates  

def prepare_scatter_total_change_stocks(in_data, keywords, start, end):
    x, values = generate_total_change(in_data, keywords)
    return values, x

def prepare_pie_total_stocks(in_data, keywords, start, end):
    x, values = prepare_stacked_bar_accounts(in_data, keywords, start, end)
    print(values)
    val = [v[-1] for v in x]
    return val, x    

def prepare_scatter_daily_changes_stocks(in_data, keywords, start, end):
    x, values = generate_daily_changes(in_data, keywords)
    return values, x    

def prepare_scatter_daily_stocks(in_data, keywords, start, end):
    x, values = generate_daily_changes(in_data, keywords)
    return values, x        

def generate_daily_changes(info, keywords):
        dates = []
        values = []
        for d in info:
            if (d[1] in keywords):
                if d[0] in dates:
                    values[-1] += d[2]
                else:
                    values += [d[2]]
                    dates += [d[0]]
        return dates, values

def generate_total_change(info, keywords):
        dates = []
        values = []
        for d in info:
            if (d[1] in keywords):
                if d[0] in dates:
                    values[-1] += d[2]
                else:
                    if values == []:
                        values += [d[2]]
                    else:
                        values += [values[-1] + d[2]]
                    dates += [d[0]]
        return dates, values           
