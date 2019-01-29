import os 
import sys 
import gui 
import parser
import analyse


# set up paths
main_path = os.getcwd()

KEYS = parser.Keywords(os.path.join(main_path,"Data","config.json"))

stocks = parser.DepotParser(os.path.join(main_path,"Data","Stocks",""))
depot = analyse.Depot(stocks)

all_accounts = []
all_account_names = []
for d in os.listdir(os.path.join(main_path,"Data","Accounts")):
    if (d == "PayPal"):
        for x in os.listdir(os.path.join(main_path,"Data","Accounts",d)):
            PayPal = parser.PayPal_Parser(os.path.join(main_path,"Data","Accounts",d,x,""),KEYS)
            all_accounts.append(PayPal)
            all_account_names.append(x)
    if (d == "DiBa"):
        for x in os.listdir(os.path.join(main_path,"Data","Accounts",d)):
            DiBa = parser.DiBa_Parser(os.path.join(main_path,"Data","Accounts",d,x,""),KEYS)        
            all_accounts.append(DiBa)
            all_account_names.append(x)
    if (d == "CA"):
        for x in os.listdir(os.path.join(main_path,"Data","Accounts",d)):
            CA = parser.CA_Parser(os.path.join(main_path,"Data","Accounts",d,x,""),KEYS)  
            all_accounts.append(CA)
            all_account_names.append(x)
    if (d == "LBB"):
        for x in os.listdir(os.path.join(main_path,"Data","Accounts",d)):
            LBB = parser.LBB_Parser(os.path.join(main_path,"Data","Accounts",d,x,""),KEYS)  
            all_accounts.append(LBB)
            all_account_names.append(x)
accounts = analyse.Balance(all_accounts, all_account_names, KEYS)   
accounts.include_depot(depot)

app = gui.QApplication(sys.argv)
ex = gui.App(depot, accounts,KEYS,3)
sys.exit(app.exec_())                                
