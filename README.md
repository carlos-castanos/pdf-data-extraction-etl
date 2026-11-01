# PDF Data Extraction & ETL Pipeline

A Python command-line tool that extracts selected information from interactive PDF forms and consolidates the results into an Excel report.

## Project overview

The script processes a folder of PDF forms. For each form, it reads the participant name and monthly activity fields, identifies the latest month with recorded participation, retrieves the corresponding hours and course information, classifies the record, and adds it to a consolidated Excel file.

## Features

- Batch processing of PDF files in a folder.
- Extraction of interactive PDF form fields with `pypdf`.
- Identification of the latest month with recorded participation (September–August).
- Extraction of the corresponding hours and course information.
- Record classification using the form's auxiliary and regular-publisher indicators (`AUX`, `REG`, or `PUB`).
- Consolidation of records into an Excel report with `pandas` and `openpyxl`.
- Per-file error handling so one invalid PDF does not stop the remaining batch.
- Configurable input and output paths through command-line arguments.

## Technologies

- Python
- pypdf
- pandas
- openpyxl

## How it works

1. Read the PDF files from the input directory.
2. Retrieve the interactive form fields from each PDF.
3. Find the latest month where the participation checkbox is selected.
4. Extract the associated hours and course fields.
5. Determine the record category from the auxiliary and regular-publisher checkboxes.
6. Write all successfully processed records to an Excel report.

## Setup

Use Python 3.10 or later.

```bash
python -m venv .venv
```

Activate the virtual environment:

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Place the PDF forms in a folder named `pdfs` next to `extractor.py`, then run:

```bash
python extractor.py
```

By default, the report is saved as `Resumen.xlsx` in the current directory.

Custom paths can be provided:

```bash
python extractor.py --input-dir "path/to/pdfs" --output "reports/Resumen.xlsx"
```

Run `python extractor.py --help` to see all available options.

## Expected PDF form fields

The script relies on the field identifiers used by the source PDF form, including:

- `900_1_Text_SanSerif` — participant name.
- `900_10_CheckBox` — regular-publisher indicator.
- `901_{month}_CheckBox` — monthly participation indicator.
- `902_{month}_Text_C_SanSerif` — course information.
- `903_{month}_CheckBox` — auxiliary-pioneer indicator.
- `904_{month}_S21_Value` — reported hours.

The month indexes range from `20` (September) through `31` (August).

## Privacy

This repository does not include original PDF forms or generated Excel reports. Those files may contain personal or confidential information and should remain local. Use synthetic or anonymized examples for demonstrations.

## Limitations

- The script is designed for PDFs containing interactive form fields with the identifiers listed above; it does not perform OCR on scanned images.
- The month selection and classification rules follow the structure and indicators of the source form.
- A PDF that lacks readable form fields or the required name field is reported as an error and skipped.

## Project status

Portfolio-ready refactoring in progress.
