import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from google import genai
from dotenv import load_dotenv

# 1. Cargar configuraciones
load_dotenv()

# 2. Configurar la aplicación web
app = Flask(__name__)
app.secret_key = 'una_clave_muy_secreta_para_seguridad'

# Inicializar el cliente de Gemini con la nueva librería
cliente_gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_db_connection():
    conn = sqlite3.connect('escuela.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        dni = request.form['dni']
        password = request.form['password']
        
        conn = get_db_connection()
        alumno = conn.execute('SELECT * FROM alumnos WHERE dni = ? AND password = ?', (dni, password)).fetchone()
        conn.close()
        
        if alumno:
            session['alumno_dni'] = alumno['dni']
            return redirect(url_for('dashboard'))
        else:
            flash('DNI o contraseña incorrectos. Revise e intente nuevamente.')
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'alumno_dni' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    alumno = conn.execute('SELECT * FROM alumnos WHERE dni = ?', (session['alumno_dni'],)).fetchone()
    conn.close()
    
    # 🤖 ACÁ ACTUALIZAMOS GEMINI AL NUEVO MODELO 🤖
    prompt = f"""
    Actúa como un profesor comunicándose con el tutor de un alumno. 
    Redacta un breve reporte académico en un tono cordial, respetuoso y alentador.
    Datos del alumno:
    - Nombre: {alumno['nombre']}
    - Inasistencias este cuatrimestre: {alumno['faltas']}
    - Notas del primer cuatrimestre: {alumno['notas_cuatrimestre']}
    
    El reporte debe estar dirigido al tutor, mencionar las notas y las faltas de forma amena, y dar un breve cierre motivador. 
    Dirígete de usted al tutor. Escribe solo el cuerpo del mensaje, sin asuntos ni saludos genéricos.
    """
    
    # Nueva forma de pedirle el texto a Gemini
    respuesta = cliente_gemini.models.generate_content(
        model='gemini-3.5-flash',
        contents=prompt
    )
    resumen_generado = respuesta.text
    
    return render_template('dashboard.html', alumno=alumno, resumen=resumen_generado)

@app.route('/logout')
def logout():
    session.pop('alumno_dni', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)