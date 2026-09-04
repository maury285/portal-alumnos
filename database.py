import sqlite3

# 1. Creamos la conexión (esto genera el archivo de la base de datos)
conexion = sqlite3.connect('escuela.db')
cursor = conexion.cursor()

# 2. Creamos la "planilla" donde guardaremos los datos
cursor.execute('''
CREATE TABLE IF NOT EXISTS alumnos (
    dni TEXT PRIMARY KEY,
    password TEXT,
    nombre TEXT,
    faltas INTEGER,
    notas_cuatrimestre TEXT
)
''')

# 3. Borramos los datos viejos por si ejecutamos este archivo más de una vez
cursor.execute('DELETE FROM alumnos')

# 4. Insertamos dos alumnos de prueba simulando tu lista de asistencia
cursor.execute('''
INSERT INTO alumnos (dni, password, nombre, faltas, notas_cuatrimestre)
VALUES ('12345678', 'clave123', 'Juan Pérez', 3, 'Matemática: 8, Lengua: 7, Historia: 9')
''')

cursor.execute('''
INSERT INTO alumnos (dni, password, nombre, faltas, notas_cuatrimestre)
VALUES ('87654321', 'clave456', 'María Gómez', 0, 'Matemática: 9, Lengua: 10, Historia: 8')
''')

# 5. Guardamos los cambios y cerramos la conexión
conexion.commit()
conexion.close()

print("¡Base de datos creada y alumnos de prueba cargados con éxito!")