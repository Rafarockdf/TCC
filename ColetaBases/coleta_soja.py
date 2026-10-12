"""
Coleta o histórico de cotações de soja (contrato futuro CBOT, ticker ZS=F)
via yfinance e salva o resultado em Dados/brutos/cotacoes/.

Uso:
    python coleta_soja.py
    python coleta_soja.py --inicio 2015-01-01 --fim 2026-08-15
"""

import argparse
from pathlib import Path

import pandas as pd
import yfinance as yf

TICKER = "ZS=F"  # Soybean Futures - Chicago Board of Trade (CBOT)
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
SAIDA_CSV = RAIZ_PROJETO / "Dados" / "brutos" / "cotacoes" / "soja_cbot.csv"


def coletar_soja(data_inicio: str | None = None, data_fim: str | None = None) -> pd.DataFrame:
    """Baixa o histórico diário do contrato futuro de soja (ZS=F)."""
    ticker = yf.Ticker(TICKER)
    df = ticker.history(start=data_inicio, end=data_fim, auto_adjust=False)

    if df.empty:
        raise RuntimeError(f"Nenhum dado retornado para o ticker {TICKER}.")

    df = df.rename_axis("Data").reset_index()
    df["Data"] = pd.to_datetime(df["Data"]).dt.tz_localize(None)
    df = df[["Data", "Open", "High", "Low", "Close", "Volume"]]
    df.columns = ["data", "abertura", "maxima", "minima", "fechamento", "volume"]

    return df


def salvar_csv(df: pd.DataFrame, caminho: Path) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(caminho, index=False)
    print(f"{len(df)} registros salvos em {caminho}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Coleta cotações de soja via yfinance")
    parser.add_argument("--inicio", default=None, help="Data inicial (AAAA-MM-DD)")
    parser.add_argument("--fim", default=None, help="Data final (AAAA-MM-DD)")
    args = parser.parse_args()

    df = coletar_soja(args.inicio, args.fim)
    salvar_csv(df, SAIDA_CSV)


if __name__ == "__main__":
    main()
