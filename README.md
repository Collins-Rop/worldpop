# WorldPop Dashboard

Interactive dashboard for exploring age and sex structured population data for Kenya and Uganda using WorldPop 2025 projections.

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone git@github.com:Collins-Rop/worldpop.git
cd worldpop
```

2. Install dependencies:
```bash
pip install -r requirements.txt --break-system-packages
```

### Running the Pipeline

1. Process the WorldPop data:
```bash
python src/pipeline.py
```

This will:
- Download WorldPop 2025 raster data for Kenya and Uganda
- Extract population totals by country, age group, and sex
- Cache processed data in `data/processed_population.parquet`
- Display summary statistics

**Expected runtime:** 10-20 minutes (depending on network speed)

2. Launch the dashboard:
```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Features

### Interactive Filters
- **Country Selection:** Kenya, Uganda, or both
- **Age Group Selection:** Filter by specific age ranges (0-4 through 80+)
- **Sex Selection:** Male, Female, or both

### Visualizations
- **Population Pyramids:** Classic demographic visualization showing age-sex structure
- **Age Distribution:** Bar chart of population by age group
- **Sex Comparison:** Side-by-side comparison of male/female populations
- **Health Indicators:** Key metrics for public health planning


## Approach Summary

The pipeline uses a modular design that:

1. **Downloads data programmatically** from WorldPop servers using structured URLs
2. **Processes rasters efficiently** using rasterio to extract population totals
3. **Caches results** to avoid re-downloading (parquet format for fast loading)
4. **Provides interactive exploration** via Streamlit with real-time filtering

The dashboard emphasizes **public health context**, highlighting age structures that inform:
- Service planning (maternal health, immunization, elderly care)
- Resource allocation for health systems
- Outbreak response capacity

## AI Tool Usage

In accordance with project transparency guidelines, the following AI-assisted contributions were made:

Documentation: The initial draft and core content of this README.md file were generated using an AI tool (GitHub Copilot) to improve documentation efficiency and save on elapsing time.

Syntax and Compliance: I used AI-based chat assistance to verify dependency versions in requirements.txt (equivalent to pip freeze), troubleshoot data processing logic, and correct syntax errors in data structure implementations.
        Example: Update versioning of requirements.txt packages

I reviewed, tested, and modified AI-generated code to ensure correctness, efficiency, and alignment with the assessment requirements.

