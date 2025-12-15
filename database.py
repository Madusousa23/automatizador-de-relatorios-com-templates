import sqlite3

def conectar():
    return sqlite3.connect("relatorios.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS templates_relatorios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            template TEXT
        )
    """)

    conn.commit()
    conn.close()

def inserir_templates():
    conn = conectar()
    cursor = conn.cursor()

    templates = [
        (
            "Relatório de Incidente",
            """RELATÓRIO DE INCIDENTE

Data: {data}
Responsável: {responsavel}
Setor: {setor}

Descrição do incidente:
{descricao}

Ação tomada:
{acao}

Status: {status}
"""
        ),
        (
            "Relatório de Atendimento",
            """RELATÓRIO DE ATENDIMENTO

Data: {data}
Cliente: {cliente}
Atendente: {atendente}

Descrição do atendimento:
{descricao}

Resultado:
{resultado}
"""
        )
    ]

    cursor.executemany("""
        INSERT INTO templates_relatorios (nome, template)
        VALUES (?, ?)
    """, templates)

    conn.commit()
    conn.close()
