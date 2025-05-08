# data_lookup.py
import pandas as pd

# Load the Section Tally CSV (host version is already trimmed through 'Campus')
# Adjust the path if needed to where the CSV lives in your project.
df = pd.read_csv("Section_Tally.csv")

# As a safeguard, re-trim any extra columns past 'Campus'
if "Campus" in df.columns:
    campus_idx = df.columns.get_loc("Campus")
    df = df.iloc[:, :campus_idx+1]

# Expose a helper function or the DataFrame directly for imports

def get_section_dataframe() -> pd.DataFrame:
    """
    Returns the DataFrame containing section tally data, trimmed through the 'Campus' column.
    """
    return df
