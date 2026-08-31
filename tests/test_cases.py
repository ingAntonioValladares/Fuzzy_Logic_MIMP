"""Pruebas unitarias para validar los casos de prueba de la documentación."""

from src.fuzzy_engine import asignar_categoria, evaluar_motor_difuso


def test_caso_a_alta_prioridad():
    score = evaluar_motor_difuso(carga=80, riesgo=85, vuln=70)
    cat = asignar_categoria(score)
    assert cat == "Crítica"


def test_caso_b_prioridad_por_riesgo_relacional():
    score = evaluar_motor_difuso(carga=35, riesgo=90, vuln=40)
    cat = asignar_categoria(score)
    assert cat == "Crítica"


def test_caso_c_baja_prioridad():
    score = evaluar_motor_difuso(carga=10, riesgo=15, vuln=10)
    cat = asignar_categoria(score)
    assert cat == "Baja"