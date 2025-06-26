#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pandas as pd
from rich.console import Console
from rich.theme import Theme

# ── 1. Cargar CSV ───────────────────────────────────────────────────────────────
path = sys.argv[1]                 # ruta al CSV pasada por CLI
df   = pd.read_csv(path)

# opcional: visualizar todas las filas sin truncar
pd.set_option('display.max_rows', None)

# ── 2. Calcular costes ─────────────────────────────────────────────────────────
cost = {
    "Desarrollo Frontend": 40,
    "Diseño UI/UX":        40,
    "CTO/Arquitectura":    50,
    "Desarrollo Backend":  50,
    "Prompting":           35,
    "Testeo":              35,
    "Reuniones":            0
}

df["Min Cost"] = df["Est. mín (h)"] * df["Tipo"].map(cost)
df["Max Cost"] = df["Est. máx (h)"] * df["Tipo"].map(cost)

# agrupaciones
feature_df = (
    df.groupby("Feature")
      .agg({"Est. mín (h)": "sum", "Est. máx (h)": "sum",
            "Min Cost": "sum",  "Max Cost": "sum"})
)

tipo_df = (
    df.groupby("Tipo")
      .agg({"Est. mín (h)": "sum", "Est. máx (h)": "sum",
            "Min Cost": "sum",  "Max Cost": "sum"})
)

# ── 3. Pretty-print con Rich ───────────────────────────────────────────────────
custom_theme = Theme({
    "rule": "bold cyan",
    "header": "bold magenta"
})
console = Console(theme=custom_theme, width=120)

def show(title: str, data):
    """Imprime data (DataFrame o Series) bajo un separador bonito."""
    console.rule(f"[header]{title}")
    console.print(data)

show("CSV completo", df)
show("Agrupación por Feature", feature_df)
show("Agrupación por Tipo", tipo_df)

# totales globales
total_df = pd.DataFrame({
    "Total Min Cost (€)": [df["Min Cost"].sum()],
    "Total Max Cost (€)": [df["Max Cost"].sum()]
})
show("Totales globales", total_df)
