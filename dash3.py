import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc  # Import Bootstrap components

# Load dataset
df = pd.read_csv('https://raw.githubusercontent.com/chriszapp/datasets/main/books.csv', on_bad_lines='skip')
top_10_books = df.head(10)

# Initial figure
initial_fig = px.bar(
    top_10_books,
    y='title',
    x='  num_pages',
    title='Top 10 Books - Number of pages per title',
    orientation='h',
    labels={'  num_pages': 'Number of Pages'},
    height=600,
    width=1200
)

initial_fig.update_traces(marker_color='#fcba6f')

initial_fig.update_layout(
    font_color='rgba(255, 255, 255, 0.9)',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis_title='',
    margin=dict(pad=25)
)

# Initializing app
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = html.Div(
    style={
        'background-image': 'url("/assets/background.jpg")',
        'background-size': 'cover',
        'background-position': 'center',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
        'padding': '0 150px',
        'color': 'rgba(255, 255, 255, 0.9)',
    },
    children=[
        html.Img(src=app.get_asset_url('Resource-Page-Books-banner.png'), style={'width': '100%', 'max-width': '1300px'}),
        html.H1("Top 10 Books", style={'text-align': 'center', 'font-size': '36px', 'font-family': 'system-ui', 'margin': '80px'}),
        dcc.Graph(figure=initial_fig, id='book-graph', style={'background-color': 'transparent', 'margin-bottom': '30px'}),

        html.H1("Select your author/ number of pages", style={'text-align': 'center', 'font-size': '36px', 'font-family': 'system-ui', 'margin': '80px'}),
        html.Label("Select an author:", style={'font-family': 'system-ui', 'margin-top': '50px', 'margin-bottom': '10px'}),
        dcc.Dropdown(
            id='author-dropdown',
            options=[{'label': author, 'value': author} for author in df['authors'].unique()],
            multi=True,
            style={'color': '#2a2a2b'}
        ),
        html.Label("Enter a maximum number of pages:", style={'font-family': 'system-ui', 'margin-top': '10px', 'margin-bottom': '10px'}),
        dcc.Input(
            id='max-pages-input',
            type='number',
            value=df['  num_pages'].max()
        ),
        dbc.Button('Update Graph', id='update-button', n_clicks=0, color='primary', className='mb-3'),

        html.Div(id='book-graph-container', style={'display': 'none', 'margin-bottom': '80px'}),

        # Bootstrap 
        dbc.Card(
            dbc.CardBody([
                html.H4("Selected Books", className="card-title"),
                html.Div(id='selected-books-info'),
            ]),
            style={'width': '18rem', 'margin': 'auto'}
        ),
    ]
)

# Callback 

@app.callback(
    [Output('book-graph-container', 'children'),
     Output('book-graph-container', 'style'),
     Output('selected-books-info', 'children')], 
    [Input('update-button', 'n_clicks')],
    [State('author-dropdown', 'value'),
     State('max-pages-input', 'value')]
)
def update_graph(n_clicks, selected_author, max_pages):
    if n_clicks > 0:
        filtered_df = df.copy()
        if selected_author:
            filtered_df = filtered_df[filtered_df['authors'].isin(selected_author)]
        filtered_df = filtered_df[filtered_df['  num_pages'] <= max_pages]

        updated_fig = px.bar(
            filtered_df,
            y='title',
            x='  num_pages',
            title='Book by author and number of pages',
            orientation='h',
            labels={'  num_pages': 'Number of Pages'},
            height=600,
            width=1200
        )
        updated_fig.update_traces(marker_color='#fcba6f')
        updated_fig.update_layout(
            font_color='rgba(255, 255, 255, 0.9)',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis_title='',
            margin=dict(pad=85)
        )

        selected_books_info = html.Div([
            html.P(f"Selected Author(s): {', '.join(selected_author) if selected_author else 'All Authors'}"),
            html.P(f"Maximum Pages: {max_pages}"),
        ])

        return [dcc.Graph(figure=updated_fig, id='book-graph')], {'display': 'block'}, selected_books_info

    return [], {'display': 'none'}, None

if __name__ == '__main__':
    app.run_server(debug=True)
