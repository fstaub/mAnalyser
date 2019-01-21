import datetime


class Balance():
    def __init__(self,accounts,keywords):
        self.collect(accounts)
        self.IN, self.missing_in = self.categorise_money_transfers(self.incoming_raw,keywords.IN)
        self.OUT, self.missing_out = self.categorise_money_transfers(self.outgoing_raw,keywords.OUT)        

    def collect(self,accounts):
        self.incoming_raw = []
        self.outgoing_raw = []        
        for a in accounts:
            for e in a.all_information:
                if e[2]>0:
                    self.incoming_raw.append(e)
                else:
                    self.outgoing_raw.append(e)

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

def find_dates(data):
    flatten = lambda l: [item for sublist in l for item in sublist]
    out = list(set(flatten([list(x.keys()) for x in data.values()])))
    return sorted(out,key=lambda x: datetime.datetime.strptime(x, "%m.%Y").date())


# MAIN FUNCTIONS
def summary_months(data,keywords):
    out = {}
    for k in keywords:
        # if k in data:
            out[k] = sum_up_month(data[k])
        # else:
            # out[k] = [{'1':0}]
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