

import altair as alt


def draw_university_profile(university_df):
    # Define a single selection that applies to both charts
    highlight = alt.selection_point(fields=['university_name'])

    # Tooltip for detailed information
    tooltip=[alt.Tooltip('university_name:N', title='University'),
            alt.Tooltip('community size (tenure track):Q', title='Faculty Community Size'),
            alt.Tooltip('average impact factor:Q', title='Average Impact Factors', format='.2f')]

    # Community Size plot with tooltip and cross-chart selection
    community_size = alt.Chart(university_df).mark_bar().encode(
        x=alt.X('university_name', sort='-y', axis=None),
        y=alt.Y('community size (tenure track)', title='Community Size'),
        color=alt.condition(highlight, alt.value('#4a6fa9'), alt.value('lightgray')),  # Highlight selected bar
        opacity=alt.condition(highlight, alt.value(1), alt.value(0.3)),  # Fade unselected bars
        tooltip=tooltip
    ).add_params(
        highlight  # Add interactive selection using add_params
    ).properties(width=800, height=100)

    # Impact Factor plot with tooltip and cross-chart selection
    impact_factor = alt.Chart(university_df).mark_bar().encode(
        x=alt.X('university_name', sort='-y', title=''),
        y=alt.Y('average impact factor', scale=alt.Scale(domain=[0, 13]), title='Average Impact Factor', ),
        color=alt.condition(highlight, alt.value('#f28f8a'), alt.value('lightgray')),  # Highlight selected bar
        opacity=alt.condition(highlight, alt.value(1), alt.value(0.3)),  # Fade unselected bars
        tooltip=tooltip
    ).add_params(
        highlight  # Add interactive selection using add_params
    ).properties(width=800, height=100)

    # Combine both charts vertically
    chart = (community_size & impact_factor).configure_legend(
        title=None,  # Remove legend title for a cleaner look
        symbolType='circle',  # Change the legend symbol to circles for a modern feel
        symbolSize=150,  # Make the legend symbols bigger
        orient='bottom',  # Place legend at the bottom
        columns=5,
    ).configure_view(
        strokeWidth=0  # Remove borders for a cleaner appearance
    ).configure_axis(
        grid=False,  # Remove gridlines to simplify the design
        domain=False  # Remove axis lines for a more minimalistic look
    ).configure_scale(
        bandPaddingInner=0.3,  # Add some spacing between bars for readability
        bandPaddingOuter=0.2
    )

    return chart



