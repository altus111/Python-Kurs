#!/usr/bin/python
 
# ------------------------------------------------------------------
# Name  : WeatherLogger.py
# Source: https://github.com/altus111/Python-Kurs/blob/main/WeatherLogger.py
#
# Description: Polling REST Service and write values to console
# https://openweathermap.org/current
#
# Autor: Markus Altenburger
#
# History:
# 01-Sep-2025   Markus Altenburger     Initial Version
#
# ------------------------------------------------------------------

import json
import requests
import urllib.parse
import time
from time import sleep
from datetime import datetime
import csv
import inspect
import os
from tabulate import tabulate
########### Konfiguration ###########


# Absoluten Pfad zur Datei config.json ermitteln
script_dir = os.path.dirname(os.path.abspath(__file__))  # Pfad zum aktuellen Skript
config_path = os.path.join(script_dir, '..', 'config.json')  # Eine Ebene höher

# Datei öffnen und laden
try:
    with open(config_path, 'r') as f:
        config = json.load(f)
    print("Konfiguration erfolgreich geladen.")
except FileNotFoundError:
    print(f"Datei nicht gefunden: {config_path}")
except json.JSONDecodeError:
    print("Fehler beim Parsen der config.json")

#with open(config_path) as f:
#    config = json.load(f)

end_point_url = config["WeatherPro"]["Endpoint_URL"]
appId = config["WeatherPro"]["ApiKey"]
check_if_first_run = "y"
########### Benutzereingaben ###########
def user_input():
    global ort
    global language
    global units
    global units_letter
    global check_if_first_run
    global polling_time
    print("Bitte geben Sie die folgenden Parameter ein:")
    print("Drücken Sie Enter für die Vorgabewerte in eckigen Klammern")
    default_mode = "a"
    mode = input("Datenlogger neu oder anhaengen [n,*a]?")
    if mode == "":
        mode = default_mode
    default_polling= 5
    polling_time = input(f"Polling-Time {default_polling} sek:")
    if polling_time == "":
        polling_time = default_polling
    
    ort_default = 'Balgach'
    ort = input(f"Ort  [*{ort_default}]   :")
    if ort == "":
        ort = ort_default
    ort_encoded = urllib.parse.quote(ort)
    
    language_default = 'de'
    language = input(f"Sprache [*{language_default},el,en,fr,hr,it]:")
    if language == '':
        language = language_default

    units_default = "metric"
    units = input(f"Units [*{units_default},standard, imperial]:")
    if units == '':
        units = units_default
        units_letter='°C'
    if units == 'imperial':
        units_letter='°F'
    elif units == 'standard':
        units_letter='K'
    check_if_first_run = "n"
######## Definitionen ########    
def check_response(responseStr):
    print("Du bist in Funktion:", inspect.currentframe().f_code.co_name)
    jsonResponse = json.loads(responseStr)
    print(f'responsestr: {jsonResponse}')
    code = jsonResponse["cod"]
    meldung = "ok"
    if "message" in jsonResponse:
        print("Meldung:", jsonResponse["message"])
        meldung = jsonResponse["message"]
    else:
        print("Key 'message' ist nicht vorhanden.")
    
    #        
    #print(f'Code:{jsonResponse["cod"]} Meldung: {jsonResponse["message"]}')
    return code, meldung
def write2file(file,line,seperator,mode):
    f=file
    print("Du bist in Funktion:", inspect.currentframe().f_code.co_name)
    print(f'schreibe linie:{line} in datei {file} im modus {mode}')
    with open(file, mode=mode, newline="", encoding="utf-8") as datei:
        writer = csv.writer(datei,delimiter=seperator)
        writer.writerow(line)

def  print2console(pfad):
    with open(pfad, 'r', encoding='utf-8') as datei:
       # for zeile in datei:
       #     print(zeile.strip())       
        reader = csv.reader(datei, delimiter=';')
        daten = list(reader)
        headers = daten[0]
        rows = daten[1:]
        print(tabulate(rows, headers=headers, tablefmt="grid"))


def endpoint_def():
    print("Du bist in Funktion:", inspect.currentframe().f_code.co_name)
    params_end_point = {
            'appid': appId,
            'q'    : ort,
            'units': units,
            'lang' : language,
            'mode' : '',          # xml, html    
        }    

    return params_end_point

def logger(counter):
    csv_datei = "Wetterlogger.csv"
    log_datei = "Wetterlogger.log"
    params_end_point =endpoint_def()

    max_counter = 1
    #counter = 0    
    doLoop = True
    while doLoop == True:
        print(f"Messung-Nr :{counter}")
        if False:
            request_url = f'{end_point_url}?q={ort_encoded}&units={units}&lang={language}&appid={appId}'
            print(f'Request:{request_url}')
            response = requests.get(request_url)
        else:
            response = requests.get(end_point_url, params=params_end_point)
        
        responseStr = response.text       
        jsonResponse = json.loads(responseStr)
        code, meldung = check_response(responseStr)
        print("Rückgabewert von check_response Code    :", code)
        if code == 200:
           # print(write2file(responseStr,log_datei))
            
            
            print("Zeige die einzelnen Felder!")
            print(f"   Ortsname    :{jsonResponse['name']}")
            print(f"   Land        :{jsonResponse['sys']['country']}")
             
            print(f"   Temp        :{jsonResponse['main']['temp']}{units_letter}")
            print(f"   Druck       :{jsonResponse['main']['pressure']}hPa")
            print(f"   Feuchtigkeit:{jsonResponse['main']['humidity']}%")
            print(f"   Desc:{jsonResponse['weather'][0]['description']}")
            print(f"   Desc:http://openweathermap.org/img/w/{jsonResponse['weather'][0]['icon']}.png")
            
            seperator = ";"
            temp = f"{jsonResponse['main']['temp']}"
            druck = f"{jsonResponse['main']['pressure']}"
            hum = f"{jsonResponse['main']['humidity']}"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            description = jsonResponse['weather'][0]['description']
            print(f"time:{timestamp}")
            
            print(timestamp,temp,druck,hum, sep = seperator)

            if counter == 0:
                header = ["Datum","Ort","Temperatur °C", "Druck hPa", "Feuchtigkeit %", "Beschreibung"]  
                write2file(log_datei,header,seperator,"w")   
            else:
                line = [timestamp,ort,temp,druck,hum,description]
                write2file(log_datei,line,seperator,"a")
            sleep(polling_time)
            '''
            counter+=1

            if counter == max_counter:
                doLoop=False  #hier abbrechen
            '''

            doLoop=False    
                
                
        else:
            doLoop=False  #hier abbrechen
            code, meldung = check_response(responseStr)
            print("Rückgabewert der Funktion Code    :", code)
            print("Rückgabewert der Funktion Meldung :", meldung)


######## Main ########
if check_if_first_run == "y":
    print("Erster Programmstart")
    user_input()
    logger('0')
orte = ("St.Gallen","Balgach","Uster","Bregenz","München")
for ort in orte:
    logger(1)
print2console("Wetterlogger.log")
