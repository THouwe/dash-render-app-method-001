import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np
import pandas as pd


app = dash.Dash(__name__)
server = app.server


df = pd.read_csv("results_df_method_001_trimmed.csv")
#df = pd.read_csv("results_df_method_001.csv")
#df.drop(columns = 'Unnamed: 0', inplace=True)
#df = df[df.n_samp > 50000]
#df = df[df.n_trades > 40]
#df.reset_index(inplace=True)
#duration = []
#[duration.append(str(pd.to_datetime(df.iloc[i].time_end) - pd.to_datetime(df.iloc[i].time_start))) for i in range(len(df))]
#for i in range(len(df)):
#    duration[i] = duration[i][:15]
#df['duration'] = duration

#colors = {
#    'text' : '#2F4F4F',
#    'plot_color' : '#C0C0C0',
#    'paper_color': '#DCDCDC'
#}
#col_seq = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']


price_labels = []
[price_labels.append(f"{df.price_X.iloc[i]} [{df.price_min.iloc[i]} {df.price_max.iloc[i]}], SD: {df.price_SD.iloc[i]}, SE: {np.round(df.price_SD.iloc[i]/np.sqrt(df.n_samp.iloc[i]),2)}") for i in range(len(df))]
pred_len_labels = []
[pred_len_labels.append(f"{df.pred_len_X.iloc[i]}, SD: {df.pred_len_SD.iloc[i]}, SE: {np.round(df.pred_len_SD.iloc[i]/np.sqrt(df.n_trades.iloc[i]),2)}") for i in range(len(df))]
trade_vol_labels = []
[trade_vol_labels.append(f"{np.round(df.tot_trade_vol_2[i],2)} FDUSD, {np.round(df.tot_trade_vol[i],5)} BTC") for i in range(len(df))]
trade_vol_h_labels = []
[trade_vol_h_labels.append(f"{np.round(df.trade_vol_h_2[i],2)} FDUSD, {np.round(df.trade_vol_h[i],5)} BTC") for i in range(len(df))]
spread_labels = []
[spread_labels.append(f"{np.round(df.spread_bp_X[i],3)} b.p., SD = {np.round(df.spread_bp_SD[i],3)}, SE = {np.round(df.spread_bp_SD[i]/np.sqrt(df.n_trades),3)}") for i in range(len(df))]

# Sample data for different sets of values
data_options = {
    'option1': {'categories': df.index, 'values': df.n_samp, 'labels': df.duration},
    'option2': {'categories': df.index, 'values': df.n_trades, 'labels': df.n_trades},
    'option3': {'categories': df.index, 'values': df.accuracy_tot, 'labels': np.round(df.accuracy_tot,2)},
    'option4': {'categories': df.index, 'values': df.PNL_glob, 'labels': np.round(df.PNL_glob,2)},
    'option5': {'categories': df.index, 'values': df.accuracy_1, 'labels': np.round(df.accuracy_1,2)},
    'option6': {'categories': df.index, 'values': df.accuracy_2, 'labels': np.round(df.accuracy_2,2)},
    'option7': {'categories': df.index, 'values': df.accuracy_3, 'labels': np.round(df.accuracy_3,2)},
    'option8': {'categories': df.index, 'values': df.price_X, 'labels': price_labels},
    'option9': {'categories': df.index, 'values': df.pred_len_X, 'labels': pred_len_labels},
    'option10': {'categories': df.index, 'values': df.tot_trade_vol_2, 'labels': trade_vol_labels},
    'option11': {'categories': df.index, 'values': df.trade_vol_h_2, 'labels': trade_vol_h_labels},
    'option12': {'categories': df.index, 'values': df.spread_bp_X, 'labels': spread_labels},
    'option13': {'categories': df.index, 'values': df.pred_on_time, 'labels': np.round(df.pred_on_time,2)},
}

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown-input',
        options=[
            {'label': 'Run Length', 'value': 'option1'},
            {'label': 'N. Trades', 'value': 'option2'},
            {'label': 'Accuracy', 'value': 'option3'},
            {'label': 'PNL', 'value': 'option4'},
            {'label': 'Accuracy Short Range', 'value': 'option5'},
            {'label': 'Accuracy Mid Range', 'value': 'option6'},
            {'label': 'Accuracy Long Range', 'value': 'option7'},
            {'label': 'BTC Price', 'value': 'option8'},
            {'label': 'Prediction Duration', 'value': 'option9'},
            {'label': 'Trade Volume', 'value': 'option10'},
            {'label': 'Trade Volume / h', 'value': 'option11'},
            {'label': 'Spread', 'value': 'option12'},
            {'label': 'Prediction ON Time', 'value': 'option13'},
        ],
        value='option1'
    ),
    dcc.Graph(id='bar-chart'),
])

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('dropdown-input', 'value')]
)

def update_bar_chart(selected_option):
    # Retrieve the data for the selected option
    selected_data = data_options[selected_option]

    # Create a bar chart using Plotly.graph_objects
    fig = go.Figure()

    # Add bars with labels using the selected data
    if selected_data['labels'] is not None:
        fig.add_trace(go.Bar(
            x=selected_data['categories'],
            y=selected_data['values'],
            text=selected_data['labels'],
            name='Bar Chart'
        ))
    else:
        fig.add_trace(go.Bar(
            x=selected_data['categories'],
            y=selected_data['values'],
            name='Bar Chart'
        ))

    # Customize x-axis and y-axis settings
    fig.update_xaxes(
        tickvals=list(range(len(df))),
        #ticktext=['First', 'Second', 'Third'],
        title_text='Run ID'
    )

    if selected_option == 'option1':
        fig.update_yaxes(
            title_text='Samples (~ sec)'
        )
        fig.update_layout(title='Run Length')
    elif selected_option == 'option2':
        fig.update_yaxes(
            title_text='Count'
        )
        fig.update_layout(title=f"N. Trades = {np.sum(df.n_trades)}")
    elif (selected_option=='option3') | (selected_option=='option4') | (selected_option=='option5') | (selected_option=='option6') | (selected_option=='option7'):
        fig.update_yaxes(
            title_text='%'
        )
        if selected_option=='option3':
            fig.update_layout(title=f"Accuracy Grand Mean = {np.round(np.sum(df.n_targ_tot) / np.sum(df.n_trades) * 100,2)} %")
        elif selected_option=='option4':
            fig.update_layout(title=f"Running PNL = {np.round(np.sum(df.PNL_glob),2)} %")
        elif selected_option=='option5':
            fig.update_layout(title=f"Accuracy Short Range: n. = {np.sum(df.n_targ_1)+np.sum(df.n_SL_1)}; mean = {np.round(np.sum(df.n_targ_1) / (np.sum(df.n_targ_1)+np.sum(df.n_SL_1)) * 100,2)} %")
        elif selected_option=='option6':
            fig.update_layout(title=f"Accuracy Mid Range: n. = {np.sum(df.n_targ_2)+np.sum(df.n_SL_2)}; mean = {np.round(np.sum(df.n_targ_2) / (np.sum(df.n_targ_2)+np.sum(df.n_SL_2)) * 100,2)} %")
        elif selected_option=='option7':
            fig.update_layout(title=f"Accuracy Long Range: n. = {np.sum(df.n_targ_3)+np.sum(df.n_SL_3)}; mean = {np.round(np.sum(df.n_targ_3) / (np.sum(df.n_targ_3)+np.sum(df.n_SL_3)) * 100,2)} %")
    elif selected_option == 'option8':
        fig.update_yaxes(
            #tickvals=[3500, 3600, 3700, 3800, 3900, 4000, 41000, 42000, 43000, 45000],
            title_text='FDUSD'
        )
        fig.update_layout(title="BTC Price")
    elif selected_option == 'option9':
        fig.update_yaxes(
            title_text='Samples (~ sec)'
        )
        fig.update_layout(title=f"Prediction Duration Mean of Means: {int(np.mean(df.pred_len_X))} sec. ({np.round(np.mean(df.pred_len_X)/60,2)} min.)")
    elif selected_option == 'option10':
        fig.update_yaxes(
            title_text='FDUSD'
        )
        fig.update_layout(title=f"Tot. Trade Volume = {int(np.sum(df.tot_trade_vol_2))} FDUSD ({np.round(np.sum(df.tot_trade_vol),5)} BTC)")
    elif selected_option == 'option11':
        fig.update_yaxes(
            title_text='FDUSD'
        )
        fig.update_layout(title=f"Tot. Trade Volume / h mean = {np.round(np.mean(df.trade_vol_h_2),2)} FDUSD ({np.round(np.mean(df.trade_vol_h),5)} BTC)")
    elif selected_option == 'option12':
        fig.update_yaxes(
            title_text='Basis Points (b.p.)'
        )
        fig.update_layout(title=f"Spread mean of means = {np.round(np.mean(df.spread_bp_X),3)} b.p.")
    elif selected_option == 'option13':
        fig.update_yaxes(
            title_text='%'
        )
        fig.update_layout(title=f"Prediction ON time mean of means = {np.round(np.mean(df.pred_on_time),2)} %")


    ## Save the chart as an HTML file
    #fig.write_html("results_method_001.html")

    return fig

if __name__ == '__main__':
    #app.run_server(debug=True, port=8052)
    app.run_server()
