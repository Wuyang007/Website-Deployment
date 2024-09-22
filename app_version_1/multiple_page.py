import streamlit as st
import pandas as pd
import altair as alt
from fuzzywuzzy import process
import streamlit as st
import os
from PIL import Image

from university_profile import draw_university_profile
from professor_profile import create_base_chart, highlight_professor_chart, profile_individual, find_best_paper
from topic_profile import topic_distribution
from topic_time_series import draw_time_series_plot
from transformers import T5Tokenizer, T5ForConditionalGeneration
from chatbot import generate_response



# Set up the title of the app
#st.title("What")

# Create a sidebar for navigation
st.set_page_config(page_title="Prof-Insight", layout="wide")
st.sidebar.image('../datasets/images/logo.png', width=150)

#st.sidebar.title("Prof-Insight")
selected_section = st.sidebar.radio("Go to", ["Overview", "University", 'Professor', 'Topics', 'Current Oppotunities', "Ask us", "About this project", 'Contact us'])

# Create a header with a tag at the top left
if selected_section == "Overview":
    st.header("Welcome to Prof-Insight")
    st.image('../datasets/images/Picture1.png', caption='Top 35 Universities in Biomedical Engineering', use_column_width=True)
    
    st.markdown(''' Your comprehensive resource for exploring the cutting-edge world of **biomedical engineering research**. 
                \n''')

    st.markdown('\n')
    


elif selected_section == "University":
    st.header("Universities")
    
    
    st.markdown("Quick fact about Biomedical Engineering Academic field")
    
    university_df = pd.read_csv('../datasets/university_profile.csv')
    university_chart = draw_university_profile(university_df)
    st.altair_chart(university_chart, use_container_width=True)

    st.markdown("\n")
    top_df = pd.read_csv('../datasets/top_5_universities.csv')
    st.table(top_df)

    #st.image('path_to_your_image.png', caption='Image for Section 1', use_column_width=True)

elif selected_section == "Professor":
    st.header("Professors")
    

    st.title("Professor Impact Finder")
    df = pd.read_csv('../datasets/professor_profile.csv')
    df = df[['university_name', 'professor_name', 'ave_if', 'num_of_pub', 'overall_impact', 'impact_level','Community Contribution']]

    # Display the base chart
    base_chart = create_base_chart(df)
    st.altair_chart(base_chart, use_container_width=True)

    # University selection
    selected_university = st.selectbox("Select University", options=df['university_name'].unique())

    # Professor name input
    professor_list = df[df['university_name']==selected_university]['professor_name'].unique()
    professor_name_input = st.selectbox("Select Professor", options=professor_list)

    # Highlight chart based on input
    if professor_name_input:
        if selected_university:
            highlighted_chart = highlight_professor_chart(professor_name_input, selected_university, df)
            st.altair_chart(highlighted_chart, use_container_width=True)
        else:
            st.write("Please select a university.")
    else:
        st.write("Enter a professor's name to highlight.")

    #st.image('../datasets/images/university_profile.png', caption='Top 35 Universities in Biomedical Engineering', use_column_width=True)
    #st.image('path_to_your_image.png', caption='Image for Section 1', use_column_width=True)
    fig = profile_individual(str(selected_university), str(professor_name_input))
    st.plotly_chart(fig)
    prof_paper_df = find_best_paper(str(selected_university), str(professor_name_input))
    st.dataframe(prof_paper_df)


elif selected_section == "Topics":
    st.header("Research Topics in Biomedical Engineering")
    

    image_folder = '../datasets/topics'
    #image_folder = 'path/to/your/images'  # Update this to the path of your images
    image_files = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith(('png', 'jpg', 'jpeg'))]

    # Display images in a grid
    st.write("#### Keywords of the 20 subtopics")
    cols = st.columns(5)  # Create 5 columns
    
    
    # Loop through images and display them
    for idx, img_file in enumerate(image_files):
        if idx % 5 == 0 and idx != 0:
            cols = st.columns(5)  # Create new row
        with cols[idx % 5]:
            image = Image.open(img_file)
            st.image(image, use_column_width=True)
    st.markdown("\n\n\n\n")
    st.markdown("\n\n\n\n")
    st.markdown("\n\n\n\n")
    st.write("#### All 93201 papers")
    st.image('../datasets/images/pca_plot.png', use_column_width=True)

    st.markdown("\n\n\n\n")
    st.markdown("\n\n\n\n")
    st.markdown("\n\n\n\n")
    st.write("#### 20 subtopics")
    topic_dist_df = pd.read_csv('../datasets/topic_distribution.csv')
    topic_dist_chart = topic_distribution(topic_dist_df)
    st.altair_chart(topic_dist_chart, use_container_width=True)

    st.markdown("\n\n\n\n")
    st.markdown("\n\n\n\n")
    st.markdown("\n\n\n\n")
    st.write("#### University_topics")
    st.image('../datasets/images/university_topic.png', use_column_width=True)
    st.markdown("\n\n\n\n")
    st.markdown("\n\n\n\n")
    st.markdown("\n\n\n\n")
    st.write("#### Along the time")
    topic_name_df = pd.read_csv('../datasets/topic_distribution.csv')
    topic_list = list(topic_name_df['index'].unique())

    selected_topic_1 = st.selectbox("Select The First Research Topic", options=topic_list)
    selected_topic_1 = str(selected_topic_1)
    topic_chart_1 = draw_time_series_plot(selected_topic_1)
    st.altair_chart(topic_chart_1, use_container_width=True)

    selected_topic_2 = st.selectbox("Select The Second Research Topic", options=topic_list)
    selected_topic_2 = str(selected_topic_2)
    topic_chart_1 = draw_time_series_plot(selected_topic_2)
    st.altair_chart(topic_chart_1, use_container_width=True)
 

elif selected_section == "Current Opportunities":
    st.header("Current graduate opportunities in North America:")




elif selected_section == "Ask us":
    st.title("Anything you interested")
    user_input = st.text_input("You: ", "")

    # When the user presses the button, generate a response
    if st.button("Send"):
        if user_input:
            # Generate chatbot response
            response = generate_response(user_input)
            st.write(f"**Chatbot**: {response}")
        else:
            st.write("Please enter a message.")
    

elif selected_section == "About this project":
    st.header("Section 3")
    st.markdown("Content for section 3 goes here.")
    st.write("Add any additional information or visualizations here.")
    st.image('../datasets/images/pipeline_schematics.png', caption='Pipeline for data analysis', use_column_width=True)

    st.write("Author: Wuyang Gao")
    st.write("Last updated: Sep 6, 2024")


elif selected_section == "Contact us":
    st.header("Section 3")
    st.markdown("Content for section 3 goes here.")

    st.write("Author: Wuyang Gao")
    st.write("Last updated: Sep 6, 2024")
