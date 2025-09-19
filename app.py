from flask import Flask, render_template
import pandas as pd
from flask import Flask, render_template, request, redirect  # Importa la función 'redirect'
import subprocess
import csv
import numpy as np
import pickle
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


app = Flask(__name__)


###############################################################################################
######################################## PROYECTO  #########################################
###############################################################################################


@app.route('/')
def header():
    # Renderizar el encabezado y la introducción
    with open('templates/header.html', 'r', encoding='utf-8-sig') as header_file:
        header_html = header_file.read()

    return render_template('header.html', header=header_html)


######################################## CAPITULO 1  #########################################

@app.route('/capitulo1')
def capitulo1():
    return render_template('capitulo1.html')

@app.route('/analitica-datos')
def analitica_datos():
    return render_template('analitica_datos.html')

@app.route('/predicciones')
def predicciones():
    return render_template('predicciones.html')

@app.route('/modelos')
def modelos():
    return render_template('modelos.html')

@app.route('/alertas')
def alertas():
    return render_template('alertas.html')

@app.route('/reportes')
def reportes():
    return render_template('reportes.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

