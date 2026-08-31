"""Motor de Inferencia Difusa Mamdani y Defusificación por Centroide."""

import numpy as np
from src.membership_functions import trapmf, trimf


def fuzzificar_carga(x: float) -> dict:
    val = max(0.0, min(100.0, float(x)))
    return {
        "Baja": trapmf(val, -10, 0, 15, 35),
        "Media": trimf(val, 20, 45, 70),
        "Alta": trapmf(val, 55, 75, 100, 110),
    }


def fuzzificar_riesgo(x: float) -> dict:
    val = max(0.0, min(100.0, float(x)))
    return {
        "Bajo": trapmf(val, -10, 0, 20, 40),
        "Medio": trimf(val, 25, 50, 75),
        "Alto": trapmf(val, 60, 80, 100, 110),
    }


def fuzzificar_vulnerabilidad(x: float) -> dict:
    val = max(0.0, min(100.0, float(x)))
    return {
        "Baja": trapmf(val, -10, 0, 20, 40),
        "Media": trimf(val, 25, 50, 75),
        "Alta": trapmf(val, 60, 80, 100, 110),
    }


# Matriz Completa de 27 Reglas Difusas
MATRIZ_REGLAS = [
    # Bloque 1: Carga_Incidencia ES Baja
    ("Baja", "Bajo", "Baja", "Baja"),
    ("Baja", "Bajo", "Media", "Baja"),
    ("Baja", "Bajo", "Alta", "Media"),
    ("Baja", "Medio", "Baja", "Baja"),
    ("Baja", "Medio", "Media", "Media"),
    ("Baja", "Medio", "Alta", "Media"),
    ("Baja", "Alto", "Baja", "Media"),
    ("Baja", "Alto", "Media", "Critica"),
    ("Baja", "Alto", "Alta", "Critica"),
    # Bloque 2: Carga_Incidencia ES Media
    ("Media", "Bajo", "Baja", "Baja"),
    ("Media", "Bajo", "Media", "Media"),
    ("Media", "Bajo", "Alta", "Media"),
    ("Media", "Medio", "Baja", "Media"),
    ("Media", "Medio", "Media", "Media"),
    ("Media", "Medio", "Alta", "Critica"),
    ("Media", "Alto", "Baja", "Critica"),
    ("Media", "Alto", "Media", "Critica"),
    ("Media", "Alto", "Alta", "Critica"),
    # Bloque 3: Carga_Incidencia ES Alta
    ("Alta", "Bajo", "Baja", "Media"),
    ("Alta", "Bajo", "Media", "Media"),
    ("Alta", "Bajo", "Alta", "Critica"),
    ("Alta", "Medio", "Baja", "Media"),
    ("Alta", "Medio", "Media", "Critica"),
    ("Alta", "Medio", "Alta", "Critica"),
    ("Alta", "Alto", "Baja", "Critica"),
    ("Alta", "Alto", "Media", "Critica"),
    ("Alta", "Alto", "Alta", "Critica"),
]


def evaluar_motor_difuso(carga: float, riesgo: float, vuln: float) -> float:
    """Evalúa las reglas y calcula el centroide continuo."""
    f_c = fuzzificar_carga(carga)
    f_r = fuzzificar_riesgo(riesgo)
    f_v = fuzzificar_vulnerabilidad(vuln)

    pesos_salida = {"Baja": 0.0, "Media": 0.0, "Critica": 0.0}

    for c_tag, r_tag, v_tag, consecuente in MATRIZ_REGLAS:
        fuerza = min(f_c[c_tag], f_r[r_tag], f_v[v_tag])
        pesos_salida[consecuente] = max(pesos_salida[consecuente], fuerza)

    x_grid = np.linspace(0, 100, 500)
    mu_agregada = np.zeros_like(x_grid)

    for i, x in enumerate(x_grid):
        mu_baja = min(pesos_salida["Baja"], trapmf(x, -10, 0, 20, 40))
        mu_media = min(pesos_salida["Media"], trimf(x, 25, 50, 75))
        mu_critica = min(pesos_salida["Critica"], trapmf(x, 60, 80, 100, 110))
        mu_agregada[i] = max(mu_baja, mu_media, mu_critica)

    suma_mu = np.sum(mu_agregada)
    if suma_mu == 0:
        return 0.0

    centroide = np.sum(x_grid * mu_agregada) / suma_mu
    return round(float(centroide), 2)


def asignar_categoria(score: float) -> str:
    """Clasifica el score continuo en una categoría de riesgo."""
    if score < 35.0:
        return "Baja"
    elif score < 65.0:
        return "Media"
    return "Crítica"