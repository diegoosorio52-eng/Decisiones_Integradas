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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

