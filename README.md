# Extractor de datos desde formularios PDF

Este proyecto nació para reducir el trabajo manual de revisar varios formularios PDF y pasar su información a una hoja de cálculo. El programa lee los campos de formularios PDF interactivos, identifica el último mes con participación registrada y genera un reporte de Excel con los datos principales.

## ¿Qué hace?

- Procesa varios archivos PDF de una carpeta.
- Extrae información de los campos del formulario con `pypdf`.
- Identifica el último mes en el que aparece participación registrada (de septiembre a agosto).
- Recupera las horas y la información de cursos de ese mes.
- Clasifica cada registro con los indicadores del formulario.
- Consolida los resultados en un archivo Excel con `pandas` y `openpyxl`.
- Si un archivo tiene un error, lo reporta y continúa con los demás.

## Cómo funciona

1. Coloco los formularios PDF en una carpeta.
2. El programa lee los campos interactivos de cada archivo.
3. Revisa los meses en orden y conserva la información del último mes marcado.
4. Extrae los datos relacionados con ese mes.
5. Agrega el registro a una tabla.
6. Genera un archivo Excel con el resultado.

## Herramientas utilizadas

- Python
- pypdf
- pandas
- openpyxl

## Instalación

Se necesita Python 3.10 o una versión posterior.

Crea y activa un entorno virtual:

```bash
python -m venv .venv
```

En Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

En macOS o Linux:

```bash
source .venv/bin/activate
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Cómo ejecutarlo

Coloca los PDF en una carpeta llamada `pdfs`, al mismo nivel que `extractor.py`, y ejecuta:

```bash
python extractor.py
```

Por defecto, el reporte se guarda como `Resumen.xlsx`.

También puedes indicar otras rutas:

```bash
python extractor.py --input-dir "ruta/a/los/pdf" --output "reportes/Resumen.xlsx"
```

Para consultar las opciones disponibles:

```bash
python extractor.py --help
```

## Ejemplo del resultado

El reporte contiene estas columnas:

| Nombre | Tipo | Mes | Horas | Cursos |
|---|---|---|---:|---:|
| Persona de ejemplo | REG | Octubre | 12 | 2 |
| Registro de prueba | AUX | Noviembre | 15 | 3 |

Los datos de esta tabla son ficticios y solo muestran la estructura del resultado.

## Pruebas

Para ejecutar las pruebas incluidas:

```bash
python -m unittest test_extractor.py -v
```

Las pruebas comprueban la lectura de casillas, la selección del último mes marcado y la clasificación de los registros. No sustituyen una prueba completa con formularios PDF reales.

## Consideraciones y límites

- El programa necesita PDF con campos de formulario interactivos que utilicen los identificadores esperados por el código.
- No realiza OCR; por lo tanto, no extrae información de documentos que sean únicamente imágenes escaneadas.
- Si un PDF no contiene los campos necesarios o no tiene un nombre legible, se reporta como error y se omite.
- La selección del mes y las reglas de clasificación siguen la estructura del formulario para el que se creó el programa.

## Privacidad

No incluyo aquí los formularios originales ni los reportes generados, porque pueden contener información personal. Para probar el programa, utiliza archivos propios con datos ficticios o anonimizados.

## Estado del proyecto

Versión de portafolio. La lógica principal está documentada y cuenta con pruebas unitarias básicas; todavía se puede ampliar la cobertura con archivos PDF de ejemplo anonimizados.
