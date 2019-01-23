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
        # print(accounts[1].all_information)
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
        self.transfers= defaultdict(lambda: 0) 
        for x,y in zip(self.names, accounts):
            # self.changes[x] = self.account_evolution_month(y.internal_transfers[x]+self.inout_account[x])
            self.transfers[x] = self.inout_account[x]+y.internal_transfers
            self.changes[x] = self.account_evolution_month(self.inout_account[x]+y.internal_transfers)

    def account_evolution_month(self,account):
        dates = find_dates_list(account)
        out = defaultdict(lambda: 0) # {}
        remaining = account
        todo = []
        for d in dates:
            summed = 0
            for k in remaining:
                if (datetime.datetime.strptime(k[0][3:], "%m.%Y").date() <= datetime.datetime.strptime(d, "%m.%Y").date()):
                    summed += k[-1]
                else:
                    todo.append(k)
            out[d] = summed
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
        month = d[0][3:]
        if month in out:
            out[month] = d[2]+out[month]
        else:
            out[month] = d[2]
    return out  

flatten = lambda l: [item for sublist in l for item in sublist]

def find_dates(data):
    out = list(set(flatten([list(x.keys()) for x in data.values()])))
    return sorted(out,key=lambda x: datetime.datetime.strptime(x, "%m.%Y").date())

def find_dates_list(data):
    out = [y[0][3:] for y in data]
    return sorted(list(set(out)),key=lambda x: datetime.datetime.strptime(x, "%m.%Y").date())

def find_dates2(all_accounts):
    out = list(set(flatten(list([list(x.keys()) for x in list((all_accounts.values()))]))))
    return  sorted(out,key=lambda x: datetime.datetime.strptime(x, "%m.%Y").date()) 

# MAIN FUNCTIONS
def summary_months(data,keywords):
    out = {}
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
                if e[0][3:] == d:
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
    start = datetime.datetime.strptime(first, "%m.%Y").date()
    end = datetime.datetime.strptime(last, "%m.%Y").date()
    next_month =  add_months(start,1)
    print(next_month,end)
    while (next_month <= end):
        out.append(next_month.strftime("%m.%Y"))
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


class Depot():
    def __init__(self, stocks):
        self.changes_depot(stocks)
        
    def changes_depot(self, stocks):    
        dates = sorted(list(stocks.all_information.keys()), key=lambda x: datetime.datetime.strptime(x, "%d.%m.%Y").date())
        last_win_stocks = 0
        last_win_fonds = 0
        self.all_information = []
        for d in dates:
            win_stocks = 0
            win_fonds = 0
            if len(stocks.all_information[d]) > 0:
                for x in stocks.all_information[d]:
                    if x[0] in stocks.stocks:
                        win_stocks  += x[1]*(x[3]-x[2])
                    else:
                        win_fonds += x[1]*(x[3]-x[2])
                self.all_information.append([d,'Fonds',win_fonds-last_win_fonds])
                self.all_information.append([d,'Aktien',win_stocks-last_win_stocks])
                last_win_fonds = win_fonds
                last_win_stocks = win_stocks 

def generate_daily_changes(info, fonds=True, stocks=True ):
        dates = []
        values = []
        for d in info:
            if (d[1]=='Aktien' and stocks==True) or (d[1] == 'Fonds' and fonds==True):
                if d[0] in dates:
                    values[-1] += d[2]
                else:
                    values += [d[2]]
                    dates += [d[0]]
        return dates, values

def generate_total_changes(info, fonds=True, stocks=True):
        dates = []
        values = []
        for d in info:
            if (d[1]=='Aktien' and stocks==True) or (d[1] == 'Fonds' and fonds==True):
                if d[0] in dates:
                    values[-1] += d[2]
                else:
                    if values == []:
                        values += [d[2]]
                    else:
                        values += [values[-1] + d[2]]
                    dates += [d[0]]
        return dates, values                
        
                            

        
