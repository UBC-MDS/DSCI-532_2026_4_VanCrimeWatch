import pandas as pd
import pytest
import sys
from pathlib import Path

# Add src to path to import helper function for testing
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.helpers import filter_crime_data

@pytest.fixture
def sample_crime_df():
    return pd.DataFrame({
        "YEAR": [2023, 2024, 2025],
        "TYPE": ["Mischief", "Other Theft", "Break and Enter Commercial"],
        "NEIGHBOURHOOD": ["West End", "Central Business District", "Kitsilano"]
    })

def test_filter_empty_years_boundary(sample_crime_df):
    """Providing an empty list for years returns an empty dataframe."""
    result = filter_crime_data(
        df=sample_crime_df, 
        years=[], # empty years
        crimes=["Mischief"], 
        neighbourhoods=["West End"]
    )
    
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0
    assert result.columns.tolist() == sample_crime_df.columns.tolist()

def test_filter_valid_conditions(sample_crime_df):
    """Filtering by valid year and crime type returns the correct intersecting rows."""
    result = filter_crime_data(
        df=sample_crime_df,
        years=["2023", "2024"],
        crimes=["Mischief"],
        neighbourhoods=[]
    )
    
    assert len(result) == 1
    assert result.iloc[0]["YEAR"] == 2023
    assert result.iloc[0]["TYPE"] == "Mischief"