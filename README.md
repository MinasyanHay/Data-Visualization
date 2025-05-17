# Canadian Immigration Dashboard

An interactive dashboard for visualizing Canadian immigration patterns from 1980 to 2013.

## Features

- Interactive choropleth map visualization
- Multiple visualization metrics (Total, Growth Rate, Year-over-Year Change)
- Region-based filtering
- Statistical insights and top contributing countries
- Dark/Light mode support

## Project Structure

```
.
├── app.py                  # Main application file
├── pages/                  # Dashboard components
│   ├── maps.py            # Map visualization
│   ├── analysis.py        # Analysis page
│   ├── home.py            # Home page
│   └── data_manager.py    # Data handling
├── Data/                   # Data directory
│   └── canadian_immegration_data.csv  # Immigration dataset
└── requirements.txt        # Python dependencies
```

## Setup Instructions

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://127.0.0.1:8050/
   ```

## Data Source
The dashboard uses Canadian immigration data from 1980 to 2013, tracking immigration patterns from various countries worldwide.

## Requirements
- Python 3.8+
- Dependencies listed in requirements.txt 