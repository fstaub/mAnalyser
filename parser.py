import os 
import json 
import csv

class Parser():
    def filter_redundant(self,data):
        out = []
        internal = []
        for entry in data:
            if  max([entry[1].find(x) for x in self.keywords.INTERNAL])<0:
                out.append(entry)
            else:
                internal.append(entry)
        return out, internal

    def format_number(self,in_string):
        return float(in_string.replace(".","").replace(",","."))

    def __init__(self,dirName,keywords):
        self.keywords=keywords
        out = []
        listOfFile = os.listdir(dirName)
        for file in listOfFile:
            out = out + (self.parse(dirName+file))
        self.all_information, self.internal_transfers = self.filter_redundant(out)


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
        out=[text[0],self.purpose(text[2],text[3],text[4]),self.format_number(text[-2])]
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
        out=[text[1],text[3],self.format_number(text[-1])]
        return out


class CA_Parser(Parser):
    def parse(self,file):
        data=[]
        with open(file, newline='', encoding = "ISO-8859-1") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for row in spamreader:
                    data.append(self.format_entry(row))
        return data

    def format_entry(self,text):
        out=[text[0],text[1],self.format_number(text[-1])]
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
        out=[text[0],text[3]+" "+text[4],self.format_number(text[7])]
        return out  

class Keywords():
    def __init__(self,file):
        with open(file) as json_data:
            d = json.load(json_data)
        self.IN = d['Einkommen']
        self.OUT = d['Ausgaben']
        self.INTERNAL = d['Internal']
