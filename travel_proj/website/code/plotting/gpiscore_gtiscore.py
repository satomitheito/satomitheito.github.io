import pandas as pd
import os
import re
import plotly.express as px
import numpy as np

img_dir = "../../../website_edited/img"
os.makedirs(img_dir, exist_ok=True)

travel_advisories = pd.read_csv("../../../data/processed/Travel_Advisories_Processed.csv")
protest_data = pd.read_csv("../../../data/processed/Global_Protest_Processed.csv")
gpi_data = pd.read_csv("../../../data/processed/Global_Peace_Index_Processed.csv")
gti_data = pd.read_csv("../../../data/processed/Global_Terrorism_Index_Processed.csv")

# Print dataset info
print(f"Travel Advisories: {len(travel_advisories)} rows")
print(f"GPI Data: {len(gpi_data)} rows")
print(f"GTI Data: {len(gti_data)} rows")

# Print column names
print("\nGPI columns:", gpi_data.columns.tolist())
print("GTI columns:", gti_data.columns.tolist())

# Get the most recent GPI scores
# Find the latest year column in the GPI data (format: '2024_Score')
gpi_year_columns = [col for col in gpi_data.columns if re.match(r'\d{4}_Score', col)]
gpi_latest_year_col = sorted(gpi_year_columns)[-1]  # Get the most recent year column
gpi_latest_year = gpi_latest_year_col.split('_')[0]
print(f"\nLatest GPI year column: {gpi_latest_year_col} (Year: {gpi_latest_year})")

# Select only country and the latest score column
latest_gpi = gpi_data[['country', gpi_latest_year_col]].copy()
latest_gpi = latest_gpi.rename(columns={'country': 'Country', gpi_latest_year_col: 'GPI_Score'})

# Get the most recent GTI scores
# Find the latest year column in the GTI data (format: '2024 score')
gti_year_columns = [col for col in gti_data.columns if re.match(r'\d{4} score', col)]
gti_latest_year_col = sorted(gti_year_columns)[-1]  # Get the most recent year column
gti_latest_year = gti_latest_year_col.split(' ')[0]
print(f"Latest GTI year column: {gti_latest_year_col} (Year: {gti_latest_year})")

# Select only country and the latest score column
latest_gti = gti_data[['country', gti_latest_year_col]].copy()
latest_gti = latest_gti.rename(columns={'country': 'Country', gti_latest_year_col: 'GTI_Score'})

print("\nSample countries in Travel Advisories:")
print(travel_advisories['Country'].sample(5).tolist())
print("\nSample countries in GPI data:")
print(latest_gpi['Country'].sample(5).tolist())
print("\nSample countries in GTI data:")
print(latest_gti['Country'].sample(5).tolist())

# Merge the travel advisories with the GPI scores
travel_with_gpi = pd.merge(
    travel_advisories,
    latest_gpi,
    on='Country',
    how='left'
)

# Merge the result with the GTI scores
travel_with_indices = pd.merge(
    travel_with_gpi,
    latest_gti,
    on='Country',
    how='left'
)

# Count how many countries we could match with scores
gpi_matched = travel_with_indices['GPI_Score'].notna().sum()
gti_matched = travel_with_indices['GTI_Score'].notna().sum()
total_countries = len(travel_with_indices)

print(f"\nMatched {gpi_matched}/{total_countries} countries with GPI scores")
print(f"Matched {gti_matched}/{total_countries} countries with GTI scores")

# Check for any countries that didn't match
print("\nSample countries that didn't match with GPI scores:")
print(travel_with_indices[travel_with_indices['GPI_Score'].isna()]['Country'].sample(min(5, travel_with_indices['GPI_Score'].isna().sum())).tolist())

print("\nSample countries that didn't match with GTI scores:")
print(travel_with_indices[travel_with_indices['GTI_Score'].isna()]['Country'].sample(min(5, travel_with_indices['GTI_Score'].isna().sum())).tolist())

# Remove countries that don't have either a GPI score or a GTI score
complete_indices = travel_with_indices.dropna(subset=['GPI_Score', 'GTI_Score'])
removed_count = len(travel_with_indices) - len(complete_indices)
print(f"\nRemoved {removed_count} countries with missing GPI or GTI scores")
print(f"Remaining countries: {len(complete_indices)}")

# Print some of the removed countries
if removed_count > 0:
    missing_countries = set(travel_with_indices['Country']) - set(complete_indices['Country'])
    print(f"Sample of removed countries (missing scores): {list(missing_countries)[:5]}")

# Check for NaN values in the Advisory Level Number
nan_advisory = complete_indices['Advisory Level Number'].isna().sum()
print(f"\nFound {nan_advisory} rows with NaN in Advisory Level Number")

# Fill any NaN in Advisory Level Number with a default value (1)
if nan_advisory > 0:
    print("Filling NaN advisory levels with default value 1")
    complete_indices['Advisory Level Number'] = complete_indices['Advisory Level Number'].fillna(1.0)

# Save the merged dataset with only complete records
output_dir = "../../../data/processed"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "Travel_Advisories_With_Indices.csv")
complete_indices.to_csv(output_path, index=False)

print(f"\nSaved filtered dataset to {output_path}")

# Print a few rows of the final dataset to verify
print("\nSample of final dataset (all have GPI and GTI scores):")
print(complete_indices.sample(5)[['Country', 'Advisory Level Number', 'GPI_Score', 'GTI_Score']].to_string())

# Create color mapping for advisory levels
# Using the website's color scheme
color_map = {
    1: "#9be7c4",  # Level 1: Exercise Normal Precautions - Light Green
    2: "#ffe082",  # Level 2: Exercise Increased Caution - Yellow
    3: "#ffa600",  # Level 3: Reconsider Travel - Orange
    4: "#ff0000"   # Level 4: Do Not Travel - Red
}

# Convert Advisory Level Number to integers for proper coloring
# First ensure all values are proper numbers and not NaN
complete_indices['Advisory Level Number'] = complete_indices['Advisory Level Number'].fillna(1.0)
complete_indices['Advisory Level Number'] = complete_indices['Advisory Level Number'].astype(int)

# Create a new column for the color based on advisory level
complete_indices['Color'] = complete_indices['Advisory Level Number'].map(color_map)

# Create a human-readable label for the legend
complete_indices['Advisory Level'] = complete_indices['Advisory Level Number'].map({
    1: "Level 1: Exercise Normal Precautions",
    2: "Level 2: Exercise Increased Caution",
    3: "Level 3: Reconsider Travel",
    4: "Level 4: Do Not Travel"
})


print("\nCreating combined GPI and GTI scatter plot...")

# Calculate statistics for GPI scores
gpi_median = complete_indices['GPI_Score'].median()
gpi_q1 = complete_indices['GPI_Score'].quantile(0.25)  # 1st quartile
gpi_q3 = complete_indices['GPI_Score'].quantile(0.75)  # 3rd quartile

# Calculate statistics for GTI scores
gti_median = complete_indices['GTI_Score'].median()
gti_q1 = complete_indices['GTI_Score'].quantile(0.25)  # 1st quartile
gti_q3 = complete_indices['GTI_Score'].quantile(0.75)  # 3rd quartile

print(f"\nGPI Score Statistics:")
print(f"Q1 (25th percentile): {gpi_q1:.2f}")
print(f"Median (50th percentile): {gpi_median:.2f}")
print(f"Q3 (75th percentile): {gpi_q3:.2f}")

print(f"\nGTI Score Statistics:")
print(f"Q1 (25th percentile): {gti_q1:.2f}")
print(f"Median (50th percentile): {gti_median:.2f}")
print(f"Q3 (75th percentile): {gti_q3:.2f}")

# Create the scatter plot
fig = px.scatter(
    complete_indices,
    x='GPI_Score',
    y='GTI_Score',
    color='Advisory Level',
    color_discrete_map={
        "Level 1: Exercise Normal Precautions": "#9be7c4",
        "Level 2: Exercise Increased Caution": "#ffe082",
        "Level 3: Reconsider Travel": "#ffa600",
        "Level 4: Do Not Travel": "#ff0000"
    },
    hover_name='Country',
    title=f'Global Peace Index Score vs Global Terrorism Index Score by Travel Advisory Level ({gpi_latest_year}/{gti_latest_year})',
    labels={
        'GPI_Score': f'Global Peace Index Score ({gpi_latest_year})',
        'GTI_Score': f'Global Terrorism Index Score ({gti_latest_year})'
    }
)

# Customize the layout
fig.update_traces(
    marker=dict(size=15, opacity=1.0, line=dict(width=1.5, color='white')),
    hovertemplate='<b>%{hovertext}</b><br>GPI Score: %{x:.2f}<br>GTI Score: %{y:.2f}<extra></extra>'
)

# Add vertical lines for GPI Q1, median, and Q3
fig.add_vline(x=gpi_q1, line_dash="dash", line_color="rgba(65, 105, 225, 0.5)", 
              annotation_text=f"Q1: {gpi_q1:.2f}", annotation_position="top")
fig.add_vline(x=gpi_median, line_dash="dash", line_color="rgba(65, 105, 225, 1.0)", 
              annotation_text=f"Median: {gpi_median:.2f}", annotation_position="top")
fig.add_vline(x=gpi_q3, line_dash="dash", line_color="rgba(65, 105, 225, 0.5)", 
              annotation_text=f"Q3: {gpi_q3:.2f}", annotation_position="top")

# Add horizontal lines for GTI Q1, median, and Q3
fig.add_hline(y=gti_q1, line_dash="dash", line_color="rgba(148, 0, 211, 0.5)", 
              annotation_text=f"Q1: {gti_q1:.2f}", annotation_position="right")
fig.add_hline(y=gti_median, line_dash="dash", line_color="rgba(148, 0, 211, 1.0)", 
              annotation_text=f"Median: {gti_median:.2f}", annotation_position="right")
fig.add_hline(y=gti_q3, line_dash="dash", line_color="rgba(148, 0, 211, 0.5)", 
              annotation_text=f"Q3: {gti_q3:.2f}", annotation_position="right")

# Set axes to start from 0
fig.update_layout(
    height=700,
    width=1000,
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
    hovermode='closest',
    font=dict(family="Arial", size=12),
    xaxis=dict(
        title=dict(
            text=f'Global Peace Index Score ({gpi_latest_year})', 
            font=dict(color="rgba(65, 105, 225, 1.0)")
        ),
        gridcolor='lightgray',
        range=[1.0, max(complete_indices['GPI_Score']) * 1.05]  # Start from 1.0, extend slightly beyond max
    ),
    yaxis=dict(
        title=dict(
            text=f'Global Terrorism Index Score ({gti_latest_year})',
            font=dict(color="rgba(148, 0, 211, 1.0)")
        ),
        gridcolor='lightgray',
        range=[-0.2, max(complete_indices['GTI_Score']) * 1.05]  # Start slightly below 0 to make bottom points more visible
    ),
    legend=dict(
        title="",  # Remove the "Travel Advisory" title
        orientation='h',  # Horizontal layout
        yanchor='top',
        y=-0.15,  # Position below the plot
        xanchor='center',
        x=0.5,
        bgcolor='rgba(255,255,255,0.8)'
    ),
    margin=dict(b=100)  # Add bottom margin to make space for the legend
)

html_path = os.path.join(img_dir, 'combined_gpi_gti_by_advisory.html')
fig.write_html(html_path)
print(f"Saved interactive combined scatter plot to {html_path}")