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

# GANANCIAS POR DÍA
cursor.execute("""
    CREATE VIEW IF NOT EXISTS ganancias_diarias AS
    SELECT
        fecha,
        COALESCE(total_ventas, 0) AS total_ventas,
        COALESCE(total_gastos, 0) AS total_gastos,
        COALESCE(total_ventas, 0) - COALESCE(total_gastos, 0) AS ganancia_neta
    FROM (
        SELECT DATE(fecha_venta) AS fecha, SUM(subtotal) AS total_ventas
        FROM ventas
        GROUP BY DATE(fecha_venta)
    ) v
    LEFT JOIN (
        SELECT DATE(fecha_del_gasto) AS fecha, SUM(monto) AS total_gastos
        FROM gastos
        GROUP BY DATE(fecha_del_gasto)
    ) g USING(fecha)
    """)

    # GANANCIAS POR MES
cursor.execute("""
    CREATE VIEW IF NOT EXISTS ganancias_mensuales AS
    SELECT
        mes,
        COALESCE(total_ventas, 0) AS total_ventas,
        COALESCE(total_gastos, 0) AS total_gastos,
        COALESCE(total_ventas, 0) - COALESCE(total_gastos, 0) AS ganancia_neta
    FROM (
        SELECT strftime('%Y-%m', fecha_venta) AS mes, SUM(subtotal) AS total_ventas
        FROM ventas
        GROUP BY strftime('%Y-%m', fecha_venta)
    ) v
    LEFT JOIN (
        SELECT strftime('%Y-%m', fecha_del_gasto) AS mes, SUM(monto) AS total_gastos
        FROM gastos
        GROUP BY strftime('%Y-%m', fecha_del_gasto)
    ) g USING(mes)
    """)

# GANANCIAS POR AÑO
cursor.execute("""
    CREATE VIEW IF NOT EXISTS ganancias_anuales AS
    SELECT
        anio,
        COALESCE(total_ventas, 0) AS total_ventas,
        COALESCE(total_gastos, 0) AS total_gastos,
        COALESCE(total_ventas, 0) - COALESCE(total_gastos, 0) AS ganancia_neta
    FROM (
        SELECT strftime('%Y', fecha_venta) AS anio, SUM(subtotal) AS total_ventas
        FROM ventas
        GROUP BY strftime('%Y', fecha_venta)
    ) v
    LEFT JOIN (
        SELECT strftime('%Y', fecha_del_gasto) AS anio, SUM(monto) AS total_gastos
        FROM gastos
        GROUP BY strftime('%Y', fecha_del_gasto)
    ) g USING(anio)
    """)

conexion.commit()
conexion.close()
