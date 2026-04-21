import pandas as pd

def clean_munchlings():
    # 1. Load the raw file
    # This must be in 'C:\Users\noahv\Doorables_Hub_V2\Data_Compiler\cleaned sheets'
    file_path = 'Munchling Codes - Codes.csv'
    
    # Munchlings data starts on row 15 (skiprows=14)
    df = pd.read_csv(file_path, skiprows=14)

    # 2. Filter out empty rows
    df = df.dropna(subset=['Code'])

    # 3. Build the clean list
    flattened_data = []
    
    for _, row in df.iterrows():
        # Get the Disney Characters from columns 7 and 8
        char_a = str(row.iloc[7]).strip() if pd.notna(row.iloc[7]) else ""
        char_b = str(row.iloc[8]).strip() if pd.notna(row.iloc[8]) else ""
        
        if char_a and char_b:
            name = f"{char_a} & {char_b}"
        elif char_a:
            name = char_a
        else:
            name = str(row['Character 1']) 

        code = str(row['Code']).strip()
        series_num = str(row['Series']).strip()
        
        flattened_data.append({
            'Series': f"Munchlings S{series_num.split('.')[0]}",
            'Character': name,
            'Code': code,
            'Rarity': 'Common'
        })

    # 4. Save to the CURRENT folder (No paths allowed!)
    output_df = pd.DataFrame(flattened_data)
    output_df.to_csv('Munchlings_CLEAN.csv', index=False)
    
    print("✅ SUCCESS! 'Munchlings_CLEAN.csv' was created right here.")

if __name__ == "__main__":
    clean_munchlings()