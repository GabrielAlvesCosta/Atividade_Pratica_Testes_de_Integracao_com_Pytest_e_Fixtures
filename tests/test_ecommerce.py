import sqlite3, pytest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "produtos.sqlite"
LOGS_BD_FILE = BASE_DIR / "logs.sqlite"

@pytest.fixture(scope='function')
def db_produtos():
    if DB_FILE.exists():
        DB_FILE.unlink()
    conn = sqlite3.connect(str(DB_FILE))
    conn.execute('''
                 CREATE TABLE produtos (
                 id INTEGER PRIMARY KEY,
                 nome TEXT NOT NULL,
                 preco REAL NOT NULL
                 )
                 ''')
    conn.commit()
    
    yield conn

    conn.close()

def test_banco_produtos_vazio(db_produtos):
    cursor = db_produtos.cursor()
    cursor.execute('SELECT COUNT(*) FROM produtos')
    total = cursor.fetchone()[0]
    
    
    assert total == 0

def test_inserir_produto(db_produtos):
    cursor = db_produtos.cursor()
    cursor.execute(
        'INSERT INTO produtos (nome, preco) VALUES (?, ?)',
          ('Produto A', 10.0)
    )
    db_produtos.commit()

    cursor.execute('SELECT nome FROM produtos WHERE preco = ?', ('10.0',))
    row = cursor.fetchone()

    assert row[0] == 'Produto A'


@pytest.fixture(scope='session')
def db_session():
    if LOGS_BD_FILE.exists():
        LOGS_BD_FILE.unlink()
    conn = sqlite3.connect(str(LOGS_BD_FILE))
    conn.execute('CREATE TABLE auditoria (id INTEGER PRIMARY KEY, evento TEXT)')
    conn.commit()
    
    yield conn

    conn.close()

def test_registrar_log(db_session):
    db_session.execute('INSERT INTO auditoria (evento) VALUES (?)', ('Primeiro Trimestre 2026',))
    db_session.commit()

    row = db_session.execute("SELECT evento FROM auditoria WHERE id = '1'").fetchone()
    assert row[0] == 'Primeiro Trimestre 2026'

def test_contar_logs(db_session):
    count = db_session.execute('SELECT COUNT(*) FROM auditoria').fetchone()[0]
    
    assert count >= 1