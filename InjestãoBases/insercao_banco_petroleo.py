import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ColetaBases.coleta_pretroleo import coleta_precos_petroleo
import sqlite3

def insere_sqlite():

    dados_petroleo = coleta_precos_petroleo()
    if dados_petroleo is None:
        print("Coleta falhou, nada para inserir.")
        return

    conn = sqlite3.connect("Data/banco.db")
    try:
        # 3. Inserir o DataFrame no banco de dados
        dados_petroleo.to_sql(
            name="Historico_Precificao_Petroleo",  # Nome da tabela que será criada ou usada
            con=conn,  # Sua conexão com o SQLite
            if_exists="append",  # O que fazer se a tabela já existir: 'fail', 'replace' ou 'append'
            index=False,  # Não salva o índice do DataFrame como uma coluna do banco
        )
        print("DataFrame inserido com sucesso!")
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
    finally:
        # 4. Fechar a conexão
        conn.close()


if __name__ == "__main__":
    insere_sqlite()