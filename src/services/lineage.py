def aplicar_historico(df):
    df = df.sort_values(["dtRecepcao", "nrRecibo"])
    df["versao"] = df.groupby("idEvento").cumcount() + 1
    df["isAtual"] = df.groupby("idEvento")["versao"].transform("max") == df["versao"]
    return df