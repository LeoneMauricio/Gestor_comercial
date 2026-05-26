import sqlite3

conexion = sqlite3.connect("soderia.db")

cursor = conexion.cursor()

# TABLA CLIENTES
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes(
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    direccion TEXT NOT NULL,
    celular TEXT NOT NULL
)
""")

# TABLA ENVASES
cursor.execute("""
CREATE TABLE IF NOT EXISTS envases(
    id_envase INTEGER PRIMARY KEY AUTOINCREMENT,
    envase TEXT NOT NULL,
    stock INTEGER NOT NULL,
    precio REAL NOT NULL
)
""")

# TABLA VENTAS
cursor.execute("""
CREATE TABLE IF NOT EXISTS ventas(
    id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    id_envase INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario REAL NOT NULL,
    subtotal REAL NOT NULL,
    fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY(id_envase) REFERENCES envases(id_envase)
)
""")

# ENVASES PRESTADOS
cursor.execute("""
CREATE TABLE IF NOT EXISTS prestamos_envases(
    id_prestamo INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    id_envase INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    fecha_prestamo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(id_cliente)
    REFERENCES clientes(id_cliente),
    FOREIGN KEY(id_envase)
    REFERENCES envases(id_envase)
)
""")

conexion.commit()
conexion.close()

print("Base de datos creada correctamente")