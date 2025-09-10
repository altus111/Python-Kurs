#!/usr/bin/python3
import os
import requests
import json
import urllib.parse
import time
from time import sleep
from datetime import datetime
import inspect
import csv
from enum import Enum
class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class LogStrategy(Enum):
    FIXED_SLICES = "FixedSlices"
    ONLY_CHANGES = "OnlyChanges"
class userInput:
    def __init__(self, ort: str = "Balgach", language: str = "de", units: str = "metric",
                polling_time: int = 5, mode: str = "a"):
        self._ort = ort
        self._language = language
        self._units = units
        self._polling_time = polling_time
        self._mode = mode
    def __str__(self):
        return f'''
            Ort          : {self.ort}
            Sprache      : {self.language}
            Units        : {self.units}
            Polling-Time : {self.polling_time} sek
            Mode         : {self.mode}
        '''
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
class logger:
    def __init__(self, file_path: str, file_name: str, append: bool = False,
                delimiter: str = "", max_entries: int = 1000,
                strategy: LogStrategy = LogStrategy.FIXED_SLICES,
                time_format: str = "%Y-%m-%d %H:%M:%S"):
        self._file_path = file_path
        self._file_name = file_name
        self._append = append
        self._delimiter = delimiter
        self._max_entries = max_entries
        self._strategy = strategy
        self._time_format = time_format
        self._log_entries = []
        self._title = []
        self._header = []
        os.makedirs(file_path, exist_ok=True) # Verzeichnis erstellen, falls es nicht existiert
        self.full_path = os.path.join(file_path, file_name) # Vollständigen Pfad zur Logdatei erstellen
    def __str__(self):
        return f'''
            Logfile     : {self.full_path}
            Pfad        : {self.file_path}
            Dateiname   : {self.file_name}
            Anfuegen     : {self.append}
            Trennzeichen: {self.delimiter}
            Max-Einträge: {self.max_entries}
            Strategie   : {self.strategy}
            Zeitformat  : {self.time_format}
            Einträge    : {len(self._log_entries)}
        '''
    @property
    def file_name(self):
        return self._file_name
    @file_name.setter
    def file_name(self, value):
        self._file_name = value

    @property
    def file_path(self):
        return self._file_path
    @file_path.setter
    def file_path(self, value):
        self._file_path = value
    @property
    def time_format(self):
        return self._time_format
    @time_format.setter
    def time_format(self, value):
        self._time_format = value
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

    @property
    def strategy(self):
        return self._strategy
    @strategy.setter
    def strategy(self, value):
        self._strategy = value

    @property
    def append(self):
        return self._append
    @append.setter
    def append(self, value):
        self._append = value
    @property
    def log_entries(self):
        return self._log_entries
    @log_entries.setter
    def log_entries(self):
        l = self.read_logfile()
        print(f'linie : {l}')
        self._log_entries = l
        return self._log_entries
    def header_line1(self): #in xml-format
        linie1 = f"Filename: {self.file_name}, Start-Time: {datetime.now().strftime(self.time_format)}"
        return linie1
    def header_title(self): #in xml-format
        return createTitle(self.delimiter)
    def read_logfile(self):
        if os.path.exists(self.full_path):
            with open(self.full_path, 'r') as log_file:
                lines = log_file.readlines()
                print(lines)
                return lines
        else:
            print(f"Datei {self.full_path} existiert nicht.")
            return []


    def write_log(self):
        #timestamp = datetime.now().strftime(self.time_format)
        #log_entry = f"{timestamp}{self.delimiter}{level.value}{self.delimiter}{message}"
        #self.log_entries.append(log_entry)
        if len(self._log_entries) > self.max_entries:
            self._log_entries.pop(0)  # Ältesten Eintrag entfernen
        mode = 'a' if self.append else 'w'
        with open(self.full_path, mode) as log_file:
            if os.path.getsize(self.full_path) == 0:  # Datei ist leer, Header schreiben
                log_file.write(self.header_line1() + "\n")
                log_file.write(self.header_title() + "\n")
            for entry in self._log_entries:
                log_file.write(entry + "\n")

# Absoluten Pfad zur Datei config.json ermitteln
script_dir = os.path.dirname(os.path.abspath(__file__))  # Pfad zum aktuellen Skript
config_path = os.path.join(script_dir, '..', 'config.json')  # Eine Ebene höher weil config.json dort liegt

# config-datei öffnen und laden
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

def user_input():
    userInputs = userInput()
    print("Bitte geben Sie die folgenden Parameter ein:")
    print("Drücken Sie Enter für die Vorgabewerte in eckigen Klammern")
    default_mode = "a"
    mode = input("Datenlogger neu oder anhaengen [n,*a]?")
    if mode == "":
        mode = default_mode
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
    check_if_first_run = "n"
    return userInputs
def createTitle(separator):
    title = ["Zeit", "Land","Ort", "Temperatur °C", "Feuchtigkeit %", "Wetterbeschreibung"]
    title = separator.join(title)
    return title
def createLogLine(separator, jsonResponse):
    #separator = ";"
    zeit = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ort = jsonResponse["name"]
    land = jsonResponse["sys"]["country"]
    temperatur= f'{jsonResponse["main"]["temp"]}'
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

    log = logger("./", "test.log", append=(userInputs.mode == "a"), delimiter=";", max_entries=1000, strategy=LogStrategy.FIXED_SLICES)
    print(log)

    request_url = f'{end_point_url}?q={userInputs.ort}&units={userInputs.units}&lang={userInputs.language}&appid={appId}'
    print(f'Request: {request_url}')

    response = requests.get(request_url)
    responseStr = response.text
    code, meldung = check_response(responseStr)

    if code == 200:
        jsonResponse = json.loads(responseStr)
        print("Erfolgreiche Anfrage")
        print(f'Aktuelle Temperatur in {jsonResponse["name"]}: {jsonResponse["main"]["temp"]}')
        log._log_entries.append(createLogLine(";", jsonResponse))
        log.write_log()
    else:
        print(f'Fehler bei der Anfrage. Code: {code}, Meldung: {meldung}')
