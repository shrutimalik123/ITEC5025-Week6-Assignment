# ITEC5025 – Week 6 Assignment: Setting Up the Development Environment

**Author:** Shruti Malik
**Course:** ITEC5025 – Advanced Chatbot Development
**Date:** February 18, 2026
**GitHub:** [ITEC5025-Week6-Assignment](https://github.com/shrutimalik123/ITEC5025-Week6-Assignment)

---

## Overview

This repository contains the Week 6 assignment for ITEC5025. The goal of this week is to set up the full development environment for the **Hypotify Clinical Chatbot** project, including:

1. Verifying the Python + TensorFlow environment is correctly configured
2. Setting up a MySQL database with chatbot response data
3. Loading and cleaning the **100,000-patient EMRBots synthetic dataset**

---

## Repository Structure

```
ITEC5025-Week6-Assignment/
│
├── ITEC5025-Week6-Shruti-Malik/     # Main submission folder
│   ├── hello_chatbot.py             # Environment verification script
│   ├── chatbot_responses.sql        # MySQL DB + 20 chatbot responses
│   ├── load_patient_data.py         # Loads & cleans the 100k patient dataset
│   ├── README.md                    # Detailed setup instructions
│   └── data/                        # Cleaned CSV output (generated)
│       ├── patients_cleaned.csv
│       ├── admissions_cleaned.csv
│       ├── diagnoses_cleaned.csv
│       └── labs_cleaned.csv
│
├── ITEC5025-WEEK5-Shruti-Malik-Chatbot/   # Week 5 chatbot (prior work)
├── 100000-Patients.zip                    # EMRBots synthetic dataset (raw)
├── ITEC5025-Week6-Shruti-Malik.zip        # Submission zip archive
└── README.md                              # This file
```

---

## Deliverables

| File | Description |
|------|-------------|
| `hello_chatbot.py` | Checks Python 3.8+, TensorFlow, numpy, pandas, mysql-connector-python and prints **"Hello, Chatbot!"** |
| `chatbot_responses.sql` | Creates `hypotify_chatbot` database, `chatbot_responses` table (20 responses), and `patient_demographics` table with 5 sample rows |
| `load_patient_data.py` | Extracts and cleans all 4 EMRBots tables from the zip; outputs tidy CSVs to `data/` |

---

## Quick Start

```powershell
# 1. Create and activate a virtual environment
python -m venv chatbot_env
chatbot_env\Scripts\activate

# 2. Install dependencies
pip install tensorflow numpy pandas mysql-connector-python

# 3. Verify the environment
python ITEC5025-Week6-Shruti-Malik/hello_chatbot.py

# 4. Load the patient dataset
python ITEC5025-Week6-Shruti-Malik/load_patient_data.py

# 5. Set up the MySQL database
mysql -u root -p < ITEC5025-Week6-Shruti-Malik/chatbot_responses.sql
```

---

## Dataset

- **Source:** [EMRBots](http://www.emrbots.org/) synthetic patient data (educational use only)
- **Size:** ~100,000 patients, ~500,000 admissions, ~500,000 diagnoses, millions of lab rows
- **No real patient data is used in this project.**

---

## Competencies Demonstrated

| Competency | Evidence |
|------------|----------|
| **Comp 1** – Basic programming | `hello_chatbot.py`: variables, control flow, functions, error handling |
| **Comp 2** – Advanced programming | `load_patient_data.py`: data structures, algorithms, robust error handling |
| **Comp 5** – User interfaces / SQL | `chatbot_responses.sql`: well-structured SQL with comments and verification queries |

---

## Connection to Prior Weeks

- **Week 5 Chatbot** (`ITEC5025-WEEK5-Shruti-Malik-Chatbot/`) built the core Hypotify chatbot logic
- This week's `patients_cleaned.csv` will replace hardcoded sample data in future weeks
- The MySQL `chatbot_responses` table will power the chatbot's response engine going forward

---

*Synthetic data only — no real patient information is used in this project.*
