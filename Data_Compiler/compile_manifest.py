import pandas as pd
import json
import os

# 1. The name of your file (Make sure this matches your folder exactly!)
input_file = 'Disney Doorables Codes Listing - Links.csv' 

def run_compiler():
    print("🚀 Starting the Doorables Master Compiler...")
    
    # 2. Try different encodings to solve the '0x90' or 'utf-8' errors
    df = None
    encodings_to_try = ['utf-8-sig', 'cp1252', 'latin1']
    
    for enc in encodings_to_try:
        try:
            df = pd.read_csv(input_file, encoding=enc)
            print(f"✅ Successfully read file using {enc} encoding.")
            break
        except Exception:
            continue

    if df is None:
        print("❌ Error: Could not read the file. Is it open in Excel? Close it and try again.")
        return

    # 3. Clean up the data and build the "Brain"
    master_hub = []
    
    # We look for 'Series Name' and 'GiD' columns based on your file
    for _, row in df.iterrows():
        name = str(row.get('Series Name', '')).strip()
        gid = str(row.get('GiD', '')).strip()
        
        if name and name != 'nan' and gid != 'nan':
            # Clean the GID (remove decimals like .0)
            clean_gid = "".join(filter(str.isdigit, gid))
            
            if clean_gid:
                entry = {
                    "series_name": name,
                    "id": name.lower().replace(" ", "_"),
                    "live_data_url": f"https://docs.google.com/spreadsheets/d/12Fqu8DNKILAAM6sN1MSGGVKXSKyz52zkdzQtHDgHMco/export?format=csv&gid={clean_gid}",
                    "wiki_url": f"https://disney-doorables.fandom.com/wiki/{name.replace(' ', '_')}",
                    "status": "active"
                }
                master_hub.append(entry)

    # 4. Save the Final JSON
    output_name = 'doorables_master_hub.json'
    with open(output_name, 'w', encoding='utf-8') as f:
        json.dump(master_hub, f, indent=4)
        
    print(f"🎉 SUCCESS! Created '{output_name}' with {len(master_hub)} series.")
    print("📍 You can now upload this file to GitHub for your app.")

if __name__ == "__main__":
    run_compiler()