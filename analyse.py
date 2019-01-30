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
        dates = sorted(list(stocks.all_information.keys()))
        win_last_day = defaultdict(lambda: 0)
        info = {}
        info['Date'] = []
        info['Name'] = []
        info['Amount'] = []
        info['Start'] = []
        info['Price'] = []
        info['Total'] = []
        info['DailyWin'] = []
        info['TotalWin'] = []
        info['Category'] = []

        for d in dates:
            for x in stocks.all_information[d]:
                total_win  = x[1]*(x[3]-x[2])
                daily_win = total_win - win_last_day[x[0]]
                win_last_day[x[0]] = total_win
                info['Date'].append(d)
                info['Name'].append(x[0])
                info['Amount'].append(x[1])
                info['Start'].append(x[2])
                info['Price'].append(x[3])
                info['Total'].append(x[1]*x[3])
                info['DailyWin'].append(daily_win)
                info['TotalWin'].append(total_win)
                info['Category'].append('Aktie' if x[0] in self.stocks else 'Fond')

        self.df_depot = pd.DataFrame(data = info)                


class Balance():
    def __init__(self, accounts, names, keywords):
        self.names = names
        self.is_included = names
        self.collect(accounts, names, keywords)        
        self.get_changes_accounts(accounts, names, self.df_transactions)

    def get_category(self, entry, keywords):
        for k in keywords.keys():
            if  max([entry.find(x) for x in keywords[k]]) > -1:
               return k
        return 'not categorised'

    def include_depot(self, depot):
        df = depot.df_depot
        dates = list(df['Date'].unique())

        info = {}
        info['Date'] = []
        info['Account'] = []
        info['Transaction'] = []
        info['Description'] = []
        info['Sum'] = []

        for d in dates:
            new_df=df[df['Date'] == d]
            summe = 0
            for index, row in new_df.iterrows():
                info['Date'].append(d)
                info['Account'].append('Depot')
                info['Description'].append(row['Name'])
                info['Transaction'].append(row['DailyWin'])
                summe += row['Total']
                info['Sum'].append(summe)
        
        frames = [self.df_acc, pd.DataFrame(data = info)]
        self.df_acc = pd.concat(frames)                
        self.is_included.append("Depot")        

    def collect(self, accounts, names, keywords):
        # for pandas data frame
        info = {}
        info['Date'] = []
        info['Description'] = []
        info['Amount'] = []
        info['InOut'] = []
        info['Category'] = []
        info['Account'] = []
        for ac, name  in zip (accounts, names):
            for entry in ac.all_information:
                info['Date'].append(entry[0])
                info['Description'].append(entry[1])
                info['Amount'].append(entry[2])
                info['InOut'].append('IN' if entry[2] > 0  else 'OUT')
                info['Category'].append( self.get_category(entry[1], keywords.IN if entry[2] > 0 else keywords.OUT))
                info['Account'].append(name)

        self.df_transactions = pd.DataFrame(data = info)         

    def get_changes_accounts(self, accounts, names, df):
        info = {}
        info['Date'] = []
        info['Account'] = []
        info['Description'] = []
        info['Transaction'] = []
        info['Sum'] = []
        for name in names:
            new_df=df[df['Account'] == name].sort_values(by=['Date'])
            summe = 0
            for index, row in new_df.iterrows():
                summe += row['Amount']
                info['Date'].append(row['Date'])
                info['Account'].append(name)
                info['Description'].append(row['Description'])
                info['Transaction'].append(row['Amount'])
                info['Sum'].append(summe)
        self.df_acc = pd.DataFrame(data = info)

 

# HELPER FUNCTIONS
def get_category(text, keywords):
    for k in keywords.keys():
        if  max([text.find(x) for x in keywords[k]]) > -1:
           return k
    return 'not categorised'

# Helper functions for dates     

def generate_dates(first,last):
    out = [go_to_last_day(first)]
    next_month = add_months(first,1)
    while (next_month <= last):
        out.append(go_to_last_day(next_month))     
        next_month = add_months(next_month,1)
    return out  

def add_months(sourcedate,months):
     month = sourcedate.month - 1 + months
     year = sourcedate.year + month // 12
     month = month % 12 + 1
     day = min(sourcedate.day,calendar.monthrange(year,month)[1])
     return datetime.date(year,month,day)

def go_to_last_day(date):
    days = calendar.monthrange(date.year,date.month)[1]
    return datetime.date(date.year, date.month, days)     


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
# Functions to generate data for DataTabs      
#----------------------------------------------

def last_entry_of_month_inout(df, keywords, start, end):
    dates = generate_dates(start, end)
    out = OrderedDict()
    for d in dates:
        new_main = OrderedDict()
        for k in keywords:
            entries = df[(df['Category'] == k)
                & (df['Date'] >= skip_day(d))
                & (df['Date'] < d)]
            if (len(entries) > 0):
                new_main[k] = OrderedDict()                
                new_main[k]['entries'] = [[e['Date'], e['Description'], e['Amount']] for i, e in entries.iterrows()]
                new_main[k]['sum'] =  sum(entries['Amount'])
        if len(new_main.keys())>0:                
            out[d] = new_main
    return out

def last_entry_of_month_accounts(df, keywords, start, end):
    dates = generate_dates(start, end)
    out = OrderedDict()
    for d in dates:
        new_main = OrderedDict()
        for k in keywords:
            entries = df[(df['Account'] == k)
                & (df['Date'] >= skip_day(d))
                & (df['Date'] < d)]
            if (len(entries) > 0):
                new_main[k] = OrderedDict()                
                new_main[k]['entries'] = [[e['Date'], e['Description'], e['Transaction']] for i, e in entries.iterrows()]
                new_main[k]['sum'] = [entries['Sum'].iloc[-1], sum(entries['Transaction'])]
        if len(new_main.keys())>0:                
            out[d] = new_main
    return out

def last_entry_of_month_stocks(df, keywords, start, end):
    dates = generate_dates(start, end)
    out = OrderedDict()
    for d in dates:
        new_main = OrderedDict()
        for k in keywords:
            entries = df[(df['Name'] == k)
                & (df['Date'] >= skip_day(d))
                & (df['Date'] < d)]
            if (len(entries) > 0):
                new_main[k] = OrderedDict()                
                new_main[k]['entries'] = [[e['Date'], e['Name'], e['DailyWin']] for i, e in entries.iterrows()]
                new_main[k]['sum'] = [entries['Total'].iloc[-1], sum(entries['DailyWin'])]
        if len(new_main.keys())>0:
            out[d] = new_main
    return out    



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
            data.append(abs(sum(df[(df['Category']==k)
                 & (df['Date'] >= skip_day(start))
                 & (df['Date'] < end)
            ]['Amount']/nr_months)))
    return data, keywords

def prepare_horizontal_bar(df, keywords, start, end):
    data = []
    nr_months = len(generate_dates(start, end))    
    for k in keywords:
            data.append(abs(sum(df[(df['Category']==k)
                 & (df['Date'] >= skip_day(start))
                 & (df['Date'] < end)
            ]['Amount']/nr_months)))
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
            abs(float(df[(df['Account']==acc)]['Sum'].tail(1)))
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
            out.append(abs(entry.iloc[-1]))
            labels.append(k)
    return out, labels

       
