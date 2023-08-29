import pymysql

def conexion():
    return pymysql.connect(
        host='localhost',
        user= 'root',
        password= '1234',
        db= 'basedatos_flask'
    )
    
def alta_usuario(email, clave):
    conn = conexion()
    with conn.cursor() as cursor:
        cursor.execute(
            f"INSERT INTO usuarios (email, clave) VALUES ('{email}','{clave}')"
        )
        conn.commit()
    conn.close()

def get_usuario(email):
    conn = conexion()
    usuario = None
    with conn.cursor() as cursor:
        cursor.execute(
            f"SELECT * FROM usuarios WHERE email = '{email}'"
        )
        usuario = cursor.fetchone()
        conn.close()
        return usuario

