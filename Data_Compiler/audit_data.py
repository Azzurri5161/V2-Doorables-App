import pandas as pd
import requests
from io import StringIO
import time

FILE_NAME = 'Disney Doorables Codes Listing - Links.csv'

def run_audit():
    try:
        links_df = pd.read_csv(FILE_NAME)
    except FileNotFoundError:
        print(f"❌ Error: {FILE_NAME} not found.")
        return

    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # 1. THE BLACKLIST: If a row contains these, skip it immediately
    BLACKLIST = ['home', 'share your codes', 'welcome', 'navigation', 'click here']
    
    # 2. THE REQUIREMENTS: A real header MUST have a name and a code
    NAME_KEYS = ['character', 'figure', 'name']
    CODE_KEYS = ['code', 'no.', 'number']

    print("--- DOORABLES BLACKLISTED AUDIT ---")

    for index, row in links_df.iterrows():
        series_name = str(row['Series Name']).strip()
        raw_url = str(row['URL']).strip()
        gid = str(row['GiD']).strip()
        
        if series_name == 'nan' or 'docs.google.com' not in raw_url:
            continue

        clean_gid = gid.split('.')[0]
        base_url = raw_url.split('/pubhtml')[0]
        csv_url = f"{base_url}/pub?gid={clean_gid}&output=csv"
        
        try:
            print(f"⏳ Scanning {series_name}...")
            response = requests.get(csv_url, headers=headers, timeout=120)
            
            if response.status_code == 200:
                lines = response.text.split('\n')
                header_index = -1
                
                for i, line in enumerate(lines[:30]):
                    clean_line = line.lower()
                    
                    # Check the Blacklist first
                    if any(bad_word in clean_line for bad_word in BLACKLIST):
                        continue
                    
                    # Check for "Multi-Column" requirement (must have Name AND Code)
                    has_name = any(k in clean_line for k in NAME_KEYS)
                    has_code = any(k in clean_line for k in CODE_KEYS)
                    
                    if has_name and has_code:
                        header_index = i
                        break
                
                if header_index != -1:
                    # Read the CSV starting from the found row
                    df = pd.read_csv(StringIO(response.text), skiprows=header_index)
                    # Remove the 'Unnamed' columns caused by merged branding cells
                    clean_cols = [c for c in df.columns if 'Unnamed' not in str(c)]
                    
                    print(f"✅ Real Table Found at row {header_index + 1}!")
                    print(f"   Headers: {clean_cols}")
                else:
                    print(f"⚠️  Could not find a valid table (Skipped branding/junk).")
            else:
                print(f"⚠️  {series_name}: Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ {series_name}: Error -> {e}")
        
        print("-" * 30)
        time.sleep(1)

    print("\n--- AUDIT COMPLETE ---")

if __name__ == "__main__":
    run_audit()