# Pagsubay Data Science — PHIVOLCS Earthquake Analysis

A data science repository focused on processing, cleaning, recalculating, and statistically modeling PHIVOLCS earthquake data in the Philippines.

## Overview

This project provides end-to-end data pipelines and analytical workflows for earthquake datasets:
- **Data Engineering & Standardization**: Aggregating and cleaning raw PHIVOLCS records (2010–2026), filtering $\ge 5.0$ magnitude events, and producing a structured master dataset.
- **Epicenter Recalculation Analysis**: Triangulation and error estimation comparing reported macroseismic intensity locations with true instrumental epicenters across historical and modern eras.
- **Statistical Earthquake Modeling**: Implementation of Ogata's Epidemic Type Aftershock Sequence (ETAS) point-process statistical model for seismic activity analysis.

---

## Repository Structure

```
pagsubay-datasci/
├── data-preprocess/                   # Master aggregated CSV datasets & preprocessing notebooks
├── Phivolc-past data and processes/   # Historical raw & processed PHIVOLCS data archives
├── copy_of_ogataprototype.py          # Python script for Ogata ETAS statistical modeling
├── Ogata-statisticalmodelearthquake.md # Technical specification for Ogata's statistical model
├── PROJECT_KEYPOINTS.md               # Detailed technical report & analytical findings
└── README.md                          # Project documentation
```

---

## Core Dataset Summary

- **Master File**: `data-preprocess/Phivolcs_Master_Aggregated_Fixed_FinalFinished.csv`
- **Event Scope**: 771 standardized earthquake events (Magnitude $\ge 5.0$, 2010-03-25 to 2026-02-15).
- **Identifiers**: Standardized Event IDs (`PHV-0001` through `PHV-0771`).

---

## How to Create a Virtual Environment in Python

### Option 1: Terminal / Command Line (Python `venv`)
```bash
# 1. Create a virtual environment named 'venv'
python -m venv venv

# 2. Activate the virtual environment:
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# On Windows (Command Prompt / CMD):
.\venv\Scripts\activate.bat

# On macOS / Linux:
source venv/bin/activate
```

### Option 2: If you are in VS Code
1. Open the Command Palette (`Ctrl+Shift+P` on Windows/Linux, `Cmd+Shift+P` on macOS).
2. Type **Python: Create Environment...** and select it.
3. Select **Venv**.
4. Choose your installed Python interpreter.
5. VS Code will automatically create `.venv` and activate it for your integrated terminal and Jupyter Notebooks.

---

## Dependencies & Execution

### Install Dependencies
```bash
pip install pandas numpy scipy matplotlib folium notebook
```

### Execution
- **Data Pipeline**: Open and run `data-preprocess/fix.ipynb`.
- **ETAS Model**: Run `python copy_of_ogataprototype.py`.
