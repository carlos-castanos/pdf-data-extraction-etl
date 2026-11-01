# PDF Data Extraction & ETL Pipeline

A Python-based automation tool that extracts structured information from PDF forms and consolidates the results into an Excel report.

## Project Overview

This project automates the processing of multiple PDF records by extracting form fields, identifying the latest month with recorded participation, classifying records, and generating a consolidated Excel dataset.

## Key Features

- Batch processing of PDF files.
- Extraction of structured form fields using Python.
- Identification of the latest month with recorded participation.
- Extraction of reported hours and course information.
- Record classification based on form selections.
- Name normalization and Excel report generation.

## Data Processing Workflow

1. **Input:** A folder containing multiple PDF forms.
2. **Extraction:** Retrieve information from interactive PDF form fields.
3. **Transformation:** Identify the latest month with participation and determine the corresponding record attributes.
4. **Classification:** Assign a record category based on the selected form fields.
5. **Output:** Generate a consolidated Excel report using pandas.

## Technologies

- Python
- pypdf
- pandas
- openpyxl
- PDF form field extraction
- Excel report generation

## Business Value

The tool reduces repetitive manual data collection by processing multiple PDF records and consolidating relevant information into a structured spreadsheet.

## Data Privacy

This repository will use anonymized or synthetic examples. No original personal records or confidential documents are included.

## Project Status

In development.
