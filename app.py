import pandas as pd
import glob
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

def process_csv_files(input_pattern='data/daily_sales_data_*.csv', output_file='formatted_output.csv'):
    """
    Reads all CSV files matching the given pattern, processes the data, and writes the output to a CSV.
    Processing includes:
      - Keeping only rows where the product is "pink morsel"
      - Removing the '$' from the price and converting it to float
      - Creating a 'Sales' field by multiplying price and quantity
      - Keeping only the Sales, Date, and Region fields in the output file
    """
    # Get all CSV file paths matching the pattern
    csv_files = glob.glob(input_pattern)
    
    # Read and collect data from all CSV files
    list_dfs = []
    for file in csv_files:
        df = pd.read_csv(file)
        list_dfs.append(df)
    
    # Combine all data into one DataFrame
    all_data = pd.concat(list_dfs, ignore_index=True)
    
    # Filter rows: keep only rows where the product is "pink morsel" (ignoring case)
    filtered = all_data[all_data['product'].str.lower() == 'pink morsel']
    
    # Clean the 'price' field: remove the "$" and convert to float
    filtered['price'] = filtered['price'].replace({'\$':''}, regex=True).astype(float)
    
    # Create the 'sales' column by multiplying price and quantity
    filtered['sales'] = filtered['price'] * filtered['quantity']
    
    # Create the final output DataFrame with only Sales, Date, and Region columns
    output_df = filtered[['sales', 'date', 'region']].rename(
        columns={'sales': 'Sales', 'date': 'Date', 'region': 'Region'}
    )
    
    # Write the processed data to the output CSV file
    output_df.to_csv(output_file, index=False)
    print("Processed data saved to", output_file)

# Process CSV files using the new file location
process_csv_files(input_pattern='data/daily_sales_data_*.csv', output_file='formatted_output.csv')

# Load the processed data for visualization
df = pd.read_csv('formatted_output.csv')

# Convert 'Date' column to datetime and sort by date
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

# Prepare the list of unique regions for the dropdown filter
regions = df['Region'].unique().tolist()
regions_options = [{'label': region, 'value': region} for region in regions]
regions_options.insert(0, {'label': 'All', 'value': 'All'})

# Set up the Dash application
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Sales Data Visualiser", style={'textAlign': 'center'}),
    html.Label("Select Region:"),
    dcc.Dropdown(
        id='region-dropdown',
        options=regions_options,
        value='All'
    ),
    dcc.Graph(id='sales-line-chart')
])

@app.callback(
    Output('sales-line-chart', 'figure'),
    Input('region-dropdown', 'value')
)
def update_graph(selected_region):
    """
    Callback that filters the data by the selected region (if any),
    aggregates sales by date, and returns a line chart with a pink-colored line.
    """
    if selected_region == 'All':
        filtered_df = df.copy()
    else:
        filtered_df = df[df['Region'] == selected_region]
    
    # Aggregate total sales by date
    agg_df = filtered_df.groupby('Date', as_index=False)['Sales'].sum()
    
    # Create a line chart with the line colored pink
    fig = px.line(
        agg_df, 
        x='Date', 
        y='Sales',
        title=f"Total Sales over Time for {selected_region}",
        labels={'Date': 'Date', 'Sales': 'Total Sales ($)'},
        color_discrete_sequence=['pink']  # sets the line color to pink
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
