[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.15031422.svg)](https://doi.org/10.5281/zenodo.15031422)



# Trade coalitions can curb tropical deforestation: the Forest Club – Code and data

This repository provides supplementary materials, data workflows, and scripts for the study:

Trade coalitions can curb tropical deforestation: the Forest Club
Etienne Berthet<sup>1,2,3,*</sup>, Ilaria Fusacchia<sup>4</sup>, Alessandro Antimiani<sup>5</sup>, Jennifer Morris<sup>1</sup>, and Alexis Laurent<sup>2,3</sup>

<sup>1</sup> MIT Center for Sustainability Science and Strategy, Massachusetts Institute of Technology; Cambridge, MA 02139, USA  
<sup>2</sup> Department of Environmental and Resource Engineering, Technical University of Denmark; Kongens Lyngby, 2800, Denmark  
<sup>3</sup> Center for Absolute Sustainability, Technical University of Denmark; Kongens Lyngby, 2800, Denmark  
<sup>4</sup> Department for Humanistic, Scientific, and Social Innovation, University of Basilicata; Potenza, 85100, Italy  
<sup>5</sup> Directorate-General for Trade, European Commission; Brussels, 1000, Belgium

*Corresponding author: etber@mit.edu


---

## Overview


This repository accompanies the manuscript’s Supplementary Materials and outlines the methodologies, data workflows, and computational steps used to:

1. **Quantify tropical deforestation** driven by agricultural production and trade (using HILDA+ and FAO data).  
2. **Compute consumption- and throughflow-based deforestation footprints** via a Multi-Regional Input-Output (MRIO) framework (GLORIA dataset).  
3. **Implement and assess** a Computable General Equilibrium (CGE) model (GTAP–AEZ) for **counterfactual “Forest Club” simulations**.

The aim of this README is to:
- Provide **system requirements** and software dependencies.  
- Give an **installation guide** (typical install times, version info).  
- Include a **demo** (small or simulated dataset) for quick tests.  
- Explain how to **run** the software with full data.  
- Summarize **reproduction steps** for main results.

---

## Project Directory Structure

```text
├── 1. Data
│   ├── 1. HILDA data
│   │   ├── 1. Extracting_ntcdf_data
│   │   ├── 2. Aggregating_data
│   │   └── 3. Split_AEZ
│   ├── 2. FAO data
│   │   └── 1. Production_Crops_Livestock_E_All_Data_(Normalized)
│   ├── 3. GTAPAEZ_Deforestation_coefficient
│   │   └── 1. GTAPAEZ_Data
│   ├── 4. Suitability
│   └── **README_DATA.md <-- Step 1**
│
├── 2. MRIO
│   ├── GLORIA
│   │   ├── commodity
│   │   ├── output
│   │   │   ├── CBA
│   │   │   └── TBA
│   │   └── (additional files)
│   ├── Visualizations
│   │   └── (additional files)
│   └── **README_MRIO.md <-- Step 2**
│
├── 3. CGE
│   ├── Game_Theory_2024
│   │   ├── 0_External_data
│   │   ├── 1_Code
│   │   ├── 2_Model.zip (experiment files, .prm parameter files, etc.)
│   │   ├── 3_Output
│   │   ├── 4_DB
│   │   └── 5_Visualisation
│   ├── 5. Tariff_SIM
│   └── **README_CGE.md <-- Step 3**
│
└── README.md  <-- You are here!
```

## Key Directories

- **`1. Data`**  
  Raw and processed input data:  
  - **HILDA+**: netCDFs, CSV extractions, and shapefiles.  
  - **FAO**: agro ecological zone/agricultural production/livestock production.

- **`2. MRIO`**   
  - Code to compute the CBA/TBA results within the MRIO GLORIA.

- **`3. CGE`**  
  CGE model files, parameter sets, and results for the Forest Club simulations.
---

## Getting Started

### 1. Clone or Download
Clone the repository directly onto your C:\ drive to avoid issues with file paths containing spaces. For example:
```text
cd C:\
git clone https://github.com/etiennebert/forest_club.git
```

Note: Do not install it under a path like C:\Users\YourName\Documents if that includes spaces (e.g., My Documents)—this can lead to inconsistent runs or file-not-found errors.

### 2. Software Requirements
- **Operating System:**  
  - Tested on **Windows 10** and **Windows 11** (64-bit).  
  - Other OS (Linux, macOS) untested; minor path adjustments may be needed.

- **Hardware Recommendations:**  
  - **16 GB RAM** or more for processing large datasets.  
  - No specialized GPU required. HPC resources recommended for very large runs.

- **Software Dependencies & Versions:**
  1. **Python 3.8+**  
     - Libraries: `xarray`, `numpy`, `pandas`, `scipy`, `netCDF4`  
     - Installation via `pip` or `conda`.  
  2. **R 4.0+**  
     - Package: `HARr` (for `.har` output parsing from GEMPACK).  
  3. **Alteryx Designer 2022.3** (optional)  
     - Required to run `.yxmd` workflows.  
  4. **GEMPACK Version 12.1** (with Fortran compiler)  
     - Runs the GTAP–AEZ model simulations.  
  5. **Tableau** (optional)  
     - For `.twb` visualization workbooks.

---

## Step 1: Data Preparation

Main Goals: 

1. **Extract HILDA+**  
   - Acquire **HILDA+ v2.1** data (`.nc` files).  
   - Python code `1_HILDA_code_extraction.py` to filter tropical regions of interest and relevant LULC codes.  
   - Convert to CSV or geographical format via Alteryx format for further analysis.

2. **Process FAO**  
   - Raw FAO files about production.  
   - `A_FAO_annual_evolution_per_GLORIA_sector.yxmd` (Alteryx) aggregates yearly incremental changes and smooths fluctuations.  
   - Merge with HILDA+ results to get sector-level deforestation intensities.

3. **Prepare the HILDA+ and FAO data processed**
   - Prepare the processed data for the MRIO GLORIA 

The various steps of this stage are detailed in the document **README_DATA.md <-- Step 1**

---

## Step 2: Running the MRIO analysis

1. **Consumption-Based Accounting (CBA)**  
   - `CBA_TBA_script.py` builds the Leontief inverse and multiplies by deforestation intensities and Final Demand.  
   - Outputs stored in `./2. MRIO/GLORIA/output/CBA`.

2. **Throughflow-Based Accounting (TBA)**  
   - Also handled by `CBA_TBA_script.py`, calculate the "throughflow" of deforestation for the different territories, using the Hypothetical Extraction Method.  
   - Results in `./2. MRIO/GLORIA/output/TBA`.

3. **Visualizations**  
   - Alteryx workflow `1_HILDA_v2-1_CBA results.yxmd` merges final CBA results.  
   - `CBA_Visualisation.twb` (Tableau) or other tools for charts and maps.

The different steps of this stage are detailed in the document **README_MRIO.md <-- Step 2**

---

## Step 3: GTAP–AEZ Counterfactual Analysis

1. **Deforestation coefficients**  
   - Represents the fraction of agricultural land expansion attributable to deforestation in each AEZ for each crop. It is used to guide land-use decisions in the CGE model (see SI 5.2 for additional details).
  
2. **Tariff Simulation**  
   - Find tariffs needed to reduce exports (or output) by the share of deforestation (See SI 6.1).  

3. **Forest Club Iterations**  
   - The game-theory logic is in `CGE_Game_Theory_GTAPAEZ.R`.
   - The R script runs with GEMPACK, then parse `.har` results with `HARr` in R.
   - Possibility to adjust the thresholds in `Thresholds_GTAPAEZ_Game_theory.xlsx` (See SI table S6)   
   - Each iteration re-runs the CGE with updated membership decisions and outputs new `.har` result files.

4. **Aggregating Results**  
   - Use Alteryx workflows `DB_GTAPAEZ_all.yxmd` and `DB_GTAPAEZ_aggregate.yxmd` to combine iteration-by-iteration data.  
   - Key outputs include:
     - `DB_GTAPAEZ_Forest_2024.csv` (forest area changes)
     - `DB_GTAPAEZ_EV_2024.csv` (welfare changes)
     - `DB_GTAPAEZ_all_results_2024_agg.csv` (aggregate iteration results).

The various steps of this stage are detailed in the document **README_CGE.md <-- Step 3**

---

## Reproduction Instructions

To replicate the **key figures and tables** from the manuscript:

1. **Download/Prepare Data** via Step 1.  
2. **Run MRIO** scripts (Step 2) to generate CBA/TBA results.  
3. **Run CGE** simulations (Step 3) for the Forest Club scenarios.  
4. **Visualize/Analyze** outcomes with Tableau or your preferred tools.  

*Note:* Large computations may require HPC time. Refer to the main text and SI for parameter settings, iteration details, and references.

---

## License

**Unless stated otherwise, this project is under the MIT License.**  

You may freely use, modify, and distribute this code under MIT terms.

> **Important:** HILDA+, FAO, GLORIA, GEMPACK, Alteryx, and GTAP data/tools each have **their own licenses**. Check their terms for any restrictions on commercial usage or redistribution.

---
## Contact

For questions, please contact the corresponding author: **etber@mit.edu**

Or open an issue on GitHub if you encounter any problems or have suggestions.

**Enjoy exploring the data and replicating our Forest Club analysis!**
