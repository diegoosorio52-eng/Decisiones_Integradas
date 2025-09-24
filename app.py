from flask import Flask, render_template
import pandas as pd
from flask import Flask, render_template, request, redirect
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
        # Método para Windows
        subprocess.run(['taskkill', '/f', '/im', 'ngrok.exe'], 
                      capture_output=True, timeout=10)
        print("✅ Procesos ngrok terminados")
    except Exception as e:
        print(f"⚠️ Error terminando procesos: {e}")
    
    # También usar el método de pyngrok
    try:
        ngrok.kill()
    except:
        pass
    
    time.sleep(2)  # Esperar a que los procesos terminen

def setup_ngrok_tunnel(port=5000):
    """Configura el túnel ngrok de manera robusta"""
    # Terminar procesos existentes primero
    kill_ngrok_processes()
    
    # Esperar un poco más
    time.sleep(3)
    
    try:
        # Configurar ngrok para que no monitoree en segundo plano
        conf.get_default().monitor_thread = False
        
        # Conectar el túnel
        tunnel = ngrok.connect(port, bind_tls=True)
        print(f"✅ Túnel ngrok creado exitosamente")
        return tunnel
    except Exception as e:
        print(f"❌ Error creando túnel: {e}")
        print("Intentando método alternativo...")
        
        # Intentar método más simple
        try:
            kill_ngrok_processes()
            time.sleep(3)
            tunnel = ngrok.connect(port)  # Sin bind_tls
            print(f"✅ Túnel creado con método alternativo")
            return tunnel
        except Exception as e2:
            print(f"❌ Error crítico: {e2}")
            print("💡 Ejecuta 'taskkill /f /im ngrok.exe' manualmente")
            return None

# Registrar cleanup al salir
atexit.register(kill_ngrok_processes)

###############################################################################################
######################################## PROYECTO  #########################################
###############################################################################################

@app.route('/')
def header():
    return render_template('header.html')

######################################## BIM ACUEDUCTOS #########################################

@app.route('/bim-acueductos')  # Ruta más simple
def bim_acueductos():
    return render_template('bim-acueductos.html')


if __name__ == "__main__":
    port = 5000

    print("🚀 Iniciando servidor Flask con ngrok...")
    
    # Configurar ngrok de manera robusta
    ngrok_tunnel = setup_ngrok_tunnel(port)
    
    if ngrok_tunnel:
        print("🌐 URL pública:", ngrok_tunnel.public_url)
        print("✅ Servidor listo para recibir conexiones")
    else:
        print("⚠️  No se pudo crear el túnel ngrok, ejecutando solo localmente")
        print("🌐 URL local: http://127.0.0.1:5000")

    # Ejecutar Flask (debug=False para mejor compatibilidad con ngrok)
    app.run(host="0.0.0.0", port=port, debug=False)