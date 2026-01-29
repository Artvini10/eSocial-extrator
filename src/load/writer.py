import pandas as pd

def escrever(df, tema, pasta):
    atual = df[df["isAtual"]]
    hist = df

    atual.to_excel(f"{pasta}/{tema}_ATUAL.xlsx", index=False)
    hist.to_excel(f"{pasta}/{tema}_HISTORICO.xlsx", index=False)