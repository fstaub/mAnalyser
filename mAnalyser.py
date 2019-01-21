import os 
import sys 
import gui 
import parser
import analyse


# set up paths
main_path = os.getcwd()

KEYS = parser.Keywords(os.path.join(main_path,"Data","config.json"))

all_accounts = []
for d in os.listdir(os.path.join(main_path,"Data")):
    print(d)
    if (d == "PayPal"):
        PayPal = parser.PayPal_Parser(os.path.join(main_path,"Data",d,""),KEYS)
        all_accounts.append(PayPal)
    if (d == "DiBa"):
        DiBa = parser.DiBa_Parser(os.path.join(main_path,"Data",d,""),KEYS)        
        all_accounts.append(DiBa)
    if (d == "CA"):
        CA = parser.CA_Parser(os.path.join(main_path,"Data",d,""),KEYS)  
        all_accounts.append(CA)
    if (d == "LBB"):
        LBB = parser.LBB_Parser(os.path.join(main_path,"Data",d,""),KEYS)  
        all_accounts.append(LBB)

money = analyse.Balance(all_accounts,KEYS)        

# print(money.incoming)   
# 
app = gui.QApplication(sys.argv)
ex = gui.App(money,KEYS)
sys.exit(app.exec_())                                
