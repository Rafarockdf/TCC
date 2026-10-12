import time
import pandas as pd
import requests
import argparse
from pathlib import Path

import pandas as pd
import yfinance as yf

TICKER = "ZS=F"  # Soybean Futures - Chicago Board of Trade (CBOT)
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
SAIDA_CSV = RAIZ_PROJETO / "Dados" / "brutos" / "cotacoes" / "preco_petroleo.csv"


def salvar_csv(df: pd.DataFrame, caminho: Path) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(caminho, index=False)
    print(f"{len(df)} registros salvos em {caminho}")

def coleta_precos_petroleo():
    API_KEY = "GpbOcZj3IE7FV7yGvorcExIMf2YpJ1rqbODXST3g"
    url = "https://api.eia.gov/v2/petroleum/pri/spt/data/"

    # Usando o código direto de série da EIA (RBRTE = Europe Brent Spot Price FOB)
    params = {
        "api_key": API_KEY,
        "frequency": "daily",
        "data[0]": "value",
        "facets[series][]": "RBRTE",
        "start": "2020-01-01",
        "end": "2026-08-01",
        "sort[0][column]": "period",
        "sort[0][direction]": "asc",
        "length": 5000,
    }

    headers = {"User-Agent": "Mozilla/5.0"}
    max_tentativas = 5
    espera = 3

    for tentativa in range(max_tentativas):
        try:
            print(
                f"Consultando API EIA (Tentativa {tentativa+1}/{max_tentativas})..."
            )
            # Timeout aumentado para 45s para evitar Read timed out
            response = requests.get(
                url, headers=headers, params=params, timeout=45
            )

            if response.status_code == 200:
                json_data = response.json()
                registros = json_data.get("response", {}).get("data", [])

                if not registros:
                    print("Resposta recebida, mas sem registros.")
                    return None

                df = pd.DataFrame(registros)
                salvar_csv(df, SAIDA_CSV)
                print(df.tail())
                df = df[["period", "value"]].rename(
                    columns={"period": "Data", "value": "Preco_Brent"}
                )
                df["Data"] = pd.to_datetime(df["Data"])
                df["Preco_Brent"] = pd.to_numeric(
                    df["Preco_Brent"], errors="coerce"
                )

                print("✓ Dados carregados com sucesso!")
                print(df.tail())
                
                return df

            elif response.status_code in [500, 502, 503, 504]:
                print(
                    f"Instabilidade no servidor ({response.status_code}). Aguardando {espera}s..."
                )
                time.sleep(espera)
                espera *= 2
            else:
                print(f"Erro {response.status_code}: {response.text}")
                break

        except (
            requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectTimeout,
        ):
            print(
                f"Tempo limite esgotado (Timeout). Tentando novamente em {espera}s..."
            )
            time.sleep(espera)
            espera *= 2
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão: {e}. Aguardando {espera}s...")
            time.sleep(espera)
            espera *= 2
    
    return None


if __name__ == "__main__":
    coleta_precos_petroleo()