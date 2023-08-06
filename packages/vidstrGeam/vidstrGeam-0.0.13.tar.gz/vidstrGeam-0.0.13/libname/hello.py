import requests, json, time, urllib3
from requests.structures import CaseInsensitiveDict
from requests.sessions import session
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

R = " \033[1;31m"
B = "\033[1;34m"
Y = "\033[1;33m"
RS = "\033[0m"
G = "\033[32m"
W = "\033[1;37m"
P = "\033[95m"

print("\n")
print("        " + B + " ▄▄ •  ▄▄▄·"+ RS + G +".▄▄ · • ▌ ▄ ·. .▄▄ · "+ RS)
print("        " + B + "▐█ ▀ ▪▐█ ▄█"+ RS + G +"▐█ ▀. ·██ ▐███▪▐█ ▀."+ RS)
print("        " + B + "▄█ ▀█▄ ██▀·"+ RS + G +"▄▀▀▀█▄▐█ ▌▐▌▐█·▄▀▀▀█▄"+ RS)
print("        " + B + "▐█▄▪▐█▐█▪·•"+ RS + G +"▐█▄▪▐███ ██▌▐█▌▐█▄▪▐█"+ RS)
print("        " + B + "·▀▀▀▀ .▀   "+ RS + G +" ▀▀▀▀ ▀▀  █▪▀▀▀ ▀▀▀▀ "+ RS)
print("\033[93m[\033[0m \033[36mFollow on Github :-\033[0m \033[36mhttps://github.com/naimkowshik \033[93m]\033[0m")
print("\n")

Number = input("        " + W + "[" + G + "+" + W + "]" + G + " Enter Your" + B + " Number" + Y + " : " + RS)

def world():
    print(" "*10 + "✒️ " + P +" Flexi Plan " + "🧾")
    flexiplan_data = {"payment_mode":"mobile_balance","longevity":3,"voice":0,"data":0,"fourg":0,"bioscope":0,"sms":50,"mca":0,"msisdn":Number,"price":6,"bundle_id":7,"is_login":"false"}
    flexiplan_data_url = requests.post('https://gpwebms.grameenphone.com/api/v1/flexiplan-purchase/activation', json=flexiplan_data)
    flexiplan_data_json = json.loads(flexiplan_data_url.content)
    print(G + 'Message Status ' + Y + ': ' + RS + B + "FlexiPlan Successful" + RS + " ✔️" + "\n")