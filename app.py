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
    csv_files = glob.glob(input_pattern)
    list_dfs = []
    for file in csv_files:
        df = pd.read_csv(file)
        list_dfs.append(df)
    
    all_data = pd.concat(list_dfs, ignore_index=True)
    filtered = all_data[all_data['product'].str.lower() == 'pink morsel']
    filtered['price'] = filtered['price'].replace({'\$':''}, regex=True).astype(float)
    filtered['sales'] = filtered['price'] * filtered['quantity']
    output_df = filtered[['sales', 'date', 'region']].rename(
        columns={'sales': 'Sales', 'date': 'Date', 'region': 'Region'}
    )
    output_df.to_csv(output_file, index=False)
    print("Processed data saved to", output_file)

# Process CSV files
process_csv_files(input_pattern='data/daily_sales_data_*.csv', output_file='formatted_output.csv')

# Load and prepare the processed data
df = pd.read_csv('formatted_output.csv')
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')

# Define inline CSS styles with a pink-dominated palette
container_style = {
    'fontFamily': 'Serif',
    'backgroundColor': '#FFE4E6',  # light pink background
    'padding': '20px'
}

header_style = {
    'color': '#F07D82',  # main pink color
    'textAlign': 'center',
    'fontSize': '3em',
    'marginBottom': '20px'
}

label_style = {
    'color': '#C94F6D',  # darker pink for labels
    'fontSize': '1.5em',
    'textAlign': 'center',
    'marginBottom': '10px'
}

radio_container_style = {
    'textAlign': 'center',
    'marginBottom': '20px'
}

radio_item_style = {
    'display': 'inline-block',
    'margin-right': '20px',
    'fontSize': '1.2em',
    'color': '#C94F6D'  # darker pink tone for radio items
}

graph_style = {
    'border': '2px solid #F7A1A8',  # pink border
    'boxShadow': '0px 4px 6px #C94F6D',  # darker pink shadow
    'margin': '0 auto',
    'maxWidth': '90%'
}

# Set up the Dash application
app = dash.Dash(__name__)

app.layout = html.Div(style=container_style, children=[
    html.H1("Sales Data Visualiser", style=header_style),
    
    html.Div(style=radio_container_style, children=[
        html.Label("Filter by Region:", style=label_style),
        dcc.RadioItems(
            id='region-radio',
            options=[
                {'label': 'north', 'value': 'north'},
                {'label': 'east', 'value': 'east'},
                {'label': 'south', 'value': 'south'},
                {'label': 'west', 'value': 'west'},
                {'label': 'all', 'value': 'all'}
            ],
            value='all',
            labelStyle=radio_item_style
        )
    ]),
    
    dcc.Graph(id='sales-line-chart', style=graph_style)
])

@app.callback(
    Output('sales-line-chart', 'figure'),
    Input('region-radio', 'value')
)
def update_graph(selected_region):
    """
    Callback that filters data by the selected region and creates a pink-colored line chart
    showing total sales over time.
    """
    if selected_region == 'all':
        filtered_df = df.copy()
        chart_title = "Total Sales Over Time (All Regions)"
    else:
        filtered_df = df[df['Region'] == selected_region]
        chart_title = f"Total Sales Over Time ({selected_region.capitalize()})"
    
    agg_df = filtered_df.groupby('Date', as_index=False)['Sales'].sum()
    
    fig = px.line(
        agg_df,
        x='Date',
        y='Sales',
        title=chart_title,
        labels={'Date': 'Date', 'Sales': 'Total Sales ($)'},
        color_discrete_sequence=['pink']  # pink-colored line
    )
    fig.update_layout(
        font_family="Serif",
        title_font_color="#F07D82",
        title_font_size=24,
        xaxis_title_font_color="#C94F6D",
        yaxis_title_font_color="#C94F6D"
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
