import pandas as pd
import json

# Load your local directory
links_df = pd.read_csv('Disney Doorables Codes Listing.xlsx - Links.csv')

def build_master_list(df):
    master_hub = []
    
    # Iterate through your 30+ series
    for _, row in df.iterrows():
        name = str(row['Series Name']).strip()
        gid = str(row['GiD']).strip()
        
        if name != 'nan' and gid != 'nan':
            # Clean GID to ensure it's just numbers
            clean_gid = "".join(filter(str.isdigit, gid))
            
            entry = {
                "series_name": name,
                "category": "Disney Doorables",
                "live_data": f"https://docs.google.com/spreadsheets/d/12Fqu8DNKILAAM6sN1MSGGVKXSKyz52zkdzQtHDgHMco/export?format=csv&gid={clean_gid}",
                "wiki_link": f"https://disney-doorables.fandom.com/wiki/{name.replace(' ', '_')}",
                "cheatsheet": "PENDING_MEENYMINIMO" 
            }
            master_hub.append(entry)
            
    return master_hub

# Create the file
master_list = build_master_list(links_df)

# Save as your App's Brain
with open('doorables_master_hub.json', 'w') as f:
    json.dump(master_list, f, indent=4)

print(f"Success! Compiled {len(master_list)} series into doorables_master_hub.json")