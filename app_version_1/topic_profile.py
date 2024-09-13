import pandas as pd
import altair as alt

def topic_distribution(topic_summary_df):
    base = alt.Chart(topic_summary_df).encode(
        alt.Theta("paper_numbers:Q").stack(True),
        alt.Radius("paper_numbers").scale(type="sqrt", zero=True, rangeMin=20),
        color=alt.Color("index:N", legend=alt.Legend(
            title="Topic",  # Title for the legend
            orient="right",  # Position the legend on the right side
            columns=1,       # Show legend in two columns
            titleFontSize=24, # Customize title font size
            labelFontSize=20  # Customize label font size
        )),
        tooltip=[alt.Tooltip('index:N', title='Topic')]
    ).properties(
        width=600, height=600
    )

    c1 = base.mark_arc(innerRadius=20, stroke="#fff").encode()

    return c1