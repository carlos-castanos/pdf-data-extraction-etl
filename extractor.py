"""Extract participation data from interactive PDF forms into an Excel report."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import pandas as pd
from pypdf import PdfReader

# PDF form field names used by the original source forms.
NAME_FIELD = "900_1_Text_SanSerif"
REGULAR_PUBLISHER_FIELD = "900_10_CheckBox"
MONTHS = {
    20: "Septiembre",
    21: "Octubre",
    22: "Noviembre",
    23: "Diciembre",
    24: "Enero",
    25: "Febrero",
    26: "Marzo",
    27: "Abril",
    28: "Mayo",
    29: "Junio",
    30: "Julio",
    31: "Agosto",
}
OUTPUT_COLUMNS = ["Nombre", "Tipo", "Mes", "Horas", "Cursos"]


def get_field_value(fields: dict[str, Any], field_name: str, default: Any = None) -> Any:
    """Return a PDF form field value, or a default when the field is absent."""
    field = fields.get(field_name)
    if field is None:
        return default

    value = getattr(field, "value", None)
    if value is not None:
        return value

    # Compatibility fallback for dictionary-like pypdf Field objects.
    try:
        return field.get("/V", default)
    except AttributeError:
        return default


def is_checked(value: Any) -> bool:
    """Interpret common checked values returned by interactive PDF fields."""
    return str(value).strip().lower() in {"/yes", "yes", "/on", "on", "true", "1"}


def clean_text(value: Any) -> str:
    """Convert a field value into trimmed text, keeping empty values empty."""
    if value is None:
        return ""
    return str(value).strip()


def get_latest_participation(fields: dict[str, Any]) -> dict[str, Any]:
    """Get the last month with participation and its related details."""
    latest = {"Mes": None, "Cursos": None, "Horas": None, "Auxiliar": False}

    # The source form stores September through August in fields 20 through 31.
    # Iterating in order preserves the original behavior: the last checked month wins.
    for index, month in MONTHS.items():
        participated = is_checked(
            get_field_value(fields, f"901_{index}_CheckBox", False)
        )
        if not participated:
            continue

        latest = {
            "Mes": month,
            "Cursos": clean_text(
                get_field_value(fields, f"902_{index}_Text_C_SanSerif")
            ),
            "Horas": clean_text(
                get_field_value(fields, f"904_{index}_S21_Value")
            ),
            "Auxiliar": is_checked(
                get_field_value(fields, f"903_{index}_CheckBox", False)
            ),
        }

    return latest


def get_record_type(fields: dict[str, Any], auxiliary: bool) -> str:
    """Classify a record using the source form's auxiliary/regular indicators."""
    if auxiliary:
        return "AUX"

    is_regular = is_checked(
        get_field_value(fields, REGULAR_PUBLISHER_FIELD, False)
    )
    return "REG" if is_regular else "PUB"


def extract_pdf_record(pdf_path: Path) -> dict[str, Any]:
    """Extract one record from a PDF form."""
    reader = PdfReader(str(pdf_path))
    fields = reader.get_fields()
    if not fields:
        raise ValueError("El PDF no contiene campos de formulario legibles.")

    name = clean_text(get_field_value(fields, NAME_FIELD))
    if not name:
        raise ValueError(f"No se encontró el campo obligatorio {NAME_FIELD}.")

    # Preserve the original cleanup rule used by the source script.
    name = name.split("Cel")[0].strip()
    latest = get_latest_participation(fields)

    return {
        "Nombre": name,
        "Tipo": get_record_type(fields, latest["Auxiliar"]),
        "Mes": latest["Mes"],
        "Horas": latest["Horas"],
        "Cursos": latest["Cursos"],
    }


def process_pdf_directory(input_dir: Path, output_file: Path) -> tuple[int, int]:
    """Process all PDFs in a directory and write a consolidated Excel report.

    Returns:
        A tuple containing (successful_records, failed_files).
    """
    if not input_dir.exists():
        raise FileNotFoundError(f"No existe la carpeta de entrada: {input_dir}")
    if not input_dir.is_dir():
        raise NotADirectoryError(f"La ruta de entrada no es una carpeta: {input_dir}")

    pdf_files = sorted(input_dir.glob("*.pdf"))
    print(f"Se encontraron {len(pdf_files)} archivos PDF en: {input_dir}")

    records: list[dict[str, Any]] = []
    failed_files = 0

    for pdf_path in pdf_files:
        try:
            records.append(extract_pdf_record(pdf_path))
            print(f"[OK] {pdf_path.name}")
        except Exception as error:  # Keep processing the remaining files.
            failed_files += 1
            print(f"[ERROR] {pdf_path.name}: {error}")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    report = pd.DataFrame(records, columns=OUTPUT_COLUMNS)
    report.to_excel(output_file, index=False)
    print(f"Reporte generado: {output_file}")
    print(f"Registros procesados: {len(records)} | Archivos con error: {failed_files}")

    return len(records), failed_files


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extrae datos de formularios PDF y genera un reporte Excel."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("pdfs"),
        help="Carpeta que contiene los PDF (predeterminada: ./pdfs).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("Resumen.xlsx"),
        help="Ruta del archivo Excel de salida (predeterminada: ./Resumen.xlsx).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        _, failed_files = process_pdf_directory(args.input_dir, args.output)
    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"[ERROR] {error}")
        return 1

    return 1 if failed_files else 0


if __name__ == "__main__":
    raise SystemExit(main())
