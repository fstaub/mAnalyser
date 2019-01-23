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

        for a,n in zip(accounts,names):
            self.inout_account[n] = []
            for e in a.all_information:
                self.inout_account[n].append(e)                
                if e[2]>0:
                    self.incoming_raw.append(e)
                else:
                    self.outgoing_raw.append(e)

    def get_changes_accounts(self,accounts):
        self.changes= defaultdict(lambda: 0) #{}
        for x,y in zip(self.names, accounts):
            # self.changes[x] = self.account_evolution_month(y.internal_transfers[x]+self.inout_account[x])
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



        #for e in list(keywords.keys()):
        #         if d in sum_all[e]:
        #             table.setItem(count,0,QTableWidgetItem(e))
        #             table.setItem(count,1,QTableWidgetItem("{:10.2f} Eur".format(abs(sum_all[e][d]))))
        #             detail_button = QPushButton("Details")
        #             detail_button.clicked.connect(self.make_show_details(in_data[e],d,str(e)+" in "+str(d)))
        #             table.setCellWidget(count,2,detail_button)
        #             count += 1
        #             table.setRowCount(count+1)
        #             if e in entry_sum:
        #                 entry_sum[e] += abs(sum_all[e][d])
        #             else: 
        #                 entry_sum[e] = abs(sum_all[e][d])


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

def find_csv_filenames(path_to_dir, suffix=".csv" ):
            filenames = os.listdir(path_to_dir)
            return [ filename for filename in filenames if filename.endswith( suffix ) ]


class Depot():
    def __init__(self,directory):
        self.dates=[]
        self.values=[]
        filenames =  find_csv_filenames(directory)
        for cfile in filenames:
                start_writing=False
                with open(os.path.join(directory,cfile),encoding = "ISO-8859-1") as csvfile:
                    day = csv.reader(csvfile, delimiter=';')
                    for row in day:
                        if (start_writing):
                            print(row) 
                            print("m6",row[-6])
                            self.dates.append(datetime.datetime.strptime(cfile[6:16], '%d.%m.%Y'))
                            self.values.append(float(row[-6].replace('.','').replace(',','.')))
                        elif len(row) > 0:
                            if (row[0]=="WP-Art"):
                                start_writing=True
                            

        
