# PHIVOLCS Earthquake Data Project — Detailed Keypoints of Work Done

## Analysis scope

This summary documents the work represented by the project files in this repository **excluding the `documents/` folder**, as requested. The `documents/` folder was treated only as reference material and was not used as evidence for the work summary.

Included evidence came from:

- `Phivolc-past data and processes/PHIVOLCS_DATA-20260520T033532Z-3-001/PHIVOLCS_DATA/`
- `Phivolc-past data and processes/Phivolcs_projectCode-20260520T033529Z-3-001/Phivolcs_projectCode/`
- `Phivolc-past data and processes/phivolcs_calculation-20260520T033535Z-3-001/phivolcs_calculation/`
- `data-preprocess/`

---

## High-level summary

I built a PHIVOLCS earthquake data collection, preprocessing, and epicenter recalculation workflow. The work focused on gathering earthquake records from PHIVOLCS, converting them into structured CSV files, cleaning inconsistent formats, aggregating monthly and yearly datasets, filtering stronger earthquakes, enriching records with geographic details, preparing a final master dataset with standardized fields and event IDs, and supporting recalculation analysis that compares true epicenters against estimated epicenters from intensity-report data.

The final output of the preprocessing work is a cleaned master earthquake dataset:

- `data-preprocess/Phivolcs_Master_Aggregated_Fixed_FinalFinished.csv`
- Final row count: **771 earthquake events**
- Final schema: **18 columns**
- Event ID format: `PHV-0001` to `PHV-0771`
- Date coverage in final file: **2010-03-25 to 2026-02-15**
- Main focus: earthquakes with magnitude **5.0 and above**, plus location/geographic enrichment

---

## Added project summary: Epicenter recalculation analysis

Beyond the raw data collection and preprocessing work, the project also includes an epicenter recalculation analysis workflow. The primary objective of this part was to **automate and refine the recalculation of earthquake epicenters using intensity reports, reported-site/station data, and cleaned event metadata**.

This part of the work covered three major areas:

1. **Data engineering and management**
2. **Analytical recalculation and accuracy testing**
3. **Reporting and geospatial visualization**

### Data engineering and management

- I cleaned and standardized PHIVOLCS master data covering **2010 to October 2025**.
- I sorted cleaned records by time and improved consistency across coordinate fields and location metadata.
- I worked with a structured database-style design where event-level information, catalog details, intensity reports, and recalculated epicenter estimates can be related to one another.
- I documented important limitations in the data, especially cases where recalculation was not mathematically reliable.
- I identified event-grouping problems caused by incomplete or conflicting timestamps.
- I noted that triangulation-style recalculation requires at least **three usable reported sites**; fewer than three points cannot produce a stable epicenter estimate.

### Analytical recalculation

- I performed recalculation across multiple historical and contemporary categories, including:
  - **Early American**
  - **Early Spanish**
  - **Early Span**
  - **Late Span**
  - **Contemporary**
- I compared each known or reported epicenter against a recalculated epicenter.
- I used fields such as:
  - true latitude
  - true longitude
  - recalculated latitude
  - recalculated longitude
  - error distance in kilometers
- I treated the error distance as the main accuracy signal between the official/known epicenter and the recalculated epicenter.
- I refined some events by removing geographic outliers when they distorted the recalculation.
- One example noted was **Event 7** in the Early Spanish era, where filtering out an outlier location such as **Vigan** improved recalculation stability and produced a more reliable estimated epicenter.

### Reporting and visualization

- I generated event-specific reports for selected recalculation cases.
- The reports included:
  - comparison of true vs. estimated epicenters
  - distance error statistics
  - recalculated statistics after outlier removal
  - mean radius
  - standard deviation
- I created interactive HTML maps with Leaflet/Folium-style visualization to show:
  - measured or true epicenters
  - recalculated epicenter points
  - reported-site points
  - radius circles for events and intensity levels
- I documented a critical triangulation limitation for **Event 726**: even though three reports existed, they came from the exact same location. This created a “single dot” problem, meaning the event could not be triangulated because the three reports did not provide three spatially distinct points.

### Additional user-provided source list for this recalculation section

The following source names were provided as additional context for the epicenter recalculation part of the project. These are listed here as user-provided source references and are separate from the excluded `documents/` folder:

- `PHIVOLCS_Main Data report (2010 - Oct 2025).pdf`
- `PHIVOLCS_Master_Final_Cleaned.csv`
- `PHIVOLCS_Master_With_PlaceCoords.csv`
- `cleaned_with_time_sorted.csv`
- `cleaned_2025-2025.csv`
- `phivolcs_erd_sample(fix1).jpg`
- `Epicenter_Recalculation_Analysis`
- `Contemporary_Epicenter_Recalculation_Analysis.csv`
- `EarlyAme_Epicenter_Recalculation_Analysis`
- `EarlySpan_Epicenter_Recalculation_Analysis`
- `LateSpan_Epicenter_Recalculation_Analysis`
- `EarlyAme_Epicenter_Recalculation_Analysis.csv`
- `LateSpan_Epicenter_Recalculation_Analysis.csv`
- `EarlySpanish_Narrative_Report.txt`
- `Event_97_Report.pdf`
- `Event_78_Report.pdf`
- `Event_95_Report.pdf`
- `Event_64_Report.pdf`
- `Event_91_Report.pdf`
- `Event_64_Map.html`
- `Event_65_Map.html`
- `Event_67_Map.html`
- `Intensity_5_Map.html`
- `Intensity_6_Map.html`

---

## What I exactly did

### 1. Organized the PHIVOLCS earthquake data workspace

I organized the project into separate areas for raw/past PHIVOLCS data, notebook-based collection code, calculation references, and final preprocessing outputs.

Key folders used:

- `Phivolc-past data and processes/PHIVOLCS_DATA-20260520T033532Z-3-001/PHIVOLCS_DATA/`
  - Contains monthly, yearly, master, and final PHIVOLCS earthquake CSV files.
- `Phivolc-past data and processes/Phivolcs_projectCode-20260520T033529Z-3-001/Phivolcs_projectCode/`
  - Contains the Jupyter notebooks used for data collection and special-case cleaning.
- `data-preprocess/`
  - Contains the later-stage preprocessing notebook and final cleaned datasets.

The repository is mainly a **data processing project**, not a packaged software application. The main work is stored in notebooks, CSV outputs, Excel checking files, and calculation PDFs.

---

### 2. Scraped PHIVOLCS earthquake data from web pages

I created notebook-based scraping workflows to collect earthquake data from PHIVOLCS pages.

Main scraping notebooks:

- `Phivolc-past data and processes/Phivolcs_projectCode-20260520T033529Z-3-001/Phivolcs_projectCode/PROJECT_DataCollection.ipynb`
- `Phivolc-past data and processes/Phivolcs_projectCode-20260520T033529Z-3-001/Phivolcs_projectCode/PROJECT_DataCollection(PAGE2).ipynb`

The scraping process used:

- `requests` for fetching PHIVOLCS pages
- `BeautifulSoup` from `bs4` for parsing HTML
- `pandas` for converting scraped table rows into DataFrames
- PHIVOLCS monthly pages such as:
  - `https://earthquake.phivolcs.dost.gov.ph/`
  - `https://earthquake.phivolcs.dost.gov.ph/EQLatest-Monthly/{year}/{year}_{month}.html`

The scraper looked for PHIVOLCS earthquake tables using the HTML class:

```text
MsoNormalTable
```

Then it extracted earthquake columns into a structured table with fields such as:

- `Date - Time (Philippine Time)`
- `Latitude (�N)`
- `Longitude (�E)`
- `Depth (km)`
- `Mag`
- `Coordinates`
- `Location`

---

### 3. Converted PHIVOLCS web tables into monthly CSV files

I converted scraped PHIVOLCS earthquake tables into monthly CSV files.

Examples of generated monthly files include:

- `phivolcs_earthquakes_2025_10_October.csv`
- `phivolcs_earthquakes_2025_09_September.csv`
- `phivolcs_earthquakes_2024_01_January.csv`
- `phivolcs_earthquakes_2023_12_December.csv`
- `phivolcs_earthquakes_2022_08_August.csv`
- `phivolcs_earthquakes_2021_07_July.csv`
- `phivolcs_earthquakes_2020_12_December.csv`
- `phivolcs_earthquakes_2019_10_October.csv`
- `phivolcs_earthquakes_2018_07_July.csv`
- `phivolcs_earthquakes_2017_12_December.csv`

Within `PHIVOLCS_DATA`, there are **130 monthly CSV files** across the year folders.

---

### 4. Handled inconsistent PHIVOLCS page formats

The PHIVOLCS source pages were not all consistent, so I wrote special-case extraction logic for problem months and years.

Examples of special handling found in the notebooks:

- The 2025 pages were handled partly with direct month-specific extraction cells.
- July 2025 required different handling because the table shape differed from surrounding months.
- Some pages had the location field combined with distance/bearing information, so I split `Location` into:
  - `Coordinates`
  - cleaned `Location`
- Some months had rows where the number of columns did not match the expected structure, so the code used `row[:6]` to keep the expected six PHIVOLCS fields before further splitting.
- Some 2018 pages had more difficult table/date structures, so I added custom date extraction logic using `re` and table cell parsing.
- 2017 required text-based parsing rather than only normal HTML-table scraping.

Notebook evidence:

- `PROJECT_DataCollection.ipynb` contains year/month page dictionaries for scraping 2019–2024 and direct month extraction for 2025.
- `PROJECT_DataCollection(PAGE2).ipynb` contains extra checks and cleaning for months such as October 2025, 2019 months, 2021 months, 2020 months, and difficult 2018 months.
- `PROJECT_DataCollection(PAGE3).ipynb` contains the custom 2017 parser.

---

### 5. Built a custom parser for 2017 earthquake records

For 2017 data, I built a regex/state-machine parser in:

- `Phivolc-past data and processes/Phivolcs_projectCode-20260520T033529Z-3-001/Phivolcs_projectCode/PROJECT_DataCollection(PAGE3).ipynb`

That parser handled text files and extracted records by recognizing patterns for:

- date/time
- latitude
- longitude
- depth
- magnitude
- month headers
- location text

The notebook includes repeated monthly parsing sections for:

- January 2017
- February 2017
- March 2017
- April 2017
- May 2017
- June 2017
- July 2017
- August 2017
- September 2017
- October 2017
- November 2017
- December 2017

For later 2017 months, I added an additional `row_rx` regex to catch rows where the date/time, coordinates, depth, and magnitude appeared on a single line.

This converted messy 2017 text-style earthquake records into structured monthly CSV files.

---

### 6. Created yearly aggregate files

After generating monthly files, I created yearly aggregate CSVs for each year.

Yearly aggregate row counts found in the project files:

| Year | Rows |
|---:|---:|
| 2010–2014 | 28 |
| 2015 | 1,637 |
| 2016 | 2,794 |
| 2017 | 5,260 |
| 2018 | 6,264 |
| 2019 | 12,986 |
| 2020 | 14,047 |
| 2021 | 12,054 |
| 2022 | 20,601 |
| 2023 | 16,631 |
| 2024 | 18,148 |
| 2025 | 16,105 |

Evidence files include:

- `PHIVOLCS_DATA/2015/phivolcs_earthquakes_2015.csv`
- `PHIVOLCS_DATA/2016/phivolcs_earthquakes_2016.csv`
- `PHIVOLCS_DATA/2017/phivolcs_earthquakes_2017.csv`
- `PHIVOLCS_DATA/2018/phivolcs_earthquakes_2018.csv`
- `PHIVOLCS_DATA/2019/phivolcs_earthquakes_2019.csv`
- `PHIVOLCS_DATA/2020/phivolcs_earthquakes_2020.csv`
- `PHIVOLCS_DATA/2021/phivolcs_earthquakes_2021.csv`
- `PHIVOLCS_DATA/2022/phivolcs_earthquakes_2022.csv`
- `PHIVOLCS_DATA/2023/phivolcs_earthquakes_2023.csv`
- `PHIVOLCS_DATA/2024/phivolcs_earthquakes_2024.csv`
- `PHIVOLCS_DATA/2025/phivolcs_earthquakes_2025.csv`

---

### 7. Built a raw master earthquake dataset

I combined yearly earthquake files into a master PHIVOLCS earthquake dataset:

- `Phivolc-past data and processes/PHIVOLCS_DATA-20260520T033532Z-3-001/PHIVOLCS_DATA/Master File/phivolcs_earthquakes.csv`

This master file contains:

- **126,555 rows**
- Columns:
  - `Date - Time (Philippine Time)`
  - `Latitude (�N)`
  - `Longitude (�E)`
  - `Depth (km)`
  - `Mag`
  - `Coordinates`
  - `Location`

This file represents the broad PHIVOLCS earthquake catalog assembled from the collected monthly/yearly data.

---

### 8. Cleaned and preserved a cleaned master copy

I also produced cleaned master-file versions, including:

- `PHIVOLCS_DATA/Master File/phivolcs_earthquakes_cleaned.csv`
- `PHIVOLCS_DATA/Final Data File/phivolcs_earthquakes_cleaned.csv`

Both cleaned master files contain:

- **126,555 rows**
- The same core PHIVOLCS earthquake schema

This indicates I preserved a cleaned full-catalog version separate from the later magnitude-filtered/enriched dataset.

---

### 9. Filtered the master catalog to magnitude 5.0 and above

I created magnitude-filtered files focused on stronger earthquakes.

Important files:

- `PHIVOLCS_DATA/Master File/phivolcs_earthquakes_5_0Abv.csv`
- `PHIVOLCS_DATA/Master File/phivolcs_earthquakes_5_0Abv_pt1.csv`
- `PHIVOLCS_DATA/Master File/phivolcs_earthquakes_5_0Abv_pt2.csv`
- `PHIVOLCS_DATA/Master File/phivolcs_earthquakes_5_0Abv_unique_locs.csv`
- `PHIVOLCS_DATA/Final Data File/phivolcs_earthquakes_5_0Abv (1).csv`

The raw master file contains **780 rows** with `Mag >= 5.0` based on the available `Mag` values.

The later final enriched master dataset contains **771 rows**, meaning the final working set was the magnitude-5+ earthquake list after later cleaning, enrichment, and manual fixes.

---

### 10. Checked duplicates and data quality during collection

The notebooks include explicit duplicate checking using:

```python
df.duplicated().sum()
df[df.duplicated(keep=False)]
```

I also used `drop_duplicates(keep="first")` in specific cases where duplicate rows needed to be removed.

A notable example appears in the 2025 February handling, where a duplicate/misplaced February 16 record was identified in the notebook comments and removed.

The notebooks also printed null counts for scraped monthly outputs, which helped verify whether table extraction produced missing fields.

---

### 11. Geocoded earthquake locations

In the preprocessing notebook:

- `data-preprocess/fix.ipynb`

I added location geocoding using:

- `geopy`
- `Nominatim`
- `RateLimiter`

The workflow:

1. Loaded a magnitude-filtered earthquake CSV.
2. Cleaned location strings for searching.
3. Sent location queries to Nominatim.
4. Used rate limiting to avoid sending requests too quickly.
5. Caught timeout and service errors.
6. Extracted geocoded latitude and longitude into:
   - `loc_latitude`
   - `loc_longitude`

The geocoding output is visible in files such as:

- `data-preprocess/Phivolcs_aggregated.csv`
- `data-preprocess/Phivolcs_aggregated_final_list.csv`
- `PHIVOLCS_DATA/Final Data File/phivolcs_earthquakes_5_0Abv_FULL_with_coords.csv`

The `phivolcs_earthquakes_5_0Abv_FULL_with_coords.csv` file contains unique location-to-coordinate mappings with columns:

- `Location`
- `Coordinates of Place`

---

### 12. Parsed locations into city, province, and region

In `data-preprocess/fix.ipynb`, I created a `parse_location()` function to split PHIVOLCS location strings into more usable fields.

The parser handled locations like:

```text
Cagwait (Surigao Del Sur)
Balut Island (Municipality Of Sarangani) (Davao Occidental)
```

It extracted:

- `city`
- `province`
- `region`

The logic handled:

- one parenthetical group as province
- two or more parenthetical groups as city/province-style entries
- cleanup of labels such as `Municipality Of` and `City Of`

---

### 13. Mapped provinces to Philippine regions

I created a `province_to_region` dictionary in `data-preprocess/fix.ipynb` to map provinces into Philippine regions.

The mapping covers major Philippine regions including:

- Ilocos Region
- Cagayan Valley
- Central Luzon
- CALABARZON
- MIMAROPA
- Bicol Region
- Western Visayas
- Central Visayas
- Eastern Visayas
- Zamboanga Peninsula
- Northern Mindanao
- Davao Region
- SOCCSKSARGEN
- Caraga
- BARMM
- CAR

The code normalized province names using lowercase/strip matching before assigning regions.

The final file contains:

- **65 unique province values**
- **23 unique region values**
- **209 unique city values**
- **226 unique location values**

Top regions in the final dataset:

| Region | Event count |
|---|---:|
| Davao Region (Region XI) | 277 |
| Caraga (Region XIII) | 152 |
| Cagayan Valley (Region II) | 69 |
| SOCCSKSARGEN (Region XII) | 43 |
| Eastern Visayas (Region VIII) | 43 |

Top provinces in the final dataset:

| Province | Event count |
|---|---:|
| Davao Occidental | 173 |
| Surigao Del Sur | 97 |
| Davao Oriental | 89 |
| Surigao Del Norte | 34 |
| Batanes | 32 |

---

### 14. Parsed epicenter relative-coordinate text into numeric/directional fields

The PHIVOLCS `Coordinates` field often contains relative descriptions such as:

```text
028km N 86° E
094 km S 75° E
```

In `data-preprocess/fix.ipynb`, I created a parser that extracted:

- distance in kilometers
- north/south direction
- angle in degrees
- east/west direction
- computed azimuth

This created derived columns that appear in the final schema as:

- `distance_km`
- `ns`
- `angle_deg`
- `ew`

This made the relative PHIVOLCS coordinate descriptions easier to analyze computationally.

---

### 15. Standardized date and time fields

The raw PHIVOLCS master file used combined date/time strings such as:

```text
25 March 2010
16 February 2025 - 07:47 AM
```

In preprocessing, I separated and standardized these into:

- `date`
- `time`

Final date examples use formats like:

```text
10/11/2025
2/15/2026
```

The final cleaned file has a date range of:

- Earliest: **2010-03-25**
- Latest: **2026-02-15**

Final event counts by year:

| Year | Final events |
|---:|---:|
| 2010 | 5 |
| 2011 | 7 |
| 2012 | 7 |
| 2013 | 8 |
| 2014 | 1 |
| 2015 | 36 |
| 2016 | 39 |
| 2017 | 43 |
| 2018 | 42 |
| 2019 | 75 |
| 2020 | 59 |
| 2021 | 69 |
| 2022 | 93 |
| 2023 | 119 |
| 2024 | 70 |
| 2025 | 79 |
| 2026 | 19 |

---

### 16. Combined older and newer processed datasets

In `data-preprocess/fix.ipynb`, I combined two processed datasets:

- `phivolcs_aggregated_final_list_fixed.csv`
- `Phivolcs_aggregated_final-new5only-fixed.csv`

The code used `pd.concat()` to stack the datasets, then sorted them by date in descending order.

This produced:

- `data-preprocess/Phivolcs_Master_Aggregated_Fixed.csv`

Then I added event IDs and produced:

- `data-preprocess/Phivolcs_Master_Aggregated_Fixed_With_IDs.csv`

Finally, the finished output appears as:

- `data-preprocess/Phivolcs_Master_Aggregated_Fixed_FinalFinished.csv`

---

### 17. Added stable event IDs

I added sequential PHIVOLCS-style event IDs to the master processed file.

The ID format is:

```text
PHV-0001
PHV-0002
PHV-0003
...
PHV-0771
```

Implementation evidence from `data-preprocess/fix.ipynb`:

```python
event_ids = ['PHV-' + str(i).zfill(4) for i in range(1, len(df_master) + 1)]
df_master.insert(0, 'event_id', event_ids)
```

This made each final earthquake event easier to reference, audit, and connect to future visualizations or database records.

---

### 18. Produced a final enriched dataset

The final finished dataset is:

- `data-preprocess/Phivolcs_Master_Aggregated_Fixed_FinalFinished.csv`

Final dataset details:

| Property | Value |
|---|---:|
| Rows | 771 |
| Columns | 18 |
| Unique event IDs | 771 |
| Duplicate full rows | 0 |
| Earliest date | 2010-03-25 |
| Latest date | 2026-02-15 |
| Unique locations | 226 |
| Unique cities | 209 |
| Unique provinces | 65 |
| Unique regions | 23 |

Final columns:

1. `event_id`
2. `date`
3. `time`
4. `latitude`
5. `longitude`
6. `depth_km`
7. `mag`
8. `coordinates`
9. `Location`
10. `loc_latitude`
11. `loc_longitude`
12. `city`
13. `province`
14. `region`
15. `distance_km`
16. `ns`
17. `angle_deg`
18. `ew`

---

### 19. Prepared special-report calculation materials

I also kept PHIVOLCS special-report calculation files in:

- `Phivolc-past data and processes/phivolcs_calculation-20260520T033535Z-3-001/phivolcs_calculation/`

These files document event-specific calculation work for major earthquake cases, including:

- 2017 Leyte / Ormoc earthquake
- 2019 Batanes / Itbayat earthquakes
- 2019 Central Luzon earthquake
- 2012 Negros Oriental earthquake
- 2017 Surigao del Norte earthquake

These calculation files appear to support the larger goal of comparing earthquake locations, reported intensities, place coordinates, and epicenter-related calculations.

---

## Data outputs created

### Raw and cleaned master data

- `PHIVOLCS_DATA/Master File/phivolcs_earthquakes.csv`
  - Full master earthquake catalog
  - 126,555 rows
- `PHIVOLCS_DATA/Master File/phivolcs_earthquakes_cleaned.csv`
  - Cleaned full catalog copy
  - 126,555 rows
- `PHIVOLCS_DATA/Final Data File/phivolcs_earthquakes_cleaned.csv`
  - Final cleaned full catalog copy
  - 126,555 rows

### Magnitude-filtered files

- `PHIVOLCS_DATA/Master File/phivolcs_earthquakes_5_0Abv.csv`
- `PHIVOLCS_DATA/Master File/phivolcs_earthquakes_5_0Abv_pt1.csv`
- `PHIVOLCS_DATA/Master File/phivolcs_earthquakes_5_0Abv_pt2.csv`
- `PHIVOLCS_DATA/Master File/phivolcs_earthquakes_5_0Abv_unique_locs.csv`
- `PHIVOLCS_DATA/Final Data File/phivolcs_earthquakes_5_0Abv (1).csv`
- `PHIVOLCS_DATA/Final Data File/phivolcs_earthquakes_5_0Abv_FULL_with_coords.csv`

### Enriched preprocessing outputs

- `data-preprocess/Phivolcs_aggregated.csv`
- `data-preprocess/Phivolcs_aggregated_final_list.csv`
- `data-preprocess/phivolcs_aggregated_final_list_fixed.csv`
- `data-preprocess/Phivolcs_aggregated_final-new5only.csv`
- `data-preprocess/Phivolcs_aggregated_final-new5only-fixed.csv`
- `data-preprocess/Phivolcs_Master_Aggregated_Fixed.csv`
- `data-preprocess/Phivolcs_Master_Aggregated_Fixed_With_IDs.csv`
- `data-preprocess/Phivolcs_Master_Aggregated_Fixed_FinalFinished.csv`

---

## Main technical skills demonstrated

### Data collection

- Web scraping PHIVOLCS earthquake pages
- Navigating inconsistent HTML table formats
- Extracting tabular records from legacy web pages
- Saving monthly and yearly CSV outputs

### Data cleaning

- Splitting combined text fields
- Handling inconsistent date/time formats
- Removing duplicate records where necessary
- Checking null values
- Standardizing column order
- Fixing special-case months manually when automated parsing was insufficient

### Data parsing

- Regex-based text parsing
- State-machine parsing for records spread across multiple lines
- Extracting distance, direction, and angle from PHIVOLCS relative-coordinate text
- Parsing location strings into city/province/region components

### Data enrichment

- Geocoding places using Nominatim through `geopy`
- Adding place latitude and longitude
- Mapping provinces to regions
- Adding unique event IDs

### Dataset preparation

- Creating monthly CSVs
- Creating yearly CSVs
- Creating full master datasets
- Creating magnitude-filtered datasets
- Creating final enriched datasets suitable for mapping, analysis, or database import

---

## Important data quality notes

The final dataset is already heavily cleaned and enriched, but the files still show some items worth noting for future review:

1. **Some old records have missing time values.**
   - This is visible mainly in older 2010–2014 records.

2. **Some rows still have incomplete coordinate fields.**
   - Example: older historical-style entries may have missing raw latitude/longitude or missing relative `coordinates` text.

3. **There are 31 final rows with at least one blank field.**
   - These are mostly older or special-case records where the source itself had incomplete details.

4. **One final row appears to have a suspicious magnitude value.**
   - `PHV-0670` has `mag = 28`, which likely needs manual verification because earthquake magnitudes should not be that high.

5. **Some region labels are not fully normalized.**
   - Example: similar regions may appear with slightly different wording, such as `Caraga (Region XIII)` and `Caraga Region (Region XIII)`.

6. **Some places are offshore or international/nearby regions.**
   - Example: Taiwan Region and Moro Gulf entries do not always map cleanly into a normal Philippine province/region structure.

These notes are not failures; they show where the source data or manual historical records need additional verification.

---

## Overall accomplishment

I created a full earthquake-data preparation and recalculation-support pipeline for PHIVOLCS data. The work started from raw PHIVOLCS web pages and older irregular records, then progressed into monthly CSVs, yearly aggregates, a full master catalog, a magnitude-5+ working subset, geocoded location data, parsed administrative location fields, region mapping, azimuth/distance parsing, and final event IDs. I also supported epicenter recalculation analysis by comparing true and estimated epicenters, documenting error distances, handling outliers, identifying impossible triangulation cases, and producing event-level reports and interactive maps.

The most complete output is the final enriched earthquake dataset:

```text
data-preprocess/Phivolcs_Master_Aggregated_Fixed_FinalFinished.csv
```

This file is ready to support later work such as:

- earthquake mapping
- filtering by year, province, or region
- magnitude-based analysis
- geographic visualization
- database import
- validation against special-report calculations
- future modeling or dashboard development

In short, I transformed scattered PHIVOLCS earthquake records into a structured, enriched, and analysis-ready dataset.
