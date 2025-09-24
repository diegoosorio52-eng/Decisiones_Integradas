from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from pyngrok import ngrok
import subprocess
import csv
import numpy as np
import pickle
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pyngrok import ngrok, conf
import time
import atexit

app = Flask(__name__)

def kill_ngrok_processes():
    """Termina todos los procesos ngrok existentes"""
    try:
        subprocess.run(['taskkill', '/f', '/im', 'ngrok.exe'], 
                      capture_output=True, timeout=10)
        print("✅ Procesos ngrok terminados")
    except Exception as e:
        print(f"⚠️ Error terminando procesos: {e}")
    
    try:
        ngrok.kill()
    except:
        pass
    
    time.sleep(2)

def setup_ngrok_tunnel(port=5000):
    """Configura el túnel ngrok de manera robusta"""
    kill_ngrok_processes()
    time.sleep(3)
    
    try:
        conf.get_default().monitor_thread = False
        tunnel = ngrok.connect(port, bind_tls=True)
        print(f"✅ Túnel ngrok creado exitosamente")
        return tunnel
    except Exception as e:
        print(f"❌ Error creando túnel: {e}")
        try:
            kill_ngrok_processes()
            time.sleep(3)
            tunnel = ngrok.connect(port)
            print(f"✅ Túnel creado con método alternativo")
            return tunnel
        except Exception as e2:
            print(f"❌ Error crítico: {e2}")
            return None

atexit.register(kill_ngrok_processes)

###############################################################################################
######################################## RUTAS DEFINIDAS #########################################
###############################################################################################

@app.route('/')
def header():
    return render_template('header.html')

# Ruta existente
@app.route('/bim-acueductos')
def bim_acueductos():
    return render_template('bim-acueductos.html')

# NUEVAS RUTAS PARA LOS ENLACES QUE FALTAN
@app.route('/analitica-datos')
def analitica_datos():
    return render_template('analitica-datos.html')

@app.route('/costos-ambientales')
def costos_ambientales():
    return render_template('costos-ambientales.html')

@app.route('/gestion-riesgos')
def gestion_riesgos():
    return render_template('gestion-riesgos.html')

@app.route('/capacitacion')
def capacitacion():
    return render_template('capacitacion.html')

# Ruta adicional que mencionó el error
@app.route('/bim-construccion')
def bim_construccion():
    return render_template('bim-construccion.html')

if __name__ == "__main__":
    port = 5000

    print("🚀 Iniciando servidor Flask con ngrok...")
    
    ngrok_tunnel = setup_ngrok_tunnel(port)
    
    if ngrok_tunnel:
        print("🌐 URL pública:", ngrok_tunnel.public_url)
        print("✅ Servidor listo para recibir conexiones")
    else:
        print("⚠️  No se pudo crear el túnel ngrok, ejecutando solo localmente")
        print("🌐 URL local: http://127.0.0.1:5000")

    app.run(host="0.0.0.0", port=port, debug=False)