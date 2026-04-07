import pandas as pd
import io

# Load the file you uploaded
file_path = 'Disney Doorables Codes Listing - Village Peeks.csv'
df = pd.read_csv(file_path, header=None)

flattened_data = []

# Scan the sheet for headers like "A 1", "A 2", etc.
for col in range(1, df.shape[1]):
    code = str(df.iloc[1, col]).strip() # Row 2 contains the codes
    
    # Check Row 3 for the Series number
    series_info = str(df.iloc[2, col]).strip()
    
    if "Series" in series_info:
        # Scan all rows below for character names
        for row in range(3, len(df)):
            char_name = str(df.iloc[row, col]).strip()
            if char_name and char_name != 'nan' and len(char_name) > 1:
                flattened_data.append({
                    'Series': series_info,
                    'Character': char_name,
                    'Code': code,
                    'Rarity': 'Common' # Default for Village Peeks
                })

# Save to a clean CSV
output_df = pd.DataFrame(flattened_data)
output_df.to_csv('Village_Peeks_CLEAN.csv', index=False)
print("✅ Done! 'Village_Peeks_CLEAN.csv' is ready for GitHub.")