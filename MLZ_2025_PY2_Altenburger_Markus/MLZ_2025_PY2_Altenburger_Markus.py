#!/usr/bin/python

# ------------------------------------------------------------------
# Name  : 01_SenseHat_Flask.py
# https://raw.githubusercontent.com/walter-rothlin/RaspberryPi4PiPlates/refs/heads/main/Python_Raspberry/04_Sense_Hat/Flask/LN/SenseHat/Vorbereitung/01_SenseHat_Flask.py
#
# Description: Stellt Web-Applikationen und REST-Services für die Steuerung der LED-Matrix
#              und das Auslesen der Sensoren auf dem Sense-Hat

#
#
# Autor: Walter Rothlin
#
# History:
# 01-Jul-2025  Walter Rothlin     Initial Version
# 04-Oct-2025  Walter Rothlin     Prepared for HBU MLZ 2025
# 06-Oct-2025  Walter Rothlin     Defined and implemented all Endpoints
# 08-Oct-2025  Walter Rothlin     Prepared for MLZ
# ------------------------------------------------------------------

import ast
#from ast import arguments
from flask import *
from sense_hat import SenseHat
from time import sleep
from datetime import datetime
import inspect
from class_MySenseHat import MySenseHat
from class_Converter import Converter
# ===========================================
# globale Variablen
# ===========================================
version = 'Markus Altenburger (V0.0)'
request_log = []


# ===========================================
# Common functions for URL-Parameter handling
# ===========================================
def get_http_parameter(request, name_endpoint='unknown', verbal=False):
    if request.method == "GET":
        all_parameters = dict(request.args)
        if verbal:
            print(f"get_http_parameter: GET: {all_parameters}")
    elif request.method == "POST":
        all_parameters = dict(request.form)
        if verbal:
            print(f"get_http_parameter: POST: {all_parameters}")
    elif request.is_json:
        all_parameters = request.get_json()
        if verbal:
            print(f"get_http_parameter: JSON: {all_parameters}")
    else:
        all_parameters = {}

    call_debug = f'{request.method}: {name_endpoint}({all_parameters})'
    if verbal:
        print(call_debug)
    return all_parameters, call_debug


# ===========================================
# Application and Endpoints
# ===========================================
app = Flask(__name__)
#sense = SenseHat()
sense = MySenseHat()
sense.clear(color=(0, 0, 0))  # LED-Matrix löschen
mconvert = Converter()
# ====================
# Overall-Status
# ====================
@app.route('/get_status', methods=['GET'])
def get_status():
    request_log.append(f"{datetime.now().strftime('%d-%m-%y %H:%M:%S')}: get_status()")
    pixel_status = sense.get_pixels()
    humidity = sense.get_humidity()
    temperature = sense.get_temperature()
    pressure = sense.get_pressure()

    # print(pixel_status)
    return {'LED_Matrix': pixel_status,
            'Temperature': {'value': temperature, 'unit': '°C'},
            'Humidity': {'value': humidity, 'unit': '%'},
            'Pressure': {'value': pressure, 'unit': 'mBar'},
            }


# ====================
# LED-Matrix Endpoints
# ====================
@app.route('/set_rotation', methods=['GET', 'POST'])
def set_rotation():
    received_parameter, arguments = get_http_parameter(request, inspect.currentframe().f_code.co_name)
    print(f'2) {arguments}')
    r_value = received_parameter.get('r', 0)  # gibt '0' zurück
    try:
        r_value = mconvert.convert2Integer(r_value, default_value=0)
        if r_value not in (0, 90, 270, 180):
            return f'{r_value} ist ein ungültiger Wert für die Rotation.<br/><br/><a href="/">Back</a>'
        elif r_value == 0:
            return f'Keine Rotation durchgeführt (0).<br/><br/><a href="/">Back</a>'
        else:
            sense.rotate(r_value)
    except:
        return f'{r_value} ist ein ungültiger Wert für die Rotation.<br/><br/><a href="/">Back</a>'
    request_log.append(f"{datetime.now().strftime('%d-%m-%y %H:%M:%S')}: {arguments}")
    return render_template('index.html', version=version, request_log=request_log)

@app.route('/draw_line', methods=['GET', 'POST'])
def draw_line():
    received_parameter, arguments = get_http_parameter(request, inspect.currentframe().f_code.co_name)
    print(f'2) {arguments}')
    
    x1 = mconvert.convert2Integer(received_parameter.get('x_start', 0))
    y1 = mconvert.convert2Integer(received_parameter.get('y_start', 0))
    x2 =  mconvert.convert2Integer(received_parameter.get('x_end', 0))
    y2 =  mconvert.convert2Integer(received_parameter.get('y_end', 0))
    r =  mconvert.convert2Integer(received_parameter.get('r'))  
    g=  mconvert.convert2Integer(received_parameter.get('g'))  
    b =  mconvert.convert2Integer(received_parameter.get('b'))
    speed =  mconvert.convert2Float(received_parameter.get('draw_speed'), default_value=0, min=0, max=10)
    color = mconvert.convert2RGB(received_parameter.get('color'), (r, g, b))

    print(f'2) draw_line({x1}, {y1}, {x2}, {y2}, color={color}, speed={speed})')
    sense.clear()
    sense.draw_line(x1, y1, x2, y2, color=color, speed=speed)

    request_log.append(f"{datetime.now().strftime('%d-%m-%y %H:%M:%S')}: {arguments}")
    return render_template('index.html', version=version, request_log=request_log)

@app.route('/flip_h', methods=['GET', 'POST'])
def flip_h():
    received_parameter, arguments = get_http_parameter(request, inspect.currentframe().f_code.co_name)
    sense.flip_h()
    request_log.append(f"{datetime.now().strftime('%d-%m-%y %H:%M:%S')}: {arguments}")
    return render_template('index.html', version=version, request_log=request_log)
 

@app.route('/flip_v', methods=['GET', 'POST'])
def flip_v():
    received_parameter, arguments = get_http_parameter(request, inspect.currentframe().f_code.co_name)
    sense.flip_v()
    request_log.append(f"{datetime.now().strftime('%d-%m-%y %H:%M:%S')}: {arguments}")
    return render_template('index.html', version=version, request_log=request_log)


@app.route('/set_pixels', methods=['GET', 'POST'])
def set_pixels():
    return f'set_pixels() not to be implemented yet!<br/><br/><a href="/">Back</a>'


@app.route('/get_pixels', methods=['GET', 'POST'])
def get_pixels(typ='json'):
    if typ == 'json':
        pixel_status = sense.get_pixels()
        return {'LED_Matrix': pixel_status}
    else:
        return super().get_pixels()


@app.route('/set_pixel', methods=['GET', 'POST'])
def set_pixel():
    received_parameter, arguments = get_http_parameter(request, inspect.currentframe().f_code.co_name)
    print(f'2) {arguments}')
    orig_x = received_parameter.get('x', 0)
    orig_y = received_parameter.get('y', 0)
    orig_r = received_parameter.get('r', 0)
    orig_g = received_parameter.get('g', 0)
    orig_b = received_parameter.get('b', 0)
    x =  mconvert.convert2Integer(received_parameter.get('x', 0))
    y =  mconvert.convert2Integer(received_parameter.get('y', 0))
    r =  mconvert.convert2Integer(received_parameter.get('r', 0))
    g =  mconvert.convert2Integer(received_parameter.get('g', 0))
    b =  mconvert.convert2Integer(received_parameter.get('b', 0))
    color =  mconvert.convert2RGB(received_parameter.get('color'), (r, g, b))
    if received_parameter.get('pixel') is not None:
        tmp_color = received_parameter.get('pixel')
        color = ast.literal_eval(tmp_color)
        if isinstance(color, tuple) and len(color) == 3:
            orig_r = color[0]
            orig_g = color[1]
            orig_b = color[2]
            r =  mconvert.convert2Integer(orig_r, None)
            g =  mconvert.convert2Integer(orig_g, None)
            b =  mconvert.convert2Integer(orig_b, None)   
    print(f'2) set_pixel({x}, {y}, color={color})')
    if x is None or y is None:
        return f'Ungültige Koordinaten x={x}, y={y}.<br/><br/><a href="/">Back</a>'
    if x < 0 or x > 7 or y < 0 or y > 7:
        return f'Koordinaten x={x}, y={y} ausserhalb des gültigen Bereichs (0-7).<br/><br/><a href="/">Back</a>'
    if orig_r is None or orig_g is None or orig_b is None:
        return f'Ungültige Farbwerte r={orig_r}, g={orig_g}, b={orig_b}.<br/><br/><a href="/">Back</a>'
    if float(orig_r) < 0 or float(orig_r) > 255 or float(orig_g) < 0 or float(orig_g) > 255 or float(orig_b) < 0 or float(orig_b) > 255:
        return f'Farbwerte r={r}, g={g}, b={b} ausserhalb des gültigen Bereichs (0-255).<br/><br/><a href="/">Back</a>'
    sense.set_pixel(x, y, color=color)
    request_log.append(f"{datetime.now().strftime('%d-%m-%y %H:%M:%S')}: {arguments}")
    return render_template('index.html', version=version, request_log=request_log)


@app.route('/get_pixel', methods=['GET', 'POST'])
def get_pixel():
    received_parameter, arguments = get_http_parameter(request, inspect.currentframe().f_code.co_name)
    print(f'2) {arguments}')
    orig_x = received_parameter.get('x', 0)
    orig_y = received_parameter.get('y', 0)
    x =  mconvert.convert2Integer(received_parameter.get('x', 0))
    y =  mconvert.convert2Integer(received_parameter.get('y', 0))
    
    if x is None or y is None:
        return f'Ungültige Koordinaten x={x}, y={y}.<br/><br/><a href="/">Back</a>'
    if x < 0 or x > 7 or y < 0 or y > 7:
        return f'Koordinaten x={x}, y={y} ausserhalb des gültigen Bereichs (0-7).<br/><br/><a href="/">Back</a>'
    color = sense.get_pixel(x, y,typ='json')
    request_log.append(f"{datetime.now().strftime('%d-%m-%y %H:%M:%S')}: {arguments}")
    return f'Farbe des Pixels an Position ({x}, {y}): {color}<br/><br/><a href="/">Back</a>'
   
    


@app.route('/clear', methods=['GET', 'POST'])
def clear():
    print('clear called!!!')
    received_parameter, arguments = get_http_parameter(request, inspect.currentframe().f_code.co_name, verbal=True)
    print(f'40) {arguments}')
    colour =  mconvert.convert2RGB(received_parameter.get('colour'), (0, 0, 0))
    sense.clear(color=colour)

    request_log.append(f"{datetime.now().strftime('%d-%m-%y %H:%M:%S')}: {arguments}")
    return render_template('index.html', version=version, request_log=request_log)
    # return f'clear() not implemented yet!<br/><br/><a href="/">Back</a>'


@app.route('/show_message', methods=['GET', 'POST'])
def show_message():
    return f'show_message() not implemented yet!<br/><br/><a href="/">Back</a>'


@app.route('/show_letter', methods=['GET', 'POST'])
def show_letter():
    received_parameter, arguments = get_http_parameter(request, inspect.currentframe().f_code.co_name)
    print(f'2) {arguments}')
    s = received_parameter.get('s', '?')[0]
    text_colour =  mconvert.convert2RGB(received_parameter.get('text_colour'), (255, 255, 255))
    back_colour =  mconvert.convert2RGB(received_parameter.get('back_colour'), (0, 0, 0))

    print(f'2) show_letter({s}, {text_colour}, {back_colour})')
    sense.show_letter(s=s, text_colour=text_colour, back_colour=back_colour)

    request_log.append(f"{datetime.now().strftime('%d-%m-%y %H:%M:%S')}: {arguments}")
    return render_template('index.html', version=version, request_log=request_log)
    # return f'show_letter() not implemented yet!<br/><br/><a href="/">Back</a>'

# =====================
# Environmental sensors
# =====================
@app.route('/get_temperature', methods=['GET', 'POST'])
def get_temperature():
    return f'get_temperature() not implemented yet!<br/><br/><a href="/">Back</a>'


@app.route('/get_pressure')
def get_pressure():
    return f'get_pressure() not implemented yet!<br/><br/><a href="/">Back</a>'


@app.route('/get_humidity')
def get_humidity():
    return f'get_humidity() not implemented yet!<br/><br/><a href="/">Back</a>'


@app.route('/get_meteo_sensor_values')
def get_meteo_sensor_values():
    return f'get_meteo_sensor_values() not implemented yet!<br/><br/><a href="/">Back</a>'


@app.route('/get_weather')
def get_weather():
    return f'get_weather() not implemented yet!<br/><br/><a href="/">Back</a>'


@app.route('/')
def index():
    return render_template('index.html', version=version, request_log=request_log)


@app.route('/LED_Matrix_Tester')
def LED_Matrix_Tester():
    return render_template('LED_Matrix_Tester.html')



# ============================
# Enpoints in MySenseHat Class
# ============================


if __name__ == '__main__':
    from class_MySenseHat import MySenseHat
    sense = MySenseHat()
    sense.clear()
    #sense.draw_line(0, 2, 7, 6, (0, 255, 0))
    #sense.rotate(90)
    app.run(debug=True, use_reloader=False, host='192.168.0.35', port=5000)  # IP-Adresse des Raspberry Pi einsetzen