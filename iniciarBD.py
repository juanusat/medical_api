import MySQLdb as dbc
import MySQLdb.cursors
from get_env import _get_required_env
import os

def ejecutar_setup():
    local_dir = os.path.dirname(os.path.abspath(__file__))
    password = os.getenv('DB_PASSWORD', '')
    
    db = dbc.connect(
        host=_get_required_env('DB_HOST'),
        user=_get_required_env('DB_USER'),
        passwd=password,
        port=int(_get_required_env('DB_PORT')),
        cursorclass=dbc.cursors.DictCursor
    )
    cursor = db.cursor()

    prefijo = _get_required_env('ENVUSERPRE')
    ruta_sql = os.path.join(local_dir, 'setup', 'database.sql')
    
    if not os.path.isfile(ruta_sql):
        ruta_sql = os.path.join(local_dir, 'setup', 'database_base.sql')

    with open(ruta_sql, 'r', encoding='utf-8') as archivo:
        contenido_sql = archivo.read()

    sql_modificado = contenido_sql.replace('PREFIX_', prefijo + '_')
    sentencias = sql_modificado.split(';')

    for sentencia in sentencias:
        sentencia_limpia = sentencia.strip()
        if sentencia_limpia:
            cursor.execute(sentencia_limpia)

    db.commit()
    cursor.close()
    db.close()

if __name__ == '__main__':
    ejecutar_setup()