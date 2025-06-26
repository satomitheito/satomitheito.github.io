import pandas as pd
import numpy as np

df = pd.read_excel("../../data/raw/unwto-inbound-arrivals-data.xlsx", header=None)

# Find the first row with actual data (looking for "C." in the first column)
start_idx = df[df[0] == "C."].index[0]
df = df.iloc[start_idx:].reset_index(drop=True)

# Initialize empty lists to store data
countries = []
yearly_data = []

# Start from row 1 (after the header) and increment by 6
base_row_number = 1
max_rows = len(df)

while base_row_number < max_rows:
    # Get country name from Column D (index 3)
    country_name = df.iloc[base_row_number, 3]
    
    if pd.isna(country_name):
        base_row_number += 6
        continue
        
    # Get total arrivals data from row+2, columns L to AM (11 to 38)
    try:
        arrivals_row = df.iloc[base_row_number + 2, 11:39]  # Columns L to AM
        
        # Convert data to numeric, treating '..' as NA
        year_data = {}
        for year, value in zip(range(1995, 2023), arrivals_row):
            if pd.notna(value) and str(value).strip() != '..':
                try:
                    cleaned_value = str(value).replace(',', '')
                    # Multiply by 1000 and convert to integer
                    year_data[str(year)] = int(float(cleaned_value) * 1000)
                except (ValueError, TypeError):
                    year_data[str(year)] = np.nan
            else:
                year_data[str(year)] = np.nan
        
        # Add to our lists
        countries.append(country_name)
        yearly_data.append(year_data)
        
        print(f"Processed {country_name}")
    except IndexError:
        print(f"Reached end of data at row {base_row_number}")
        break
    
    # Increment base_row_number by 6
    base_row_number += 6

result_df = pd.DataFrame(yearly_data)
result_df.insert(0, 'Country', countries)

# Ensure columns are in correct order
year_cols = [str(year) for year in range(1995, 2023)]
result_df = result_df[['Country'] + year_cols]

# Convert all numeric columns to Int64 
for col in year_cols:
    result_df[col] = result_df[col].astype('Int64')

result_df.to_csv("../../data/processed/inbound_arrivals_processed.csv", index=False)