from pathlib import Path
import pandas as pd


def load_and_prepare_data():
    """
    Load and preprocess the Canadian immigration data.
    Returns processed DataFrame or empty DataFrame if loading fails.
    """
    try:
        # Construct path relative to this file
        data_path = Path(__file__).parent.parent / 'Data' / \
            'canadian_immegration_data.csv'
        df = pd.read_csv(data_path)
        years = [str(year) for year in range(1980, 2014)]

        # Validate years in columns
        if not all(year in df.columns for year in years):
            raise ValueError(
                "Not all years are present in the DataFrame columns")

        # Calculate derived columns
        df['Total'] = df[years].sum(axis=1)
        df['Growth'] = ((df[years[-1]] - df[years[0]]) /
                        df[years[0]] * 100).round(1)
        df['Variance'] = df[years].var(axis=1)

        return df, years
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame(), []
