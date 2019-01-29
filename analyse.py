import datetime
import os
import csv
from collections import defaultdict, OrderedDict
import calendar
import pandas as pd

class Depot():
    def __init__(self, stocks):
        self.stocks = stocks.stocks 
        self.fonds = stocks.fonds
        self.is_included = self.fonds + self.stocks
        self.changes_depot(stocks)        

    def changes_depot(self, stocks):    
#        dates = sorted(list(stocks.all_information.keys()), key=lambda x: datetime.datetime.strptime(x, "%d.%m.%Y").date())
        dates = sorted(list(stocks.all_information.keys()))
        # last_win_stocks = 0
        last_win = defaultdict(lambda: 0)
        self.all_information = []
        self.current_values = {}
        self.initial_values = {}
        self.current_values_total = []
        self.current_changes_total = []
        
        for d in dates:
            sum_total = 0
            last_win_total = 0
            if len(stocks.all_information[d]) > 0:
                for x in stocks.all_information[d]:
                    win  = x[1]*(x[3]-x[2])
                    self.all_information.append([d,x[0],win-last_win[x[0]]])
                    last_win_total += win-last_win[x[0]]
                    last_win[x[0]] = win
                    if x[0] not in  self.initial_values:
                        self.initial_values[x[0]] = x[1]*x[2]
                        self.current_values[x[0]] = []
                    sum_total += x[1]*x[3]
                    self.current_values[x[0]].append([d, x[1], x[1]*x[3]])
            if sum_total > 0:
                self.current_values_total.append([d,'daily sum', sum_total])
                self.current_changes_total.append([d,'daily change', last_win_total])

        # generate pandas data frame
        all_columns = ['Date', 'Name', 'Amount', 'Start', 'Price', 'Total' , 'DailyWin', 'TotalWin', 'Category']
        self.df_depot = pd.DataFrame(columns=all_columns)
        win_last_day = defaultdict(lambda: 0)
        for d in dates:
            for x in stocks.all_information[d]:
                total_win  = x[1]*(x[3]-x[2])
                daily_win = total_win - win_last_day[x[0]]
                win_last_day[x[0]] = total_win

                new = [d, x[0], x[1], x[2], x[3], x[1]*x[3], daily_win, total_win, 'Aktie' if x[0] in self.stocks else 'Fond']
                self.df_depot = self.df_depot.append(pd.Series(new, index=all_columns), ignore_index=True)


class Balance():
    def __init__(self, accounts, names, keywords):
        self.collect(accounts, names, keywords)
        # self.IN, self.missing_in = self.categorise_money_transfers(self.incoming_raw,keywords.IN)
        # self.OUT, self.missing_out = self.categorise_money_transfers(self.outgoing_raw,keywords.OUT)        

        self.names = names
        self.is_included = names
        self.get_changes_accounts(accounts, names,  self.df_transactions)

    def include_depot(self, depot):
        self.changes = {**self.changes, **{"Depot": depot.current_values_total}}
        self.transfers = {**self.transfers, **{"Depot": depot.current_changes_total}}
        self.is_included.append("Depot")

    def collect(self, accounts, names, keywords):
        self.incoming_raw = []
        self.outgoing_raw = []   
        self.inout_account = defaultdict(lambda: 0)
        self.start = defaultdict(lambda: 0)
        self.internal = []
        self.internal_account = {}

        for a,n in zip(accounts, names):
            self.inout_account[n] = []
            self.start[n] = a.start
            self.internal += a.internal_transfers
            self.internal_account[n] = a.internal_transfers
            for e in a.all_information:
                self.inout_account[n].append(e)                
                if e[2]>0:
                    self.incoming_raw.append(e)
                else:
                    self.outgoing_raw.append(e)

        # for pandas data frame
        all_columns = ['Date','Description','Amount', 'InOut', 'Category','Account']
        self.df_transactions = pd.DataFrame(columns=all_columns)
        for ac, name  in zip (accounts, names):
            for entry in ac.all_information:
                new = [entry[0],entry[1],entry[2], 'IN' if entry[2] > 0  else 'OUT',
                    get_category(entry[1], keywords.IN if entry[2] > 0 else keywords.OUT), name] 
                self.df_transactions = self.df_transactions.append(pd.Series(new, index=all_columns), ignore_index=True)



    def get_changes_accounts(self, accounts, names, df):
        self.changes= defaultdict(lambda: 0) 
        # self.transfers= defaultdict(lambda: 0)
        self.transfers = {}
        for x,y in zip(self.names, accounts):
            # self.changes[x] = self.account_evolution_month(y.internal_transfers[x]+self.inout_account[x])
            self.transfers[x] = self.inout_account[x]+y.internal_transfers
            self.changes[x] = self.account_evolution_month(self.inout_account[x] + y.internal_transfers, x)

        all_columns_accounts = ['Date','Account','Transaction','Sum']
        self.df_acc = pd.DataFrame(columns=all_columns_accounts)
        for name in names:
            new_df=df[df['Account']==name].sort_values(by=['Date'])
            summe = 0
            for index, row in new_df.iterrows():
                summe += row['Amount']
                new = [row['Date'], name, row['Amount'],summe] 
                self.df_acc = self.df_acc.append(pd.Series(new, index=all_columns_accounts), ignore_index=True)            

    def account_evolution_month(self, account, name):
        dates = find_dates_list(account)
        # out = defaultdict(lambda: 0) # {}
        out = []
        remaining = account
        todo = []
        summed = self.start[name]       
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

    # def categorise_money_transfers(self,data,keywords):
    #     category = {}
    #     for k in keywords.keys():
    #         category[k]=[]
    #     no_category=[]
    #     for d in data:
    #         found = False
    #         for k in keywords.keys():
    #             if  max([d[1].find(x) for x in keywords[k]])>-1:
    #                 found = True
    #                 category[k].append(d)
    #         if found is False:
    #             no_category.append(d)
    #     return category, no_category                     


# HELPER FUNCTIONS
def get_category(text, keywords):
    for k in keywords.keys():
        if  max([text.find(x) for x in keywords[k]]) > -1:
           return k
    return 'not categorised'

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
    return sorted(out)

def find_dates_list(data):
    out = [y[0] for y in data]
    return sorted(list(set(out)))    

def find_dates2(all_accounts):
    out = list(set(flatten(list([list(x.keys()) for x in list((all_accounts.values()))]))))
    return  sorted(out) 

# MAIN FUNCTIONS
def summary_months(data, keywords):
    out = OrderedDict()
    for k in keywords:
            out[k] = sum_up_month(data[k])
    return out

def group_data_by_month(in_data, dates, keywords):
    out = OrderedDict()
    for d in dates:
        new_main = OrderedDict()
        for k in in_data.keys():
            if k in keywords:
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

def last_of_month(data, dates, keywords):
    out = OrderedDict()
    last_date_in = datetime.date(1999,1,1)
    for d in dates:
        new_main = OrderedDict()
        for key in data.keys():
            if key in keywords:
                new_list = []
                last_value = 0
                last_date = last_date_in
                for entry in data[key]:
                    if last_date <= entry[0] <= d:
                        last_value = entry[2]
                        last_date = entry[0]
                        new_list.append(entry)
                new_main[key] = {}
                new_main[key]['entries'] =  new_list
                new_main[key]['sum'] =  last_value 
        last_date_in = d
        out[d] = new_main
    return out  
    

def average_months(in_data, first, last, keywords):
    dates = generate_dates(first,last)
    data = group_data_by_month(in_data,dates, keywords)
    flat=list(data.values())
    ld = len(dates)
    new_list = {}
    for i in flat:
        for  k in i.keys():
            if k in new_list:
                new_list[k]['sum'] += i[k]['sum']/ld
                new_list[k]['entries'] += i[k]['entries']
            else:
                new_list[k]={}
                new_list[k]['sum'] = i[k]['sum']/ld
                new_list[k]['entries']= i[k]['entries']
    return new_list   

def depot_value(in_data):
    new_list = OrderedDict()
    for d in in_data.keys():
        sum = 0
        entries = []
        for k in in_data[d].keys():
            sum += in_data[d][k]['sum']
            entries.append([d, k, in_data[d][k]['sum']])
        new_list[get_month(d)] = {}
        new_list[get_month(d)]['sum'] = sum 
        new_list[get_month(d)]['entries'] = entries
    return new_list

def add_months(sourcedate,months):
     month = sourcedate.month - 1 + months
     year = sourcedate.year + month // 12
     month = month % 12 + 1
     day = min(sourcedate.day,calendar.monthrange(year,month)[1])
     return datetime.date(year,month,day)

def go_to_last_day(date):
    days = calendar.monthrange(date.year,date.month)[1]
    return datetime.date(date.year, date.month, days)     

def generate_dates(first,last):
    out = [go_to_last_day(first)]
    next_month = add_months(first,1)
    while (next_month <= last):
        out.append(go_to_last_day(next_month))     
        next_month = add_months(next_month,1)
    return out    


# # FOR HISTOGRAM
# def arrange_sum_by_data(data):
#     dates = find_dates(data)
#     entries = []
#     for k in data.values():
#         sub_list=[]
#         for d in dates:
#             if d in k:
#                 sub_list.append(k[d])
#             else:
#                 sub_list.append(0.)
#         entries.append(sub_list)
#     return entries

# def arrange_sum_by_data2(data,dates):
# #    dates = find_dates(data)
#     entries = []
#     for d in dates:
#         sub_list=[]
#         for k in data.values():
#             if d in k:
#                 sub_list.append(k[d])
#             else:
#                 sub_list.append(0.)
#         entries.append(sub_list)
#     return entries  

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



# Helper functions for dates     

def get_month(in_date):
    return  in_date.strftime("%m/%Y")

def skip_days(dates):
    new_dates = []
    for d in dates:
        new_dates.append(datetime.date(d.year,d.month,1))
    return new_dates

def skip_day(date):
    return  datetime.date(date.year,date.month,1)



#----------------------------------------------
# Functions to generate data for Plot      
#----------------------------------------------
 
# IN/OUT 
def prepare_stacked_bar(df, keywords, start, end):
        dates = generate_dates(start, end)
        data = []
        for d in dates:
            row = []
            for k in keywords:
                row.append(sum(df[(df['Category']==k)
                 & (df['Date'] >= skip_day(d))
                 & (df['Date'] < d)
                ]['Amount']))
            data.append(row)

        return data, keywords, skip_days(dates)

def prepare_pie_chart(df, keywords, start, end):
    nr_months = len(generate_dates(start, end))
    data = []
    for k in keywords:
            data.append(sum(df[(df['Category']==k)
                 & (df['Date'] >= skip_day(start))
                 & (df['Date'] < end)
            ]['Amount']/nr_months))
    return data, keywords

def prepare_horizontal_bar(df, keywords, start, end):
    data = []
    nr_months = len(generate_dates(start, end))    
    for k in keywords:
            data.append(sum(df[(df['Category']==k)
                 & (df['Date'] >= skip_day(start))
                 & (df['Date'] < end)
            ]['Amount']/nr_months))
    return data, keywords 



# ACCOUNTS

def prepare_stacked_bar_accounts(df, accounts, start, end):
        dates = generate_dates(start, end)
        final_val =[]
        for d in dates:
            per_month=[]
            for acc in accounts:
                val = df[(df['Account']==acc) 
                        & (df['Date'] >= skip_day(d))
                        & (df['Date'] < d) 
                        ]['Sum']
                if len(val.index) == 0:
                    per_month.append(0)
                else:
                    per_month.append(float(val.tail(1)))
            final_val.append(per_month)
        return final_val, accounts, skip_days(dates)

def prepare_horizontal_bar_accounts(df, accounts, start, end):
    final_val = []
    for acc in accounts:
        final_val.append(
            float(df[(df['Account']==acc)]['Sum'].tail(1))
        )
    return final_val, accounts

def prepare_plusminus_bar(df, accounts, start, end):
    dates = generate_dates(start, end)
    out = []
    for d in dates:
        out.append(
            sum(df[(df['Date'] >= skip_day(d))
                & (df['Date'] < d) 
                ]['Transaction'])
        )
    return out, skip_days(dates)        

# STOCKS

def prepare_stacked_bar_stocks(df, stocks, start, end):
        dates = generate_dates(start, end)
        final_val =[]
        for d in dates:
            per_month=[]
            for name in stocks:
                val = df[(df['Name']==name) 
                        & (df['Date'] >= skip_day(d))
                        & (df['Date'] < d) 
                        ]['Total']
                if len(val.index) == 0:
                    per_month.append(0)
                else:
                    per_month.append(float(val.tail(1)))
            final_val.append(per_month)
        return final_val, stocks, skip_days(dates)

def prepare_scatter_total_change_stocks(df, keywords, start, end, relative):
    return prepare_scatter_change_stocks(df, keywords, start, end, 'TotalWin', relative)

def prepare_scatter_daily_changes_stocks(df, keywords, start, end, relative):
    return prepare_scatter_change_stocks(df, keywords, start, end, 'DailyWin', relative)

def prepare_scatter_change_stocks(df, keywords, start, end, kind_of_win, relative):
    dates = list(df['Date'].unique())
    dates = [d for d in dates if (start <= d < end)]
    values = []
    for d in dates:
        win = sum(df[(df['Date']==d)
                & (df['Name'].isin(keywords))][kind_of_win])
        if relative == True:
            total = sum(df[(df['Date']==d)
                & (df['Name'].isin(keywords))]['Total'])
            values.append( win/total) 
        else:
            values.append( win )
    return values, dates


def prepare_pie_total_stocks(df, keywords, start, end):
    last_day = df['Date'].iloc[-1]
    out = []
    labels = []
    for k in keywords:
        print(k)
        entry = df[(df['Date']==last_day) & (df['Name'] == k)]['Total']
        if (len(entry)>0):
            out.append(entry.iloc[-1])
            labels.append(k)
    return out, labels

       

# DARA FOR PLOTS

# def prepare_stacked_bar(in_data, keywords, start, end):
#         sum_all = summary_months(in_data, list(keywords.keys()))
#         dates = generate_dates(start, end)
#         arranged = arrange_sum_by_data_datetime(sum_all,dates)
#         data = [[abs(x) for x in y] for y in arranged]

#         return data, list(keywords.keys()), skip_days(dates)

# def prepare_stacked_bar(in_data, keywords, start, end):
#         sum_all = summary_months(in_data, keywords)
#         dates = generate_dates(start, end)
#         arranged = arrange_sum_by_data_datetime(sum_all, dates)
#         data = [[abs(x) for x in y] for y in arranged]

#         return data, keywords, skip_days(dates)


# def prepare_stacked_bar_accounts(in_data, keywords, start, end):
#         labels = keywords
#         vals = list(in_data.values())
#         dates = generate_dates(start, end)
#         final_val =[]
#         for d in dates:
#             per_month=[]
#             for l in labels:
#                 last=0                
#                 for b in in_data[l]:
#                     if b[0] <= d:
#                         last = b[2]
#                 per_month.append(last)
#             final_val.append(per_month)
#         return final_val, labels, skip_days(dates)  

# def prepare_pie_chart(in_data, keywords, start, end):
#     sum_all = summary_months(in_data, keywords)
#     dates = generate_dates(start, end)

#     sizes = [abs(sum([x for x in s.values()])) for s in sum_all.values()]
#     sizes = [s/len(dates) for s in sizes]
#     return sizes, keywords



# def prepare_horizontal_bar(in_data, keywords, start, end):
#     # sum_all = summary_months(in_data,list(keywords.keys()))
#     sum_all = summary_months(in_data, keywords)
#     dates = generate_dates(start, end)
#     arranged = arrange_sum_by_data_datetime(sum_all,dates)
#     labels = list(sum_all.keys())
#     val = [abs(sum([x for x in y.values()]))/(1*len(dates)) for y in sum_all.values()]
#     return val, labels  
# 
#   

# def prepare_horizontal_bar_accounts(in_data, keywords, start, end):
#     vals = [in_data[k] for k in keywords] #list(in_data.values())
#     final_val = [v[-1][-1] for v in vals]
#     return final_val,keywords

# def prepare_plusminus_bar(in_data, keywords, start, end):
#     dates = generate_dates(start, end)
#     data = group_data_by_month(in_data, dates, keywords)
#     out = []
#     for x in data.keys():
#         out += [sum(x['sum'] for x in list(data[x].values()))]
#     return out, skip_days(dates)

# def prepare_scatter_total_change_stocks(in_data, in_data_total, keywords, start, end, relative):
#     dates, values = generate_total_change(in_data, keywords)
#     if (relative):
#         values = [v/vt[2] for v,vt, d in zip(values,in_data_total,dates)
#             if start <= d <= end]
#     else: 
#         values = [v for v, d in zip(values,dates) if start <= d <= end]
#     dates = [d for d in dates if  start <= d <= end]
#     return values, skip_days(dates)

# def prepare_pie_total_stocks(in_data, keywords, start, end):
#     x, labels, dates = prepare_stacked_bar_accounts(in_data, keywords, start, end)
#     return x[-1], labels    

# def prepare_scatter_daily_changes_stocks(in_data, in_data_total, keywords, start, end, relative ):
#     dates, values = generate_daily_changes(in_data, keywords)
#     if (relative):
#         values = [v/vt[2] for v,vt, d in zip(values,in_data_total,dates)
#             if start <= d <= end]
#     else: 
#         values = [v for v, d in zip(values,dates) if start <= d <= end]
#     dates = [d for d in dates if  start <= d <= end]
#     return values, skip_days(dates)    

# def prepare_scatter_daily_stocks(in_data, keywords, start, end):
#     dates, values = generate_daily_changes(in_data, keywords)
#     values = [v for v, d in zip(values,dates) if start <= d <= end]
#     dates = [d for d in dates if  start <= d <= end]
#     return values, skip_days(dates)      


# def generate_daily_changes(info, keywords):
#         dates = []
#         values = []
#         for d in info:
#             if (d[1] in keywords):
#                 if d[0] in dates:
#                     values[-1] += d[2]
#                 else:
#                     values += [d[2]]
#                     dates += [d[0]]
#         return dates, values

# def generate_total_change(info, keywords):
#         dates = []
#         values = []
#         for d in info:
#             if (d[1] in keywords):
#                 if d[0] in dates:
#                     values[-1] += d[2]
#                 else:
#                     if values == []:
#                         values += [d[2]]
#                     else:
#                         values += [values[-1] + d[2]]
#                     dates += [d[0]]
#         return dates, values           
