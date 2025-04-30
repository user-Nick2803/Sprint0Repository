# data_lookup.py
import pandas as pd

# Load the CSV file
df = pd.read_csv("Section_Tally.csv")

# If the CSV contains a column named "Campus", ignore any columns to the right of it.
if "Campus" in df.columns:
    campus_idx = df.columns.get_loc("Campus")
    df = df.iloc[:, :campus_idx+1]

def lookup_section_tally(query: str) -> str:
    """
    Searches the entire DataFrame for cells matching the query string (case-insensitive).
    Returns a CSV excerpt of the matching rows if any are found, or a summary message otherwise.
    """
    # Create a boolean mask that checks every cell in each row.
    mask = df.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1)
    matches = df[mask]
    
    if not matches.empty:
        # Return the matching rows as a CSV-formatted string.
        return matches.to_csv(index=False).strip()
    
    # If no matches are found, return a brief descriptive message.
    return (
        "No direct matches were found for your query in the Section Tally data. "
        "This dataset includes details on courses, class times, professors, and campus locations. "
        "Please try a different keyword or a more specific query."
    )
