# Sistema Difuso de Priorización MIMP

Un sistema basado en **Lógica Difusa Mamdani** desarrollado en Python para calcular el nivel de prioridad de intervención frente a la violencia contra la mujer en el Perú. El modelo toma microdatos agregados del MIMP, calcula variables antecedentes (carga, riesgo relacional y vulnerabilidad etaria), aplica una matriz exhaustiva de 27 reglas difusas y defusifica mediante el método del centroide para generar un scoring continuo (0 - 100) y categorías de riesgo listas para consumir en **Power BI**.

---

## 📂 Estructura del Proyecto

```text
SistemaDifuso_MIMP/
│
├── data/
│   ├── raw/
│   │   └── dataset_mimp.csv              # Microdatos de entrada descargados del MIMP
│   └── processed/
│       └── dataset_procesado_difuso.xlsx # Dataset procesado listo para Power BI
│
├── src/
│   ├── __init__.py                       # Módulo del paquete src
│   ├── membership_functions.py           # Funciones de pertenencia (Trimf y Trapmf from scratch)
│   ├── fuzzy_engine.py                   # Fuzzificación, matriz de 27 reglas y defusificación por Centroide
│   └── data_pipeline.py                  # Carga, transformación de antecedente por fila y exportación
│
├── tests/
│   ├── __init__.py
│   └── test_cases.py                     # Pruebas unitarias de los casos de estudio (pytest)
│
├── notebooks/
│   └── exploracion_y_validacion.ipynb    # Notebook interactivo para pruebas y validación visual
│
├── main.py                               # Script principal de ejecución
├── requirements.txt                      # Dependencias de Python
└── README.md                             # Documentación del proyecto
```

## Requisitos Previos e Instalación

1. Clonar el repositorio y entrar a la carpeta del proyecto
   git clone <URL_DEL_REPOSITORIO>
   cd SistemaDifuso_MIMP

2. Instalar dependencias
   Se requiere Python 3.10+. Ejecuta el siguiente comando para instalar las librerías necesarias (pandas, numpy, openpyxl, pytest):
   pip install -r requirements.txt

## Guía de Uso Rápido (Paso a Paso)

Paso 1. Preparar el Dataset de Entrada
Coloca tu archivo de microdatos descargado del portal de datos en la carpeta data/raw/ con el nombre exacto:
data/raw/dataset_mimp.csv

Paso 2. Validar los Casos de Prueba (Opcional)
Ejecuta la suite de pruebas con pytest para verificar el correcto funcionamiento del motor de inferencia difusa con los casos teóricos (Casos A, B y C):
pytest tests/test_cases.py

Si la instalación y la lógica están intactas, la terminal devolverá 3 pruebas pasadas (3 passed).

Paso 3. Ejecutar el Pipeline Principal
Para procesar la totalidad del dataset y aplicar el modelo difuso fila por fila:
python main.py

Al finalizar la ejecución, se generará el archivo consolidado en:
data/processed/dataset_procesado_difuso.xlsx

## Arquitectura del Modelo Difuso

1. Variables Antecedentes (Entradas)
   -> Carga_Incidencia: Numero total de atenciones registradas (N° DE CASOS - MUJERES)
   - Rango: 0 - 100 casos
   - Conjuntos Difusos: Baja, Media, Alta

   -> Riesgo_Relacional: Porcentaje de agresiones cometidas por el entorno intimo (((Pareja + Ex Pareja) / N Casos Mujeres) \* 100)
   - Rango: 0% - 100%
   - Conjuntos Difusos: Baja, Media, Alta

   -> Vulnerabilidad_Etaria: Porcentaje de víctimas en rangos de edad de alta vulnerabilidad (((Menores(0-17) + Adultos Mayores(60+)) / N Casos Mujeres) \* 100)
   - Rango: 0% - 100%
   - Conjuntos Difusos: Baja, Media, Alta

2. Variable Consecuente (Salida)

- SCORE_PRIORIDAD_DIFUSA: Rango [0, 100] calculado mediante la defusificación por centroide sobre la agregación Max-Min de las 27 reglas difusas.
- CATEGORIA_RIESGO:
  -> Baja: Score < 35.0
  -> Media: 35.0 <= Score < 65.0
  -> Crítica: Score >= 65.0

## Integración con Power BI

1. Abre Power BI Desktop.
2. Haz clic en Obtener datos -> Libro de Excel.
3. Selecciona la ruta del archivo generado: data/processed/dataset_procesado_difuso.xlsx.
4. Utiliza los campos SCORE_PRIORIDAD_DIFUSA y CATEGORIA_RIESGO para construir mapas de calor, segmentadores de riesgo y paneles de priorización presupuestal o de asignación de recursos.
