from flask import Flask, render_template, request, redirect, url_for
import time
import os
import logging
from threading import Thread
import requests

# ----------------------------------------------------------
# CONFIGURACIÓN INICIAL
# ----------------------------------------------------------

app = Flask(__name__)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Health check
app_start_time = time.time()

# Detectar entorno
IS_RENDER = os.environ.get('RENDER') is not None
IS_LOCAL = not IS_RENDER

# ----------------------------------------------------------
# NGROK SOLO PARA ENTORNO LOCAL
# ----------------------------------------------------------

if IS_LOCAL:
    try:
        from pyngrok import ngrok, conf
        import subprocess
        import atexit

        def kill_ngrok_processes():
            """Termina procesos de ngrok (Windows principalmente)"""
            try:
                subprocess.run(['taskkill', '/f', '/im', 'ngrok.exe'],
                               capture_output=True, timeout=10)
                print("🔴 Procesos ngrok terminados")
            except:
                pass

            try:
                ngrok.kill()
            except:
                pass

            time.sleep(2)

        def setup_ngrok_tunnel(port=5000):
            """Configura túnel ngrok robusto"""
            kill_ngrok_processes()
            time.sleep(3)

            try:
                conf.get_default().monitor_thread = False
                tunnel = ngrok.connect(port, bind_tls=True)
                print("🌐 Túnel NGROK creado:")
                print("URL pública:", tunnel.public_url)
                return tunnel
            except Exception as e:
                print("❌ Error NGROK:", e)
                return None

        atexit.register(kill_ngrok_processes)

    except ImportError:
        print("⚠️ Ngrok no disponible (modo Render)")
        IS_LOCAL = False


# ----------------------------------------------------------
# RUTAS DEL SITIO WEB
# ----------------------------------------------------------

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/empresa")
def empresa():
    return render_template("empresa.html")

@app.route("/servicios")
def servicios():
    return render_template("servicios.html")

@app.route("/proyectos")
def proyectos():
    return render_template("proyectos.html")

@app.route('/health')
def health_check():
    """Render usa este endpoint para verificar que la app está activa."""
    return {
        "status": "healthy",
        "uptime": time.time() - app_start_time,
        "environment": "Render" if IS_RENDER else "Local"
    }, 200

@app.route('/bim-acueductos')
def bim_acueductos():
    return render_template('bim-acueductos.html')

@app.route("/ingenieria-acueductos")
def ingenieria_acueductos():
    return render_template("ingenieria-acueductos.html")

@app.route("/analitica")
def analitica():
    return render_template("analitica.html")

@app.route("/ambiental-riesgos")
def ambiental_riesgos():
    return render_template("ambiental-riesgos.html")

@app.route("/consultoria-proyectos")
def consultoria_proyectos():
    return render_template("consultoria-proyectos.html")

@app.route("/capacitacion")
def capacitacion():
    return render_template("capacitacion.html")

@app.route("/mantenimiento-pozos-profundos")
def mantenimiento_pozos():
    return render_template("mantenimiento-pozos-profundos.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# ----------------------------------------------------------
# FUNCIÓN KEEP-ALIVE PARA RENDER
# ----------------------------------------------------------

def keep_alive():
    """Evita que Render apague el servidor en plan Free."""
    if IS_RENDER:
        while True:
            try:
                base_url = os.environ.get("RENDER_EXTERNAL_URL", "")
                if base_url:
                    requests.get(f"{base_url}/health", timeout=10)
                    logger.info("💓 Keep-alive ejecutado correctamente.")
                time.sleep(300)
            except Exception as e:
                logger.warning(f"⚠️ Error en keep-alive: {e}")
                time.sleep(60)


# ----------------------------------------------------------
# EJECUCIÓN DEL SERVIDOR
# ----------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))

    if IS_RENDER:
        logger.info("🚀 Ejecutando en modo RENDER.")

        # Iniciar hilo de keep-alive
        keep_thread = Thread(target=keep_alive)
        keep_thread.daemon = True
        keep_thread.start()
        logger.info("🔁 Keep-alive iniciado.")

    else:
        logger.info("💻 Ejecutando localmente con NGROK.")

        try:
            tunnel = setup_ngrok_tunnel(port)
            if tunnel:
                print("📱 URL para pruebas externas:", tunnel.public_url)
            else:
                print("⚠️ Ngrok no disponible. Solo localhost.")
        except Exception as e:
            print("❌ Error ngrok:", e)

    # Ejecutar Flask
    app.run(host="0.0.0.0", port=port, debug=IS_LOCAL)
