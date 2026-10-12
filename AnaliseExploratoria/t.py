import sqlite3
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
# 1. Conectar ao banco de dados SQLite
conn = sqlite3.connect("Data/banco.db")

try:
    # 2. Definir a consulta SQL (pode usar WHERE, JOIN, GROUP BY, etc.)
    query = "SELECT Data, Preco_Brent FROM Historico_Precificao_Petroleo"
    
    # 3. Executar o SELECT e carregar direto no DataFrame
    # O argumento 'params' passa os valores de forma segura (evita SQL Injection)
    df = pd.read_sql_query(query, conn)
    
    # 4. Exibir o DataFrame resultante
    print("Dados carregados com sucesso:")
    print(df)

except Exception as e:
    print(f"Erro ao ler os dados: {e}")

finally:
    # 5. Fechar a conexão
    conn.close()
