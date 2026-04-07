import pandas as pd
from io import StringIO

# Load the file
file_path = 'Disney Doorables Codes Listing - Mega _ Specials.csv'
df = pd.read_csv(file_path, header=None)

flattened_data = []

# --- PART 1: THE ADVENT CALENDARS (Columns 0 to 11) ---
# Group 1: Cols 0-5 (Stitch and Jack)
# Group 2: Cols 6-11 (Mickey and Minnie)
advent_groups = {
    "2024 Advent Calendar (Stitch/Jack)": range(0, 6),
    "2024 Advent Calendar (Mickey/Minnie)": range(6, 12)
}

for group_name, col_range in advent_groups.items():
    for col in col_range:
        # Code is in Row 2 (Index 1)
        code = str(df.iloc[1, col]).strip()
        
        # Characters start at Row 3 (Index 2)
        for row in range(2, len(df)):
            entry = str(df.iloc[row, col]).strip()
            if entry and entry != 'nan' and len(entry) > 2:
                # Advent entries often look like "8: Boo" (Series: Character)
                if ":" in entry:
                    series, name = entry.split(":", 1)
                    char_series = f"Series {series.strip()}"
                    char_name = name.strip()
                else:
                    char_series = group_name
                    char_name = entry
                
                flattened_data.append({
                    'Category': 'Mega & Specials',
                    'Series': char_series,
                    'Character': char_name,
                    'Code': code,
                    'Rarity': 'Special'
                })

# --- PART 2: THE SIDE-BY-SIDE SERIES (Columns 15, 19, 23...) ---
# These are triplets: [Number, Character, Rarity]
series_starts = [15, 19, 23] # Start columns for Series 5, 9, 10

for start_col in series_starts:
    series_label = str(df.iloc[1, start_col]).strip() # e.g. "Series 5"
    
    for row in range(2, len(df)):
        number = str(df.iloc[row, start_col]).strip()
        name = str(df.iloc[row, start_col + 1]).strip()
        rarity = str(df.iloc[row, start_col + 2]).strip()
        
        if name and name != 'nan' and len(name) > 1:
            flattened_data.append({
                'Category': 'Mega & Specials',
                'Series': series_label,
                'Character': name,
                'Code': number, # Using number as code here
                'Rarity': rarity
            })

# Save to one clean file
output_df = pd.DataFrame(flattened_data)
output_df.to_csv('Mega_Specials_CLEAN.csv', index=False)
print("✅ Success! 'Mega_Specials_CLEAN.csv' created.")