import pandas as pd
import os
import plotly.graph_objects as go

final_df = pd.read_csv('notyet_interactive_table.csv')

# Create a plotly table
fig = go.Figure(data=[go.Table(
    header=dict(
        values=list(final_df.columns),
        fill_color='rgba(0,0,0,0)',
        align='left',
        font=dict(color='black', size=14)
    ),
    cells=dict(
        values=[final_df[col] for col in final_df.columns],
        fill_color='rgba(0,0,0,0)',
        align='left',
        font=dict(color='black', size=12)
    )
)])

fig.update_layout(
    title="Country Travel and Safety Summary",
    width=1000,
    height=800,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

# Ensure output directory exists
os.makedirs('../../img', exist_ok=True)

# Save as HTML
fig.write_html("../../img/interactive_table.html", include_plotlyjs=True, full_html=True)
print("HTML file generated at img/interactive_table.html") 