import psycopg2

class DBManager:

    def __init__(self, host: str, dbname: str, user: str, password: str, port: int = 5432):
        self.host     = host
        self.dbname   = dbname
        self.user     = user
        self.password = password
        self.port     = port
        self.conn     = None
        self.cursor   = None

    def conectar(self) -> None:
        self.conn = psycopg2.connect(
            host     = self.host,
            dbname   = self.dbname,
            user     = self.user,
            password = self.password,
            port     = self.port
        )
        self.cursor = self.conn.cursor()
        print("[OK] Conectado a PostgreSQL")
    def crear_tabla(self) -> None:
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS resultados (
                id      TEXT PRIMARY KEY,
                modulo  TEXT NOT NULL,
                estado  TEXT NOT NULL,
                tiempo  NUMERIC(10, 2) NOT NULL
            )
        """)
        self.conn.commit()
        print("[OK] Tabla creada")

    def insertar_resultados(self, resultados: list) -> None:
        for resultado in resultados:
            self.cursor.execute("""
                INSERT INTO resultados (id, modulo, estado, tiempo)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (resultado["id"], resultado["modulo"], resultado["estado"], resultado["tiempo"]))
        self.conn.commit()
        print(f"[OK] {len(resultados)} registros insertados")
        
    def obtener_fallos(self) -> list:
        self.cursor.execute("""
            SELECT id, modulo, estado, tiempo 
            FROM resultados 
            WHERE estado = 'FAILED'
        """)
        filas = self.cursor.fetchall()
        return [
            {"id": f[0], "modulo": f[1], "estado": f[2], "tiempo": float(f[3])}
            for f in filas
        ]
    
    def obtener_resumen(self) -> dict:
        self.cursor.execute("""
            SELECT estado, COUNT(*) FROM resultados GROUP BY estado
        """)
        return dict(self.cursor.fetchall())
    
    def obtener_lentos(self, tiempo_max: float = 2.0) -> list:
        self.cursor.execute("""
            SELECT id, modulo, estado, tiempo 
            FROM resultados 
            WHERE tiempo > %s
            ORDER BY tiempo DESC
        """, (tiempo_max,))
        filas = self.cursor.fetchall()
        return [
            {"id": f[0], "modulo": f[1], "estado": f[2], "tiempo": float(f[3])}
            for f in filas
        ]

    def cerrar(self) -> None:
        if self.conn:
            self.conn.close()
            print("[OK] Conexión cerrada")