# -*- coding: utf-8 -*-
"""
load_patient_data.py
====================
ITEC5025 – Week 6 Assignment: Setting Up the Development Environment
Author: Shruti Malik
Date:   2026-02-18

Purpose:
    Extract, clean, and save all four tables from the 100,000-patient
    EMRBots synthetic dataset (100000-Patients.zip) into tidy CSV files
    inside the data/ directory.

    Tables processed:
        PatientCorePopulatedTable.txt        → data/patients_cleaned.csv
        AdmissionsCorePopulatedTable.txt     → data/admissions_cleaned.csv
        AdmissionsDiagnosesCorePopulatedTable.txt → data/diagnoses_cleaned.csv
        LabsCorePopulatedTable.txt           → data/labs_cleaned.csv

    Cleaning steps applied to each table:
        • Strip leading/trailing whitespace from all string columns
        • Drop rows where the primary key (PatientID) is null or empty
        • Parse date columns into standard ISO-8601 format (YYYY-MM-DD HH:MM:SS)
        • Convert numeric columns to float; coerce invalid values to NaN
        • Remove exact duplicate rows
        • Report row counts before and after cleaning

How to run:
    python load_patient_data.py

    The zip file is expected at:
        ../100000-Patients.zip   (one level above this script)
    or in the same directory as this script.
"""

# ── Standard library imports ──────────────────────────────────────────────────
import os           # File path operations
import sys          # Exit on fatal error

# Force UTF-8 output on Windows so Unicode characters print correctly
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import zipfile      # Read files directly from the zip archive
import io           # Wrap zip byte-streams for pandas
from pathlib import Path  # Cross-platform path handling

# ── Third-party imports ───────────────────────────────────────────────────────
try:
    import pandas as pd
except ImportError:
    print("ERROR: pandas is not installed. Run:  pip install pandas")
    sys.exit(1)

# ── ANSI colour helpers ───────────────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RESET  = "\033[0m"

def ok(msg):   print(f"  {GREEN}[OK]  {msg}{RESET}")
def fail(msg): print(f"  {RED}[ERR] {msg}{RESET}")
def info(msg): print(f"  {CYAN}[i]   {msg}{RESET}")
def warn(msg): print(f"  {YELLOW}[!]   {msg}{RESET}")


# ── Configuration ─────────────────────────────────────────────────────────────

# Script directory (where this .py file lives)
SCRIPT_DIR = Path(__file__).parent.resolve()

# Look for the zip one level up (repo root) or in the same folder
ZIP_CANDIDATES = [
    SCRIPT_DIR.parent / "100000-Patients.zip",
    SCRIPT_DIR / "100000-Patients.zip",
]

# Output directory for cleaned CSVs
DATA_DIR = SCRIPT_DIR / "data"

# Table definitions: zip entry name → (output CSV name, date columns, numeric columns)
TABLES = {
    "PatientCorePopulatedTable.txt": {
        "output":   "patients_cleaned.csv",
        "pk":       "PatientID",
        "dates":    ["PatientDateOfBirth"],
        "numerics": ["PatientPopulationPercentageBelowPoverty"],
        "rename":   {
            "PatientID":                              "patient_id",
            "PatientGender":                          "gender",
            "PatientDateOfBirth":                     "date_of_birth",
            "PatientRace":                            "race",
            "PatientMaritalStatus":                   "marital_status",
            "PatientLanguage":                        "language",
            "PatientPopulationPercentageBelowPoverty":"poverty_pct",
        },
    },
    "AdmissionsCorePopulatedTable.txt": {
        "output":   "admissions_cleaned.csv",
        "pk":       "PatientID",
        "dates":    ["AdmissionStartDate", "AdmissionEndDate"],
        "numerics": ["AdmissionID"],
        "rename":   {
            "PatientID":          "patient_id",
            "AdmissionID":        "admission_id",
            "AdmissionStartDate": "admission_start",
            "AdmissionEndDate":   "admission_end",
        },
    },
    "AdmissionsDiagnosesCorePopulatedTable.txt": {
        "output":   "diagnoses_cleaned.csv",
        "pk":       "PatientID",
        "dates":    [],
        "numerics": ["AdmissionID"],
        "rename":   {
            "PatientID":                   "patient_id",
            "AdmissionID":                 "admission_id",
            "PrimaryDiagnosisCode":        "diagnosis_code",
            "PrimaryDiagnosisDescription": "diagnosis_description",
        },
    },
    "LabsCorePopulatedTable.txt": {
        "output":   "labs_cleaned.csv",
        "pk":       "PatientID",
        "dates":    ["LabDateTime"],
        "numerics": ["AdmissionID", "LabValue"],
        "rename":   {
            "PatientID":   "patient_id",
            "AdmissionID": "admission_id",
            "LabName":     "lab_name",
            "LabValue":    "lab_value",
            "LabUnits":    "lab_units",
            "LabDateTime": "lab_datetime",
        },
    },
}


# ── Core functions ────────────────────────────────────────────────────────────

def find_zip() -> Path:
    """
    Locate the 100000-Patients.zip file.

    Searches the candidate paths defined in ZIP_CANDIDATES.

    Returns:
        Path: Absolute path to the zip file.

    Raises:
        FileNotFoundError: If the zip cannot be found.
    """
    for candidate in ZIP_CANDIDATES:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        "Could not find 100000-Patients.zip.\n"
        "Expected locations:\n"
        + "\n".join(f"  {p}" for p in ZIP_CANDIDATES)
    )


def read_table_from_zip(zf: zipfile.ZipFile, entry_name: str) -> pd.DataFrame:
    """
    Read a tab-delimited text file from an open ZipFile into a DataFrame.

    Args:
        zf         (zipfile.ZipFile): Open zip archive.
        entry_name (str):             Name of the file inside the zip.

    Returns:
        pd.DataFrame: Raw (uncleaned) data.
    """
    with zf.open(entry_name) as raw_file:
        # Wrap bytes in a text-mode stream so pandas can read it
        text_stream = io.TextIOWrapper(raw_file, encoding="utf-8", errors="replace")
        df = pd.read_csv(text_stream, sep="\t", low_memory=False)
    return df


def clean_table(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Apply standard cleaning steps to a raw DataFrame.

    Steps:
        1. Strip whitespace from all object (string) columns.
        2. Drop rows where the primary key is null or empty.
        3. Parse date columns to datetime, then format as ISO strings.
        4. Convert numeric columns to float (invalid → NaN).
        5. Drop exact duplicate rows.

    Args:
        df     (pd.DataFrame): Raw data.
        config (dict):         Table config from TABLES dict.

    Returns:
        pd.DataFrame: Cleaned data with renamed columns.
    """
    raw_count = len(df)

    # Step 1 – strip whitespace from string columns
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda col: col.str.strip())

    # Step 2 – drop rows with null/empty primary key
    pk = config["pk"]
    if pk in df.columns:
        df = df[df[pk].notna() & (df[pk] != "")]

    # Step 3 – parse and reformat date columns
    for col in config.get("dates", []):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce") \
                        .dt.strftime("%Y-%m-%d %H:%M:%S")

    # Step 4 – coerce numeric columns
    for col in config.get("numerics", []):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Step 5 – drop exact duplicates
    df = df.drop_duplicates()

    # Rename columns to snake_case
    df = df.rename(columns=config.get("rename", {}))

    clean_count = len(df)
    dropped     = raw_count - clean_count
    return df, raw_count, clean_count, dropped


def save_csv(df: pd.DataFrame, output_path: Path) -> None:
    """
    Save a DataFrame to a UTF-8 CSV file (no index column).

    Args:
        df          (pd.DataFrame): Data to save.
        output_path (Path):         Destination file path.
    """
    df.to_csv(output_path, index=False, encoding="utf-8")


def print_summary(df: pd.DataFrame, table_name: str) -> None:
    """
    Print a brief statistical summary of a cleaned DataFrame.

    Args:
        df         (pd.DataFrame): Cleaned data.
        table_name (str):          Human-readable table name.
    """
    print(f"\n  {CYAN}── {table_name} preview ──{RESET}")
    print(df.head(3).to_string(index=False))
    print()
    info(f"Columns : {list(df.columns)}")
    info(f"Shape   : {df.shape[0]:,} rows × {df.shape[1]} columns")


# ── Main orchestration ────────────────────────────────────────────────────────

def main() -> None:
    """
    Orchestrate the full extract → clean → save pipeline.

    For each table in TABLES:
        1. Read from zip
        2. Clean
        3. Save to data/
        4. Print summary
    """
    print()
    print(f"{CYAN}{'=' * 60}")
    print("  ITEC5025 Week 6 – Patient Data Loader")
    print("  100,000-Patient EMRBots Synthetic Dataset")
    print(f"{'=' * 60}{RESET}")
    print()

    # ── Locate zip ────────────────────────────────────────────────────────────
    try:
        zip_path = find_zip()
        ok(f"Found dataset: {zip_path}")
    except FileNotFoundError as exc:
        fail(str(exc))
        sys.exit(1)

    # ── Ensure output directory exists ────────────────────────────────────────
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ok(f"Output directory: {DATA_DIR}")
    print()

    # ── Process each table ────────────────────────────────────────────────────
    results = []

    # Labs file is very large (~4 GB uncompressed); read it in chunks
    LARGE_FILES = {"LabsCorePopulatedTable.txt"}
    CHUNK_SIZE  = 100_000   # rows per chunk

    with zipfile.ZipFile(zip_path, "r") as zf:
        available = {e.filename for e in zf.infolist()}

        for entry_name, config in TABLES.items():
            print(f"Processing  {CYAN}{entry_name}{RESET} ...")

            if entry_name not in available:
                warn(f"  {entry_name} not found in zip -- skipping.")
                continue

            try:
                out_path = DATA_DIR / config["output"]

                if entry_name in LARGE_FILES:
                    # ── Chunked path for very large files ────────────────────
                    info(f"Large file detected -- reading in chunks of {CHUNK_SIZE:,} rows")
                    raw_n    = 0
                    clean_n  = 0
                    first    = True

                    with zf.open(entry_name) as raw_file:
                        text_stream = io.TextIOWrapper(raw_file, encoding="utf-8", errors="replace")
                        reader = pd.read_csv(
                            text_stream, sep="\t", low_memory=False,
                            chunksize=CHUNK_SIZE
                        )
                        for chunk_num, chunk in enumerate(reader, 1):
                            raw_n += len(chunk)
                            chunk_clean, _, c_clean, _ = clean_table(chunk, config)
                            clean_n += c_clean

                            # Write header only on first chunk
                            chunk_clean.to_csv(
                                out_path, mode="a" if not first else "w",
                                index=False, encoding="utf-8",
                                header=first
                            )
                            first = False

                            if chunk_num % 10 == 0:
                                info(f"  Processed {raw_n:,} rows so far ...")

                    ok(f"Cleaned -- {clean_n:,} rows retained")
                    ok(f"Saved -- {out_path.name}")

                else:
                    # ── Standard path for normal-sized files ─────────────────
                    df_raw = read_table_from_zip(zf, entry_name)
                    info(f"Read {len(df_raw):,} raw rows")

                    df_clean, raw_n, clean_n, dropped = clean_table(df_raw, config)
                    if dropped > 0:
                        warn(f"Dropped {dropped:,} rows (duplicates / null PKs)")
                    ok(f"Cleaned -- {clean_n:,} rows retained")

                    save_csv(df_clean, out_path)
                    ok(f"Saved -- {out_path.name}")

                    print_summary(df_clean, config["output"])

                results.append((entry_name, raw_n, clean_n, str(out_path)))

            except Exception as exc:
                fail(f"Error processing {entry_name}: {exc}")

    # ── Final report ──────────────────────────────────────────────────────────
    print(f"{CYAN}{'=' * 60}")
    print("  SUMMARY")
    print(f"{'=' * 60}{RESET}")
    for entry, raw_n, clean_n, out in results:
        print(f"  {GREEN}✓{RESET}  {entry}")
        print(f"       {raw_n:>10,} raw rows  →  {clean_n:>10,} clean rows")
        print(f"       Saved: {out}")
        print()

    print(f"{GREEN}  All tables processed successfully!{RESET}")
    print(f"  Cleaned CSVs are in: {DATA_DIR}")
    print()


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}  Interrupted by user. Goodbye!{RESET}\n")
        sys.exit(0)
