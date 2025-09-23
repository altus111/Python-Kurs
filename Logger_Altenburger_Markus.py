#!/usr/bin/python3
import sys
import os
import requests
import json
import urllib.parse
from time import sleep
from datetime import datetime
import inspect
import csv
from enum import Enum
#from Wetterdaten.user_input.input_handler import userInput -> spaeter benoetigt
class userInput:
    def __init__(self, pfad: str = "./", file_name: str = "wetterlogger.log", ort: str = "Balgach", language: str = "de", units: str = "metric",
                 polling_time: int = 5, mode: str = "a", delimiter: str = ";", max_entries: int = 10):
        self._file_path = pfad
        self._file_name = file_name
        self._delimiter = delimiter
        self._max_entries = max_entries
        self._ort = ort
        self._language = language
        self._units = units
        self._polling_time = polling_time
        self._mode = mode

    def __str__(self):
        return f"""
            Logfile      : {self.file_name}
            Pfad         : {self.file_path}
            Ort          : {self.ort}
            Sprache      : {self.language}
            Units        : {self.units}
            Polling-Time : {self.polling_time} sek
            Mode         : {self.mode}
            Delimiter    : {self.delimiter}
            Max-Einträge : {self.max_entries}
        """

    @property
    def ort(self):
        return self._ort

    @ort.setter
    def ort(self, value):
        self._ort = value

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, value):
        self._language = value

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        self._units = value

    @property
    def polling_time(self):
        return self._polling_time

    @polling_time.setter
    def polling_time(self, value):
        self._polling_time = value

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = value

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        self._file_path = value

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name = value

    @property
    def delimiter(self):
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value):
        self._delimiter = value

    @property
    def max_entries(self):
        return self._max_entries

    @max_entries.setter
    def max_entries(self, value):
        self._max_entries = value


class LogStrategy(Enum):
    FIXED_SLICES = "FixedSlices"
    ONLY_CHANGES = "OnlyChanges"

class Logger:
    def __init__(self, file_path: str, file_name: str, append: str,
                 delimiter: str = ";", max_entries: int = 1000,
                 strategy: LogStrategy = LogStrategy.FIXED_SLICES,
                 time_format: str = "%Y-%m-%d %H:%M:%S"):
        self.file_path = file_path
        self.file_name = file_name
        self.writemode = append
        self.delimiter = delimiter
        self.max_entries = max_entries
        self.strategy = strategy
        self.time_format = time_format


        os.makedirs(file_path, exist_ok=True)
        self.full_path = os.path.join(file_path, file_name)

    def __str__(self):
        return (
            f"Logfile     : {self.full_path}\n"
            f"Pfad        : {self.file_path}\n"
            f"Dateiname   : {self.file_name}\n"
            f"Schreibmodus: {self.writemode}\n"
            f"Trennzeichen: {self.delimiter}\n"
            f"Max-Einträge: {self.max_entries}\n"
            f"Strategie   : {self.strategy.value}\n"
            f"Zeitformat  : {self.time_format}\n"
            
        )
    
    def write_header(self, log_file):
        with open(log_file, "w", newline="") as f:
            start_time = datetime.now().strftime(self.time_format)
            f.write(f"Filename: {self.file_name}, Start-Time: {start_time}\n")
            writer = csv.writer(f, delimiter=self.delimiter)
            writer.writerow(["Zeit", "Land", "Ort","Status", "Temperatur °C", "Feuchtigkeit %", "Wetterbeschreibung"])

 # -------- Logging --------


    def logging(self, level, message):
        print(f'mess: {message}')
        #now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        now = datetime.now().strftime(self.time_format)
        entry_line = f"{now},{level},{message}\n"
        file = self.full_path

        if os.path.exists(file) ==False:
            print("Datei existiert nicht")
            self.write_header(file)

        else:
            if len(file) == 0:
                # Datei ist leer, Header schreiben
                self.write_header(file)
            if self.writemode == "w":
                self.write_header(file)

            with open(file, "r") as f:            
                lines = f.readlines()

            # ab Zeile 3 sind Datenzeilen
            header = lines[:2]
            if self.writemode == "w":
                data = []
                data.insert(0, entry_line)
            else:
                data = lines[2:self.max_entries+2]  # +2 wegen Headerzeilen
                data.insert(0, entry_line)

            with open(file, "w", newline="") as f:
                f.writelines(header)
                f.writelines(data)
    
#-----
 
    @property
    def delimiter(self):
        return self._delimiter
    @delimiter.setter 
    def delimiter(self, value):
        self._delimiter = value
    @property
    def max_entries(self):
        return int(self._max_entries)
    @max_entries.setter
    def max_entries(self, value):
        self._max_entries = value


# Absoluten Pfad zur Datei config.json ermitteln
# config-datei öffnen und laden

script_dir = os.path.dirname(os.path.abspath(__file__))  # Pfad zum aktuellen Skript
config_path = os.path.join(script_dir, '..', 'config.json')  # Eine Ebene höher weil config.json dort liegt
if os.path.exists(config_path) == True:
    try:
        with open(config_path, 'r') as f: #mit with wird die Datei automatisch geschlossen
            config = json.load(f)
        print("Konfiguration erfolgreich geladen.")
    except FileNotFoundError:
        print(f"Datei nicht gefunden: {config_path}")
    except json.JSONDecodeError:
        print("Fehler beim Parsen der config.json")

    end_point_url = config["WeatherPro"]["Endpoint_URL"]
    appId = config["WeatherPro"]["ApiKey"]
else: #nur zu Testzwecken
    print(f"Datei nicht gefunden: {config_path}")
    end_point_url = "https://api.openweathermap.org/data/2.5/weather"
    appId = "9acc5ac99ab484b08d9c8f9e3b6dcccb"

def user_input():
    userInputs = userInput()
    print("Bitte geben Sie die folgenden Parameter ein:")
    print("Drücken Sie Enter für die Vorgabewerte in eckigen Klammern")
  

    default_Filename = "wetter.log"
    filename = input(f"Logfile Name [*{default_Filename}]:")
    if filename == "":
        filename = default_Filename
    userInputs.file_name = filename
    default_Path = "./"
    path = input(f"Logfile Pfad [*{default_Path}]:")
    if path == "":
        path = default_Path
    userInputs.file_path = path

    default_mode = "a"
    mode = input("Datenlogger neu oder anhaengen [n,*a]?")
    if mode == "":
        mode = default_mode
    elif mode == 'n':
        mode = 'w' 
    userInputs.mode = mode

    default_polling= 5
    polling_time = input(f"Polling-Time {default_polling} sek:")
    if polling_time == "":
        polling_time = default_polling
    userInputs.polling_time = polling_time

    ort_default = 'Balgach'
    ort = input(f"Ort  [*{ort_default}]   :")
    if ort == "":
        ort = ort_default
    ort_encoded = urllib.parse.quote(ort)
    userInputs.ort = ort_encoded
    language_default = 'de'
    language = input(f"Sprache [*{language_default},el,en,fr,hr,it]:")
    if language == '':
        language = language_default
    userInputs.language = language

    units_default = "metric"
    units = input(f"Units [*{units_default},standard, imperial]:")
    if units == '':
        units = units_default
        units_letter='°C'
    if units == 'imperial':
        units_letter='°F'
    elif units == 'standard':
        units_letter='K'
    userInputs.units = units

    delimiter_default = ";"
    delimiter = input(f"Trennzeichen [*{delimiter_default},'_','-']:")
    if delimiter == '':
        delimiter = delimiter_default
    userInputs.delimiter = delimiter

    max_entries_default = 1000
    max_entries = input(f"Maximale Anzahl Einträge [*{max_entries_default}]:")
    if max_entries == '':
        max_entries = max_entries_default
    userInputs.max_entries = max_entries

    return userInputs

def createLogLine(separator, jsonResponse):
    #separator = ";"
    zeit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ort = jsonResponse["name"]
    land = jsonResponse["sys"]["country"]
    temperatur=f'{jsonResponse["main"]["temp"]}'
    feuchtigkeit = f'{jsonResponse["main"]["humidity"]}'
    wetterbeschreibung = jsonResponse["weather"][0]["description"]
    log_line = [zeit, land,ort, temperatur, feuchtigkeit, wetterbeschreibung]
    log_line = separator.join(log_line)
    return log_line
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
if __name__ == '__main__':
    
    userInputs = user_input()
    print(userInputs)
    log = Logger(userInputs.file_path, userInputs.file_name, append=(userInputs.mode), delimiter=";", max_entries=userInputs.max_entries, strategy=LogStrategy.FIXED_SLICES)
    print(log)
    sleep(2)
    orte = ['Balgach', 'Gams', 'Feldkirch', 'New York', 'London', 'Tokio']
    max_requests = 2
    counter = 0
    doloop = True
    while doloop:        
        sleep(int(userInputs.polling_time))
        for ort in orte:
            request_url = f'{end_point_url}?q={ort}&units={userInputs.units}&lang={userInputs.language}&appid={appId}'
            response = requests.get(request_url)
            responseStr = response.text
            code, meldung = check_response(responseStr)
            if code == 200:
                jsonResponse = json.loads(responseStr)
                print("Erfolgreiche Anfrage")
                tmpTemp = jsonResponse["main"]["temp"]
                tmpTemp = round(tmpTemp, 1)
                jsonResponse["main"]["temp"] = tmpTemp

                print(f'Aktuelle Temperatur in {jsonResponse["name"]}: {jsonResponse["main"]["temp"]}')
                line = createLogLine(";", jsonResponse)
                log.logging("Info",line)
            else:
                log.logging("Error",f'Fehler bei der Anfrage. Code: {code}, Meldung: {meldung}')
                print(f'Fehler bei der Anfrage. Code: {code}, Meldung: {meldung}')
        counter += 1
        print(f'Anzahl Requests: {counter}')
        if counter >= max_requests:
            doloop = False
    print("Fertig") 