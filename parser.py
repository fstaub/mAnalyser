import os 
import json 
import csv
import datetime
import collections

class Parser():
    def filter_redundant(self,data):
        out = []
        internal = []
        start = 0
        for entry in data:
            if entry[1].find("STARTGUTHABEN") >= 0:
                start = entry[-1]
            elif  max([entry[1].find(x) for x in self.keywords.INTERNAL])<0:
                out.append(entry)
            else:
                internal.append(entry)
        return out, internal, start

    def format_number(self,in_string):
        return float(in_string.replace(".","").replace(",","."))

    def format_date(self, in_string):
        return  datetime.datetime.strptime(in_string, "%d.%m.%Y").date()        

    def __init__(self,dirName,keywords):
        self.keywords=keywords
        out = []
        listOfFile = os.listdir(dirName)
        for file in listOfFile:
            # try:
            #     out = out + (self.parse(dirName+file))
            # except:
            #     print("broken file: ", file)
            out = out + (self.parse(dirName+file))
        # self.all_information, self.internal_transfers, self.start = self.filter_redundant(out)
        self.all_information = out


class DiBa_Parser(Parser):
    def parse(self,file):
        data=[]
        with open(file, newline='', encoding = "ISO-8859-1") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
            start_writing=False
            for row in spamreader:
                if (start_writing):
                    data.append(self.format_entry(row))
                elif len(row)>0:
                    if (row[0]=='Buchung'):
                            start_writing=True
        return data

    def format_entry(self,text):
        try:
            out=[self.format_date(text[0]),self.purpose(text[2],text[3],text[4]),self.format_number(text[-2])]
        except:
            print("problematic line:", text)
        return out

    def purpose(self,in1,in2,in3):
        return in1 + " " + in2 


class LBB_Parser(Parser):
    def parse(self,file):
        data=[]
        with open(file, newline='', encoding = "ISO-8859-1") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
            start_writing=False
            for row in spamreader:
                if (start_writing) and ('PUNKTE' not in row[3]):
                    data.append(self.format_entry(row))
                elif len(row)>0:
                    if (row[0]=='Konto-/Kartennummer'):
                            start_writing=True
        return data

    def format_entry(self,text):
        out=[self.format_date(text[1]),text[3],self.format_number(text[-1])]
        return out

class Amazon_Parser(Parser):
    def parse(self,file):
        data=[]
        with open(file, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:
                data.append(self.format_entry(row))
                data.append(self.format_entry_payment(row))
        return data

    def format_entry(self,text):
        out=[self.format_date(text[3]), text[1] + " for " + text[2] ,self.format_number(text[4])]
        return out

    def format_entry_payment(self,text):
        out=[self.format_date(text[3]), "Amazon Payment", -self.format_number(text[4])]
        return out

    def format_number(self,in_string):
        return -float(in_string.replace("EUR","").replace(".","").replace(",","."))

    def format_date(self, in_string):
        return  datetime.datetime.strptime(in_string, "%Y-%m-%d").date()





class CA_Parser(Parser):
    def parse(self,file):
        data=[]
        start_writing = False
        with open(file, newline='', encoding = "ISO-8859-1") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for row in spamreader:
                    if (start_writing):
                        if len(row)>1:
                            data.append(self.format_entry(row))
                    elif len(row)>0:
                        if (row[0]=='Date'):
                            start_writing=True  
        return data

    def format_date(self, in_string):
        return  datetime.datetime.strptime(in_string, "%d/%m/%Y").date()

    def format_entry(self,text):
        try:
            out=[self.format_date(text[0]),text[1],self.format_number(text[3])]
        except:
            out=[self.format_date(text[0]),text[1],-self.format_number(text[2])]            
        return out

class PayPal_Parser(Parser):     
    def parse(self,file):
        data=[]
        with open(file, newline='',encoding = "utf-8") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            start_writing=False
            for row in spamreader:
                if (start_writing):
                    line = self.format_entry(row)
#                    if line[-1]<0: 
                    data.append(line)
                elif len(row)>0:
                    start_writing=True
        return data

    def format_entry(self,text):
        out=[self.format_date(text[0]),text[3]+" "+text[4],self.format_number(text[7])]
        return out  

class DepotParser(Parser):
    def __init__(self, dirName):
        out = []
        listOfFile = os.listdir(dirName)
        self.all_information = {}
        self.stocks = []
        self.fonds = []
        self.ISIN = {}
        for file in listOfFile:
            date = datetime.datetime.strptime(file[6:16], '%d.%m.%Y').date()            
            try:
                self.all_information[date], new_stocks, new_fonds = self.parse(dirName,file)
                self.stocks += (new_stocks)
                self.fonds += (new_fonds)
            except:
                pass
        self.fonds = list(set(self.fonds))
        self.stocks = list(set(self.stocks))

    def parse(self,directory,file):
        stocks = []
        fonds = []
        with open(os.path.join(directory,file), encoding = "ISO-8859-1") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
            out = []
            for row in spamreader:
                if len(row)>0:
                    if row[0] == "Aktien" or row[0] == "Fonds":
                        if row[1] not in self.ISIN:
                            self.ISIN[row[1]] = row[2]
                        try:
                            out.append([self.ISIN[row[1]], int(row[3]), self.format_number(row[5]), self.format_number(row[10])])
                            if row[0] == "Aktien":
                                stocks.append(self.ISIN[row[1]])
                            else:
                                fonds.append(self.ISIN[row[1]])
                        except:
                            print("corrupted file: ", file)

        return out, stocks, fonds

class Keywords():
    def __init__(self,file):
        with open(file) as json_data:
            d = json.load(json_data, object_pairs_hook=collections.OrderedDict)
        self.IN = [d['Level1']['Einkommen'],d['Level2']['Einkommen']]
        self.OUT = [d['Level1']['Ausgaben'],d['Level2']['Ausgaben']]
        self.INTERNAL = [d['Level1']['Internal'],d['Level2']['Internal']]

        self.is_included = [[],[]]

        for i in range(len(self.IN)):
            for k in list(list(self.IN[i].keys()) + list(self.OUT[i].keys())):
                if k[-2:] != "**":
                    self.is_included[i].append(k) 
