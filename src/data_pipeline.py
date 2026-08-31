"""Pipeline de transformación de datos de microdatos a resultados para Power BI."""

import pandas as pd
from src.fuzzy_engine import asignar_categoria, evaluar_motor_difuso


def procesar_pipeline(
    ruta_entrada: str, ruta_salida: str
) -> pd.DataFrame:
    print(f"Cargando dataset desde: {ruta_entrada}")
    try:
        df = pd.read_csv(ruta_entrada)
    except UnicodeDecodeError:
        df = pd.read_csv(ruta_entrada, encoding="latin-1", sep=";")
        
    print("Calculando antecedentes por fila...")
    df["Carga_Incidencia"] = df["N° DE CASOS - MUJERES"]

    casos_pareja = (
        df["N° CASOS - VINCULO RELACIONAL - PAREJA"]
        + df["N° CASO - VINCULO RELACIONAL - EX PAREJA"]
    )
    df["Riesgo_Relacional"] = (casos_pareja / df["N° DE CASOS - MUJERES"]) * 100

    casos_vulnerables = (
        df["N° CASOS DE TENTATIVA FEMINICIDIO - 0_5 - MUJERES"]
        + df["N° CASOS DE TENTATIVA FEMINICIDIO - 6_11 - MUJERES"]
        + df["N° CASOS DE TENTATIVA FEMINICIDIO - 12_17 - MUJERES"]
        + df["N° CASOS DE TENTATIVA FEMINICIDIO - 60_MÁS - MUJERES"]
    )
    df["Vulnerabilidad_Etaria"] = (
        casos_vulnerables / df["N° DE CASOS - MUJERES"]
    ) * 100

    df["Riesgo_Relacional"] = df["Riesgo_Relacional"].fillna(0.0)
    df["Vulnerabilidad_Etaria"] = df["Vulnerabilidad_Etaria"].fillna(0.0)

    print("Aplicando Inferencia Difusa...")
    scores = []
    categorias = []

    for _, row in df.iterrows():
        score = evaluar_motor_difuso(
            carga=row["Carga_Incidencia"],
            riesgo=row["Riesgo_Relacional"],
            vuln=row["Vulnerabilidad_Etaria"],
        )
        scores.append(score)
        categorias.append(asignar_categoria(score))

    df["SCORE_PRIORIDAD_DIFUSA"] = scores
    df["CATEGORIA_RIESGO"] = categorias

    print(f"Exportando archivo consolidado a: {ruta_salida}")
    df.to_excel(ruta_salida, index=False)
    return df