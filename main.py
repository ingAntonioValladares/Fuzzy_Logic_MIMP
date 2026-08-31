"""Punto de entrada principal para ejecutar el pipeline completo."""

import os
from src.data_pipeline import procesar_pipeline


def main():
    entrada = os.path.join("data", "raw", "dataset_mimp.csv")
    salida = os.path.join("data", "processed", "dataset_procesado_difuso.xlsx")

    if not os.path.exists(entrada):
        print(f"Error: Asegúrate de colocar el archivo CSV en {entrada}")
        return

    procesar_pipeline(ruta_entrada=entrada, ruta_salida=salida)


if __name__ == "__main__":
    main()