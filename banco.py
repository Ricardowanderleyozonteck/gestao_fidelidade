import sqlite3

def conectar():
    conn = sqlite3.connect("dados.db", check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ciclos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        ciclo INTEGER,
        valor REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS arquivos_processados (
        nome_arquivo TEXT PRIMARY KEY
    )
    """)

    conn.commit()
    return conn