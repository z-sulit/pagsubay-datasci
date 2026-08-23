# Pagsubay Data Science — PHIVOLCS Earthquake Analysis

A data science repository focused on processing, cleaning, recalculating, and statistically modeling PHIVOLCS earthquake data in the Philippines.

##  Overview

This project provides end-to-end data pipelines and analytical workflows for earthquake datasets:
- **Data Engineering & Standardization**: Aggregating and cleaning raw PHIVOLCS records (2010–2026), filtering $\ge 5.0$ magnitude events, and producing a structured master dataset.
- **Epicenter Recalculation Analysis**: Triangulation and error estimation comparing reported macroseismic intensity locations with true instrumental epicenters across historical and modern eras.
- **Statistical Earthquake Modeling**: Implementation of Ogata's Epidemic Type Aftershock Sequence (ETAS) point-process statistical model for seismic activity analysis.


---

## 📊 Core Dataset Summary

- **Master File**: `data-preprocess/Phivolcs_Master_Aggregated_Fixed_FinalFinished.csv`
- **Event Scope**: 771 standardized earthquake events (Magnitude $\ge 5.0$, 2010-03-25 to 2026-02-15).
- **Identifiers**: Standardized Event IDs (`PHV-0001` through `PHV-0771`).

---

## 🛠️ Usage

### Prerequisites
```bash
pip install pandas numpy scipy matplotlib folium
```

### Execution
- **Data Pipeline**: Run or inspect `data-preprocess/fix.ipynb`.
- **ETAS Model**: Execute `python copy_of_ogataprototype.py`.
