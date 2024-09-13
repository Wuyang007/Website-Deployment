import pandas as pd
import altair as alt
import numpy as np
import ast

def draw_time_series_plot(topic):
    df = pd.read_csv('../datasets/for_topic_along_time.csv')
    df['publish_date'] = pd.to_datetime(df['publish_date'])
    df['year_month'] = df['publish_date'].dt.to_period('M')
    df['year_month'] = df['year_month'].dt.to_timestamp()

    topic_distribution_df = pd.read_csv('../datasets/topic_distribution.csv')
    topic_distribution_df = topic_distribution_df.set_index('index')

    def convert_to_list(str_list):
        try:
            return ast.literal_eval(str_list)
        except (SyntaxError, ValueError):
            return []
    
    topic_PMID_list = convert_to_list(topic_distribution_df.loc[topic, 'contents'])

    topic_df = df[df['PMID'].isin(topic_PMID_list)]
    topic_time_df = topic_df.groupby('year_month').agg({'PMID':'count'}).reset_index()
    topic_time_df = topic_time_df[topic_time_df['year_month']<'2024-01-01']

    topic_chart =alt.Chart(topic_time_df).mark_line(color='steelblue').encode(
        x=alt.X('year_month:T', title=''),
        y=alt.Y('PMID:Q', title='Publications per Month'),
    ).properties(width=800, height=150).configure_axis(
        grid=False,  # Turn off grid lines for cleaner look
        labelFontSize=10
    )



    return topic_chart