import pandas as pd
import numpy as np
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

def add_link(df):
    link_dict = {
        'Carnegie Mellon University': 'https://www.cmu.edu/bme/People/Faculty/index.html',
        'Columbia University': 'https://www.bme.columbia.edu/directory?gsarqfields%5Bbiotypetid%5D=30',
        'Cornell University': 'https://www.bme.cornell.edu/bme/faculty-directory',
        'Duke University': 'https://bme.duke.edu/faculty',
        'ETH Zurich': 'https://biomed.ee.ethz.ch/institute/People/principal-investigators.html',
        'Georgia Institute of Technology': 'https://bioengineering.gatech.edu/program-faculty',
        'Harvard University': 'https://seas.harvard.edu/bioengineering/people?role%5B46%5D=46',
        'Imperial College London': 'https://www.imperial.ac.uk/bioengineering/people/academic-staff-and-research-fellows/',
        'Johns Hopkins University': 'https://www.bme.jhu.edu/people/faculty/',
        'Massachusetts Institute of Technology': 'https://be.mit.edu/faculty/?exposed_search&exposed_taxonomy_role%5B0%5D=35&exposed_taxonomy_role%5B1%5D=34&exposed_taxonomy_role%5B2%5D=32',
        'McGill University': 'https://www.mcgill.ca/bioengineering/people',
        'Nanyang Technological University': 'https://www.ntu.edu.sg/cceb/faculty-and-staff/chemical-engineering',
        'National University of Singapore': 'https://cde.nus.edu.sg/bme/about-us/people/academic-staff/?category=academic-3&search&sort=ASC',
        'Northwestern University': 'https://www.mccormick.northwestern.edu/biomedical/people/faculty/',
        'Peking University': 'https://future.pku.edu.cn/en/js/Faculty/index.htm',
        'Rice University': 'https://bioengineering.rice.edu/people',
        'Shanghai Jiao Tong University': 'https://en.bme.sjtu.edu.cn/lists-faculty.html',
        'Stanford University': 'https://bioengineering.stanford.edu/people/faculty',
        'Tsinghua University': 'https://www.med.tsinghua.edu.cn/en/Faculty/DepartmentofBiomedicalEngineering.htm',
        'University College London': 'https://www.ucl.ac.uk/biochemical-engineering/people/academics',
        'University of British Columbia': 'https://bme.ubc.ca/people/?custom_cat=faculty',
        'University of California Berkeley': 'https://bioeng.berkeley.edu/people',
        'University of California Los Angeles': 'https://samueli.ucla.edu/search-faculty/#be',
        'University of California San Diego': 'https://be.ucsd.edu/faculty',
        'University of California San Francisco': 'https://bts.ucsf.edu/people/faculty',
        'University of Cambridge': 'https://www.eng.cam.ac.uk/people/strategic-research-theme/181?field_user_surname_value_1=&field_user_list_category_tid=216',
        'University of Hong Kong': 'https://www.engineering.hku.hk/bmeengg/people-faculty/',
        'University of Michigan': 'https://bme.umich.edu/role/core/',
        'University of Oxford': 'https://ibme.ox.ac.uk/people/directory/?role=ac',
        'University of Pennsylvania': 'https://directory.seas.upenn.edu/bioengineering/',
        'University of Pittsburgh': 'https://www.engineering.pitt.edu/departments/bioengineering/people/faculty-research-interests/',
        'University of Sydney': 'https://www.sydney.edu.au/engineering/schools/school-of-biomedical-engineering/academic-staff.html',
        'University of Washington': 'https://bioe.uw.edu/faculty-staff/core-faculty/',
        'University of Tokyo': 'https://bioeng.t.u-tokyo.ac.jp/en/faculty/',
        'University of Toronto': 'https://bme.utoronto.ca/faculty-research/core-faculty/',
    }

    def find_link(name):
        return link_dict[name]
    
    df['link'] = df['university_name'].apply(find_link)

    return df



