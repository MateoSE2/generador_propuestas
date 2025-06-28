#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pandas as pd
from rich.console import Console
from rich.theme import Theme

# ── 1. Cargar CSV ───────────────────────────────────────────────────────────────
path = sys.argv[1]                 # ruta al CSV pasada por CLI
df   = pd.read_csv(path)

# Mostrar todas las filas sin truncar
pd.set_option('display.max_rows', None)
# ***Clave: no limitar el ancho de la representación en texto***
pd.set_option('display.width', None)      # o pd.set_option('display.width', 0)

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

df["Min Cost"] = df["Min H"] * df["Type"].map(cost)
df["Max Cost"] = df["Max H"] * df["Type"].map(cost)

# Agrupaciones (mantener)
feature_df = (
    df.groupby("Phase/Feature")
      .agg({"Min H": "sum", "Max H": "sum",
            "Min Cost": "sum",  "Max Cost": "sum"})
)
tipo_df = (
    df.groupby("Type")
      .agg({"Min H": "sum", "Max H": "sum",
            "Min Cost": "sum",  "Max Cost": "sum"})
)

# ── 3. Pretty-print con Rich ───────────────────────────────────────────────────
custom_theme = Theme({
    "rule":   "bold cyan",
    "header": "bold magenta"
})
# ***Clave: NO fijar width; Rich usa todo el ancho disponible***
console = Console(theme=custom_theme)

def show(title: str, data):
    """Imprime data (DataFrame o Series) bajo un separador bonito."""
    console.rule(f"[header]{title}")
    console.print(data)

show("CSV completo", df)
show("Agrupación por Feature", feature_df)
show("Agrupación por Tipo", tipo_df)

# Totales globales
total_df = pd.DataFrame({
    "Total Min Cost (€)": [df["Min Cost"].sum()],
    "Total Max Cost (€)": [df["Max Cost"].sum()]
})
show("Totales globales", total_df)

# ── 4. Guardar CSV manteniendo la clave de agrupación ──────────────────────────
feature_df_reset = feature_df.reset_index()
tipo_df_reset    = tipo_df.reset_index()

input_folder   = "/".join(path.split("/")[:-1])
input_filename = path.split("/")[-1].split(".")[0]

feature_out = f"{input_folder}/{input_filename}_feature_df.csv"
tipo_out    = f"{input_folder}/{input_filename}_type_df.csv"
full_out    = f"{input_folder}/{input_filename}_full_df.csv"

feature_df_reset.to_csv(feature_out, index=False)
tipo_df_reset.to_csv(tipo_out,    index=False)
df.to_csv(full_out,               index=False)
