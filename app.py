from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import csv
import numpy as np
import pickle
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import os
import logging
from threading import Thread
import requests

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variable para health check
app_start_time = time.time()

# Detectar si estamos en Render o local
IS_RENDER = os.environ.get('RENDER') is not None
IS_LOCAL = not IS_RENDER

# Ngrok solo para desarrollo local
if IS_LOCAL:
    try:
        from pyngrok import ngrok, conf
        import subprocess
        import atexit
        
        def kill_ngrok_processes():
            """Termina todos los procesos ngrok existentes (solo local)"""
            try:
                # Para Windows
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
            """Configura el túnel ngrok de manera robusta (solo local)"""
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
        
    except ImportError:
        print("⚠️ Ngrok no disponible - modo Render")
        IS_LOCAL = False

###############################################################################################
######################################## RUTAS DEFINIDAS #########################################
###############################################################################################

@app.route('/')
def header():
    return render_template('header.html')

@app.route('/health')
def health_check():
    """Endpoint crítico para que Render verifique que la app está viva"""
    return {
        'status': 'healthy', 
        'uptime': time.time() - app_start_time,
        'environment': 'Render' if IS_RENDER else 'Local'
    }, 200

@app.route('/bim-acueductos')
def bim_acueductos():
    return render_template('bim-acueductos.html')

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

@app.route('/bim-construccion')
def bim_construccion():
    return render_template('bim-construccion.html')

# Función para mantener la app activa en Render
def keep_alive():
    """Función para mantener la app activa en plan free de Render"""
    if IS_RENDER:
        while True:
            try:
                # Hacer una request a la propia app cada 5 minutos
                base_url = os.environ.get('RENDER_EXTERNAL_URL', '')
                if base_url:
                    requests.get(f"{base_url}/health", timeout=10)
                    logger.info("✅ Keep-alive check realizado")
                time.sleep(300)  # 5 minutos
            except Exception as e:
                logger.warning(f"⚠️ Keep-alive error: {e}")
                time.sleep(60)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    
    # Configuración específica para cada entorno
    if IS_RENDER:
        # MODO RENDER - Sin ngrok
        logger.info("🚀 Iniciando en modo RENDER")
        
        # Iniciar keep-alive
        keep_alive_thread = Thread(target=keep_alive)
        keep_alive_thread.daemon = True
        keep_alive_thread.start()
        logger.info("✅ Keep-alive iniciado")
        
    else:
        # MODO LOCAL - Con ngrok
        logger.info("🚀 Iniciando en modo LOCAL con ngrok")
        
        try:
            ngrok_tunnel = setup_ngrok_tunnel(port)
            if ngrok_tunnel:
                print("🌐 URL pública para celular:", ngrok_tunnel.public_url)
                print("📱 Usa esta URL en tu celular para probar")
                print("📍 URL local: http://127.0.0.1:5000")
            else:
                print("⚠️  No se pudo crear el túnel ngrok")
        except Exception as e:
            print(f"❌ Error con ngrok: {e}")
            print("🔧 Ejecutando solo en localhost")

    # Iniciar servidor Flask
    debug_mode = not IS_RENDER  # Debug solo en local
    app.run(host="0.0.0.0", port=port, debug=debug_mode)