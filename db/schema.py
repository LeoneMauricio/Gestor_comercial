import sqlite3

conexion = sqlite3.connect("soderia.db")

cursor = conexion.cursor()

# TABLA CLIENTES
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes(
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT,
    direccion TEXT,
    coordenadas TEXT,
    celular TEXT NOT NULL UNIQUE
)
""")

# TABLA ENVASES
cursor.execute("""
CREATE TABLE IF NOT EXISTS envases(
    id_envase INTEGER PRIMARY KEY AUTOINCREMENT,
    envase TEXT NOT NULL UNIQUE,
    stock INTEGER,
    precio REAL
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
    fecha_venta DATETIME DEFAULT (datetime('now', 'localtime')),
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
    fecha_prestamo DATETIME DEFAULT (datetime('now', 'localtime')),
    UNIQUE(id_cliente, id_envase),
    FOREIGN KEY(id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY(id_envase) REFERENCES envases(id_envase)
)
""")

# GASTOS 
cursor.execute("""
CREATE TABLE IF NOT EXISTS gastos(
    id_gasto INTEGER PRIMARY KEY AUTOINCREMENT,
    motivo TEXT,
    monto REAL,
    fecha_del_gasto DATETIME DEFAULT (datetime('now', 'localtime'))
)
""")

# GANANCIAS VER SI ES NECESARIA
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS ganancias(
#     id_ganancia INTEGER PRIMARY KEY AUTOINCREMENT,
#     gasto REAL,
#     venta REAL,
#     ganancia REAL,
#     fecha_del_gasto DATETIME DEFAULT (datetime('now', 'localtime'))
# )
# """)


conexion.commit()
conexion.close()
