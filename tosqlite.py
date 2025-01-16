import sqlite3
import json

# Cargar el archivo JSON
with open('output.json', 'r') as file:
    data = json.load(file)

# Conectar a SQLite
conn = sqlite3.connect('diagnostics.db')
cursor = conn.cursor()

# Crear la tabla
cursor.execute('''
CREATE TABLE IF NOT EXISTS diagnostics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    symptoms TEXT,
    cause TEXT,
    control TEXT,
    reference TEXT
);
''')

# Insertar datos
for item in data:
    cursor.execute('''
    INSERT INTO diagnostics (name, symptoms, cause, control, reference)
    VALUES (?, ?, ?, ?, ?)
    ''', (
        item['name'],
        item.get('symptoms', ''),
        item.get('cause', ''),
        item.get('control', ''),
        json.dumps(item.get('reference', []))  # Guardar las referencias como JSON
    ))

# Guardar y cerrar
conn.commit()
conn.close()

print("Base de datos creada exitosamente.")
