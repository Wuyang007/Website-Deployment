import altair as alt
import pandas as pd
from fuzzywuzzy import process
import pandas as pd
import plotly.graph_objects as go

def create_base_chart(df):
    base_chart = alt.Chart(df).mark_circle(size=25).encode(
        x=alt.X('num_of_pub', title='Number of publications per year'),
        #y='ave_if',
        y=alt.Y('ave_if', scale=alt.Scale(type='log', domain=[0.5, 100]), title='Average impact factor'),
        color=alt.Color('Community Contribution:N',scale=alt.Scale(scheme='tableau10'),legend=alt.Legend(orient='top', direction='horizontal')),
        tooltip=[alt.Tooltip('university_name:N', title='University'),
                alt.Tooltip('professor_name:N', title='Professor'),
                alt.Tooltip('num_of_pub:Q', title='Number of Publications'),
                alt.Tooltip('ave_if:Q', title='Average Impact Factor'),
                alt.Tooltip('impact_level:N', title='Impact Level')],
    ).properties(
        width=800, 
        height=400,
        title='Professor Profiles: Publications vs Impact Factor'
    ).configure_axis(
        gridOpacity=0.5  # Adjust gridline transparency (0: fully transparent, 1: fully opaque)
    ).interactive()
    return base_chart

def prof_univ_bar(professor_name, selected_university, df):
    university_df = df[df['university_name'] == selected_university]
    university_df['opacity'] = 0.2
    university_df.loc[university_df['professor_name']==professor_name,'opacity'] = 1
    chart = alt.Chart(university_df).mark_bar().encode(
        x=alt.X('professor_name',sort='-y', axis=None),
        y=alt.Y('overall_impact', title='Overall Impact'),
        color=alt.Color('Community Contribution:N',scale=alt.Scale(scheme='tableau10'),legend=alt.Legend(orient='top', direction='horizontal')),
        opacity=alt.Opacity('opacity', legend=None),
        tooltip=[
            alt.Tooltip('professor_name:N', title='Professor name'),  # Tooltip for professor names
            alt.Tooltip('num_of_pub:Q', title='Publication per year'),  # Format overall impact
            alt.Tooltip('overall_impact:Q', title = 'Overall contribution', format = '.2f'),
            alt.Tooltip('ave_if:Q', title = 'Average impact factor', format = '.2f'),
            alt.Tooltip('Community Contribution:N', title='Community Contribution')  # Add contribution to tooltip
        ]
    ).properties(width=800, height=400)
    return chart

def univ_bar(selected_university, df):
    university_df = df[df['university_name'] == selected_university] 
    chart = alt.Chart(university_df).mark_bar().encode(
        x=alt.X('professor_name',sort='-y', axis=None),
        y=alt.Y('overall_impact', title='Overall Impact'),
        color=alt.Color('Community Contribution:N',scale=alt.Scale(scheme='tableau10'),legend=alt.Legend(orient='top', direction='horizontal')),
        tooltip=[
            alt.Tooltip('professor_name:N', title='Professor name'),  # Tooltip for professor names
            alt.Tooltip('num_of_pub:Q', title='Publication per year'),  # Format overall impact
            alt.Tooltip('overall_impact:Q', title = 'Overall contribution', format = '.2f'),
            alt.Tooltip('ave_if:Q', title = 'Average impact factor', format = '.2f'),
            alt.Tooltip('Community Contribution:N', title='Community Contribution')  # Add contribution to tooltip
        ]
    ).properties(width=800, height=400)
    return chart


def highlight_professor_chart(professor_name, selected_university, df):
    university_df = df[df['university_name'] == selected_university]
    matched_professor = process.extractOne(professor_name, university_df['professor_name'])[0]
    
    base_chart = alt.Chart(university_df).mark_circle().encode(
        x=alt.X('num_of_pub', title='Number of publications per year'),
        #y='ave_if',
        y=alt.Y('ave_if', scale=alt.Scale(type='log', domain=[0.5, 100]), title='Average impact factor'),
        color=alt.Color('Community Contribution:N',scale=alt.Scale(scheme='tableau10')),
        #opacity=alt.value(0.6),
        tooltip=[alt.Tooltip('university_name:N', title='University'),
                alt.Tooltip('professor_name:N', title='Professor'),
                alt.Tooltip('num_of_pub:Q', title='Number of Publications'),
                alt.Tooltip('ave_if:Q', title='Average Impact Factor'),
                alt.Tooltip('impact_level:N', title='Impact Level')],
    ).properties(
        width=800, 
        height=400,
        title='Professor Profiles: Publications vs Impact Factor'
    )

    professor_df = university_df[university_df['professor_name']==matched_professor]
    prof_chart = alt.Chart(professor_df).mark_point(size=75,filled=True,  color='black').encode(
        x=alt.X('num_of_pub', title=''),
        y=alt.Y('ave_if', scale=alt.Scale(type='log', domain=[0.5, 100]), title=''),
        #color=alt.Color('impact_level:N', scale=alt.Scale(scheme='viridis'), title='Impact Level'),
        #size=alt.value(50),
        tooltip=[alt.Tooltip('university_name:N', title='University'),
                alt.Tooltip('professor_name:N', title='Professor'),
                alt.Tooltip('num_of_pub:Q', title='Number of Publications'),
                alt.Tooltip('ave_if:Q', title='Average Impact Factor'),
                alt.Tooltip('impact_level:N', title='Impact Level')],
    ).properties(
        width=800, 
        height=400,
        title='Professor Profiles: Publications vs Impact Factor'
    )
    chart = base_chart + prof_chart


    return chart

def profile_individual(university, name):
    df = pd.read_csv('../datasets/prof_topic.csv')
    unique_name = university+'--'+name
    person_info = df[df['Unnamed: 0']==unique_name]

    person_topic_info = person_info.iloc[:,1:].T
    person_topic_info.columns = ['score']
    person_topic_info = person_topic_info.sort_values(by='score', ascending=False)
    person_topic_info = person_topic_info.head(5)
    person_topic_info=person_topic_info.reset_index()
    max_radius = person_topic_info.iloc[0,1]
    fig = go.Figure()

    # Add trace to radar plot with improved color style
    fig.add_trace(go.Scatterpolar(
        r=person_topic_info['score'].tolist() + [person_topic_info['score'].iloc[0]],  # Close the circle
        theta=person_topic_info['index'].tolist() + [person_topic_info['index'].iloc[0]],  # Close the circle
        fill='toself',
        line=dict(color='deepskyblue', width=2),  # Change line color
        fillcolor='rgba(135, 206, 250, 0.3)'  # Light blue fill color with transparency
    ))

    # Update layout for radar plot
    fig.update_layout(
        title_x=0.5,  # Center the title
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max_radius],  # Adjust according to your data range
                showticklabels=True,
                ticks='outside',
                ticklen=5
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color='black'),  # Customize axis labels
                showticklabels=True,
                ticks='outside'
            )
        ),
        legend=dict(
            title='Legend',
            title_font_size=13,
            font=dict(size=12, color='black')
        ),
        margin=dict(l=50, r=50, t=50, b=50)  # Adjust margins
    )


    return fig
 
def find_best_paper(university, name):
    paper_df = pd.read_csv('../datasets/paper_with_title.csv')
    personal_df = paper_df[paper_df['university']==university]
    personal_df = personal_df[personal_df['professor_name']==name]

    personal_df = paper_df[paper_df['professor_authorship'].isin(['First Corresponding author', 'First Author'])]
    personal_df = personal_df.drop_duplicates(subset='PMID')
    personal_df = personal_df.sort_values(by='journal_if', ascending=False)

    personal_df['publish_date'] = pd.to_datetime(personal_df['publish_date'])
    personal_df['time']  = personal_df['publish_date'].dt.to_period('M')
    personal_df=personal_df[['time', 'PMID','title']]
    personal_df = personal_df.iloc[:10,:]
    personal_df.set_index('time', inplace=True)

    return personal_df 

