# Pagsubay Data Science — PHIVOLCS Earthquake Analysis

A data science repository focused on processing, cleaning, recalculating, and statistically modeling PHIVOLCS earthquake data in the Philippines.

## 📌 Overview

This project provides end-to-end data pipelines and analytical workflows for earthquake datasets:
- **Data Engineering & Standardization**: Aggregating and cleaning raw PHIVOLCS records (2010–2026), filtering $\ge 5.0$ magnitude events, and producing a structured master dataset.
- **Epicenter Recalculation Analysis**: Triangulation and error estimation comparing reported macroseismic intensity locations with true instrumental epicenters across historical and modern eras.
- **Statistical Earthquake Modeling**: Implementation of Ogata's Epidemic Type Aftershock Sequence (ETAS) point-process statistical model for seismic activity analysis.

---

## 📁 Repository Structure

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

## 📊 Core Dataset Summary

- **Master File**: `data-preprocess/Phivolcs_Master_Aggregated_Fixed_FinalFinished.csv`
- **Event Scope**: 771 standardized earthquake events (Magnitude $\ge 5.0$, 2010-03-25 to 2026-02-15).
- **Identifiers**: Standardized Event IDs (`PHV-0001` through `PHV-0771`).

---

## 🛠️ Environment Setup & Usage

### 1. Virtual Environment Setup (`venv`)

#### Option A: Terminal / Command Line
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Activate on Windows (CMD)
.\venv\Scripts\activate.bat

# Activate on macOS/Linux
source venv/bin/activate
```

#### Option B: If you are in VS Code
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) to open the Command Palette.
2. Select **Python: Create Environment...**
3. Choose **Venv**.
4. Select your Python interpreter version.
5. VS Code will create the `.venv` environment and prompt to automatically select it for your workspace terminal and notebooks.

---

### 2. Install Dependencies
```bash
pip install pandas numpy scipy matplotlib folium notebook
```

---

### 3. Execution
- **Data Pipeline**: Open and run `data-preprocess/fix.ipynb`.
- **ETAS Model**: Run `python copy_of_ogataprototype.py`.

