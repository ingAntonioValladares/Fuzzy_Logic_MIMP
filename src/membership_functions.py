"""Módulo de Funciones de Pertenencia construidas desde cero (from scratch)."""


def trimf(x: float, a: float, b: float, c: float) -> float:
    """Función de pertenencia Triangular."""
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return 1.0 if a == b else (x - a) / (b - a)
    elif b < x < c:
        return (c - x) / (c - b)
    return 0.0


def trapmf(
    x: float, a: float, b: float, c: float, d: float
) -> float:
    """Función de pertenencia Trapezoidal."""
    if x <= a or x >= d:
        return 0.0
    elif a < x < b:
        return (x - a) / (b - a)
    elif b <= x <= c:
        return 1.0
    elif c < x < d:
        return (d - x) / (d - c)
    return 0.0