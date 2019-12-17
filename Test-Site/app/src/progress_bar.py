from src.helpers import ct2ctts, find_near_time_row, segment
from plotly import graph_objs as go
from src.imports import *
from time import time
def get_progress_bar(df_pred, ctts, df_label_map):
    """
    Generate the progess bar figure
    Args:
        df_pred(pd.DataFrame) : Dataframe of predictions
        ctts(Datetime.Datetime): currentTime to show in timestmap
        df_label_map(pd.DataFrame) : a label map from code to name and color code
    Return : 
        fig(go.Figure) : a progress bar
    """


    fig = go.Figure()
    index, row = find_near_time_row(df_pred, ctts)
    logging.info(f"Progress-bar Current time: {ctts}, index : {index} ")
    if index is None : return fig
    df = df_pred.iloc[:index, :].copy()
    # segment to a dataframe of label to plot
    df_count = segment(df) # consider precompute this

    for i, row in df_count.iterrows():
        label_map = df_label_map[df_label_map.Code==row.Label]
        if len(label_map)<1:  raise "Can't find label"
        label_map = label_map.iloc[0]
        starttime = row.Starttime.strftime('%H:%M:%S')
        duration = (row.Endtime - row.Starttime).total_seconds()
        text = f"""Activity : {label_map.Label_name}<br />Confidence : {row.Prob}%<br />Start Time : {starttime}<br />Duration : {duration:.1f} seconds<br />"""


        duration = row['Endtime'] - row['Starttime']
        fig.add_trace(go.Bar(
            hovertext = text,
            y=[1],
            # because bar plot align at center => shift the start to the right half of the duration
            x = [row['Starttime']+duration/2],
            width = duration.total_seconds()*1000,
    #         name=label_map.Label_name,
            marker = dict(color=label_map.Color),
            showlegend=False,
    #         text='abc',textposition="outside"
            hoverinfo = 'text'
        ))


    fig.layout.update(
        showlegend=False,
        annotations=[
            go.layout.Annotation(
                x=row.Endtime,
                y=0,
                text = text, # the last text from the above iter will be this text
                bordercolor="#c7c7c7",
                borderwidth=2,
                borderpad=4,
                #bgcolor="#FFC312",
                bgcolor= label_map.Color,
                xref="x",
                yref="y",
                font = dict(color="white"),
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=50,
                align='left',
            )
        ],
        xaxis = go.layout.XAxis(
                range=[df_pred.Timestamp.iloc[0], df_pred.Timestamp.iloc[-1]], # change this to start and stop time of video not df_pred
                showgrid=False,
                side = 'top',
            ),
        yaxis = go.layout.YAxis(
            showticklabels = False,
            showgrid=False,
        ),
        margin=go.layout.Margin(
            l=100,
            r=100,
            b=0,
            t=0,
            pad=0
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=170,
    )
    return fig
