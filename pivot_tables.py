#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import pandas as pd
from rich.console import Console
from rich.theme import Theme

# ── 1. Cargar CSV ───────────────────────────────────────────────────────────────
path = sys.argv[1]                 # ruta al CSV pasada por CLI
df   = pd.read_csv(path)

# ── 1.1. Procesar formato decimal europeo (comas) ──────────────────────────────
# Convertir valores con comas decimales a puntos para evitar errores de multiplicación
for col in ['Min H', 'Max H']:
    if col in df.columns:
        # Convertir valores string con comas a puntos, luego a numeric
        df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Mostrar todas las filas sin truncar
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)      # NO limitar el ancho

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

#cost/2
# cost = {
#     "Desarrollo Frontend": 20,
#     "Diseño UI/UX":        20,
#     "CTO/Arquitectura":    25,
#     "Desarrollo Backend":  25,
#     "Prompting":           17.5,
#     "Testeo":              17.5,
#     "Reuniones":            0
# }

df["Min Cost"] = df["Min H"] * df["Type"].map(cost)
df["Max Cost"] = df["Max H"] * df["Type"].map(cost)

# Agrupaciones
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
    "Total Min H": [df["Min H"].sum()],
    "Total Max H": [df["Max H"].sum()],
    "Total Min Cost (€)": [df["Min Cost"].sum()],
    "Total Max Cost (€)": [df["Max Cost"].sum()]
})
show("Totales globales", total_df)

# ── 4. Guardar CSVs ────────────────────────────────────────────────────────────
# Carpeta donde está el CSV de entrada
input_folder   = "/".join(path.split("/")[:-1])
input_filename = path.split("/")[-1].split(".")[0]

# Rutas para feature y type: sin prefijo ‘task_’
feature_out = f"{input_folder}/{input_filename}_feature_df.csv"
tipo_out    = f"{input_folder}/{input_filename}_type_df.csv"

# Rutas para full: con prefijo ‘task_’ y dos ubicaciones
root_folder     = "/".join(path.split("/")[:-2])           # carpeta padre del proyecto
content_folder  = f"{root_folder}/content"                 # carpeta ‘content’ dinámica
os.makedirs(content_folder, exist_ok=True)                 # crearla si no existe

full_basename          = f"task_{input_filename}_full_df.csv"
full_out_estimations   = f"{input_folder}/{full_basename}"
full_out_content       = f"{content_folder}/{full_basename}"

# Escribir archivos
feature_df.reset_index().to_csv(feature_out, index=False)
tipo_df.reset_index().to_csv(tipo_out,    index=False)
df.to_csv(full_out_estimations, index=False)
df.to_csv(full_out_content,     index=False)
