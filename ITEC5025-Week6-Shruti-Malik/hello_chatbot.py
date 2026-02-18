"""
hello_chatbot.py
================
ITEC5025 - Week 6 Assignment: Setting Up the Development Environment
Author: Shruti Malik
Date:   2026-02-18

Purpose:
    This script verifies that the Python development environment is correctly
    configured for the Hypotify Clinical Chatbot project. It checks:
      1. Python version
      2. TensorFlow installation and version
      3. Key supporting libraries (numpy, pandas, mysql-connector-python)
    It then prints the required "Hello, Chatbot!" confirmation message.

How to run:
    1. Create and activate a virtual environment:
           python -m venv chatbot_env
           chatbot_env\\Scripts\\activate      (Windows)
    2. Install dependencies:
           pip install tensorflow numpy pandas mysql-connector-python
    3. Run this script:
           python hello_chatbot.py
"""

# ── Standard library imports ──────────────────────────────────────────────────
import sys          # Access Python version and interpreter info
import platform     # Detect operating system details

# ── Helper: coloured console output ──────────────────────────────────────────
# ANSI escape codes let us print green (✓) or red (✗) status lines.
# We wrap them in a helper so the rest of the code stays readable.

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RESET  = "\033[0m"

def ok(msg: str) -> None:
    """Print a green success line."""
    print(f"  {GREEN}✓ {msg}{RESET}")

def fail(msg: str) -> None:
    """Print a red failure line."""
    print(f"  {RED}✗ {msg}{RESET}")

def info(msg: str) -> None:
    """Print a cyan informational line."""
    print(f"  {CYAN}ℹ {msg}{RESET}")


# ── Section 1: Python version check ──────────────────────────────────────────

def check_python() -> bool:
    """
    Verify that Python 3.8 or higher is installed.

    Returns:
        bool: True if the version requirement is met, False otherwise.
    """
    major, minor = sys.version_info.major, sys.version_info.minor
    version_str  = f"{major}.{minor}.{sys.version_info.micro}"

    if major == 3 and minor >= 8:
        ok(f"Python {version_str}  ({platform.system()} {platform.machine()})")
        return True
    else:
        fail(f"Python {version_str} detected — Python 3.8+ is required.")
        return False


# ── Section 2: TensorFlow check ───────────────────────────────────────────────

def check_tensorflow() -> bool:
    """
    Attempt to import TensorFlow and report its version.

    TensorFlow is the machine-learning backbone for the chatbot's intent
    classification model (to be built in later weeks).

    Returns:
        bool: True if TensorFlow imported successfully, False otherwise.
    """
    try:
        import tensorflow as tf                          # noqa: F401
        ok(f"TensorFlow {tf.__version__} installed")
        return True
    except ImportError:
        fail("TensorFlow not found — run:  pip install tensorflow")
        return False
    except Exception as exc:
        # Catch any unexpected import-time errors (e.g. DLL load failures)
        fail(f"TensorFlow import error: {exc}")
        return False


# ── Section 3: Supporting library checks ─────────────────────────────────────

def check_libraries() -> dict:
    """
    Check that key supporting libraries are available.

    Libraries checked:
        numpy            – numerical arrays for ML feature vectors
        pandas           – DataFrame-based patient data processing
        mysql.connector  – MySQL database connectivity for chatbot responses

    Returns:
        dict: {library_name: bool} indicating pass/fail for each library.
    """
    results = {}

    # numpy ───────────────────────────────────────────────────────────────────
    try:
        import numpy as np                               # noqa: F401
        ok(f"numpy {np.__version__} installed")
        results["numpy"] = True
    except ImportError:
        fail("numpy not found — run:  pip install numpy")
        results["numpy"] = False

    # pandas ──────────────────────────────────────────────────────────────────
    try:
        import pandas as pd                              # noqa: F401
        ok(f"pandas {pd.__version__} installed")
        results["pandas"] = True
    except ImportError:
        fail("pandas not found — run:  pip install pandas")
        results["pandas"] = False

    # mysql-connector-python ──────────────────────────────────────────────────
    try:
        import mysql.connector                           # noqa: F401
        ok("mysql-connector-python installed")
        results["mysql.connector"] = True
    except ImportError:
        fail("mysql-connector-python not found — run:  pip install mysql-connector-python")
        results["mysql.connector"] = False

    return results


# ── Section 4: Summary banner ─────────────────────────────────────────────────

def print_summary(python_ok: bool, tf_ok: bool, lib_results: dict) -> None:
    """
    Print a final pass/fail summary and the required greeting.

    Args:
        python_ok   (bool): Python version check result.
        tf_ok       (bool): TensorFlow check result.
        lib_results (dict): Results from check_libraries().
    """
    all_passed = python_ok and tf_ok and all(lib_results.values())

    print()
    print("=" * 55)

    if all_passed:
        # ── All checks passed ─────────────────────────────────────────────
        print(f"{GREEN}")
        print("  ██╗  ██╗███████╗██╗     ██╗      ██████╗ ██╗")
        print("  ██║  ██║██╔════╝██║     ██║     ██╔═══██╗██║")
        print("  ███████║█████╗  ██║     ██║     ██║   ██║██║")
        print("  ██╔══██║██╔══╝  ██║     ██║     ██║   ██║╚═╝")
        print("  ██║  ██║███████╗███████╗███████╗╚██████╔╝██╗")
        print("  ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝")
        print(f"{RESET}")
        print(f"  {GREEN}Hello, Chatbot!{RESET}")
        print()
        print("  Environment is fully configured.")
        print("  Ready to build the Hypotify Clinical Chatbot! 🚀")
    else:
        # ── Some checks failed ────────────────────────────────────────────
        print(f"{YELLOW}  Hello, Chatbot!{RESET}")
        print()
        print(f"  {YELLOW}⚠  Some dependencies are missing.{RESET}")
        print("  Please install the missing packages listed above,")
        print("  then re-run this script to confirm your environment.")

    print("=" * 55)
    print()


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    """
    Run all environment checks and print the final greeting.

    Control flow:
        1. Print header
        2. Check Python version
        3. Check TensorFlow
        4. Check supporting libraries
        5. Print summary / greeting
    """
    # Header
    print()
    print(f"{CYAN}{'=' * 55}")
    print("  ITEC5025 – Week 6: Environment Setup Check")
    print("  Hypotify Clinical Chatbot Project")
    print(f"{'=' * 55}{RESET}")
    print()

    # Run checks
    print("Checking environment …")
    print()

    python_ok   = check_python()
    tf_ok       = check_tensorflow()
    lib_results = check_libraries()

    # Final summary
    print_summary(python_ok, tf_ok, lib_results)


# Standard Python entry-point guard:
# Ensures main() only runs when this file is executed directly,
# not when it is imported as a module.
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Gracefully handle Ctrl+C without a traceback
        print(f"\n{YELLOW}  Interrupted by user. Goodbye!{RESET}\n")
        sys.exit(0)
