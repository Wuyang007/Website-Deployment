import streamlit as st
import pandas as pd
import altair as alt
import requests

import streamlit as st
import os
from PIL import Image


import sys
sys.path.append('../help_functions')

from university_profile import draw_university_profile
from professor_profile import create_base_chart, find_best_paper, prof_univ_bar, univ_bar, profile_individual
from topic_profile import topic_distribution
from topic_time_series import draw_time_series_plot
#from transformers import T5Tokenizer, T5ForConditionalGeneration
from chatbot import generate_response



# Set up the title of the app
#st.title("What")

# Create a sidebar for navigation
st.set_page_config(page_title="Prof-Insight", layout="wide")


st.sidebar.image('datasets/images/logo.png', width=150)

#st.sidebar.title("Prof-Insight")
st.sidebar.markdown("<br>", unsafe_allow_html=True)
st.sidebar.text_input("Search")
st.sidebar.markdown("<br>", unsafe_allow_html=True)

selected_section = st.sidebar.radio("Go to", ["Overview", "University", 'Professor', 'Topics', 'Current Opportunities', "Ask us", "About this project"])


st.sidebar.markdown("<div style='height: 100%;'></div>", unsafe_allow_html=True)
st.sidebar.markdown("### Contact Us")
st.sidebar.markdown("[Email us](mailto:wuyang.gao007@gmail.com)")

#--------------------------------------------------------------------------------------------
# following is for the overview page
if selected_section == "Overview":
    #st.header("Welcome to Prof-Insight")
    
    #st.write("This is :blue[test]")
    st.markdown("""
    <style>
        .highlighted-text {
            font-size: 36px; /* Slightly smaller but still prominent */
            font-weight: 600; /* Semi-bold for a refined look */
            color: #003366; /* Dark blue color for professionalism */
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3); /* Subtle shadow for depth */
            letter-spacing: 1px; /* Slight spacing between letters for readability */
            text-align: center; /* Center align text */
            margin-top: 40px; /* Space above text */
            margin-bottom: 40px; /* Space below text */
            line-height: 1.4; /* Adjust line height for better readability */
        }
        .info-bar {
            background-color: #e74c3c; /* Orange-red background color */
            color: #ffffff; /* White text color */
            font-size: 24px; /* Font size for the bar text */
            font-weight: 700; /* Bold text */
            text-align: center; /* Center align text */
            padding: 15px 0; /* Padding for top and bottom */
            margin: 20px 0; /* Margin for spacing */
            border-radius: 5px; /* Rounded corners for a softer look */
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
        }
    </style>
""", unsafe_allow_html=True)
    st.markdown("""
    <div class="highlighted-text">
        Prof-Insight: Your personal assistant for graduate career!
    </div>
""", unsafe_allow_html=True)
    st.image('datasets/images/Picture1.png', caption='')
    st.markdown("""
    <div class="info-bar">
        Biomedical Engineering \t  |   Top 35 Universities \t  |   93,200 Manuscripts \t  | \t  1,880 Professors
    </div>
""", unsafe_allow_html=True)
#    st.markdown('\n')
    

#--------------------------------------------------------------------------------------------
# following is for the university page
elif selected_section == "University":
    st.title("University Profiles in Biomedical Engineering")
    st.header("Universities faculty community and publications")
    st.markdown('''Biomedical Engineering blends engineering and biology to create cutting-edge medical technologies. 
                Many top-ranking universities now offer specialized programs in this field, driving advancements in medical 
                devices, diagnostic tools, and therapies to enhance patient care and health outcomes.''')
    

    university_df = pd.read_csv('datasets/numeric_table/university_profile.csv')
    university_chart = draw_university_profile(university_df)
    st.altair_chart(university_chart, use_container_width=True)
    st.markdown('<br><br>', unsafe_allow_html=True) 
    
    # Customize the table's style (e.g., bold headers, font size, background color)
    university_df = university_df.set_index('university_name')
    university_df.rename(columns={'total publications per year': 'total publications per year since 2014'}, inplace=True)
    styled_table = university_df.style.set_properties(**{
        'font-size': '14px',
        'font-family': 'Arial',
        'background-color': '#f9f9f9',  # Slightly different light grey for a modern look
        'border': '1px solid #ddd',       # Light grey border for a subtle look
        'text-align': 'left',             # Align text to the left for readability
    }).set_table_styles([
        {'selector': 'thead th', 'props': [('font-weight', 'bold'), ('background-color', '#e0e0e0'), ('border-bottom', '2px solid #ccc')]},  # Bold headers with a slightly darker background
        {'selector': 'tbody tr:hover', 'props': [('background-color', '#f1f1f1')]},  # Highlight rows on hover
        {'selector': 'tbody td', 'props': [('padding', '8px')]},  # Add padding to cells
    ]).set_table_attributes('style="border-collapse: collapse; width: 100%;"')  #

    # Display the styled dataframe
    
    st.write(styled_table)


#--------------------------------------------------------------------------------------------
# following is for the Professor page
elif selected_section == "Professor":
    st.header("Professors")
    st.title("Professor Impact Finder")
    df = pd.read_csv('datasets/professor_profile.csv')
    df = df[['university_name', 'professor_name', 'ave_if', 'num_of_pub', 'overall_impact', 'impact_level','Community Contribution']]

    # Display the base chart
    base_chart = create_base_chart(df)
    st.altair_chart(base_chart, use_container_width=True)

    st.markdown('<br>', unsafe_allow_html=True) 
    st.title("Find the professor")
    # University selection
    selected_university = st.selectbox("Select University", options=df['university_name'].unique())

    # Professor name input
    professor_list = df[df['university_name']==selected_university]['professor_name'].unique()
    professor_name_input = st.selectbox("Select Professor", options=professor_list)

    # Highlight chart based on input
    if selected_university:
        if professor_name_input:
            prof_univ_chart = prof_univ_bar(professor_name_input, selected_university, df)
            st.altair_chart(prof_univ_chart, use_container_width=True)
        else: 
            univer_chart = univ_bar(selected_university, df)
            st.altair_chart(univer_chart, use_container_width=True)
    else:
        st.write('Enter a university')

    st.markdown('<br>', unsafe_allow_html=True) 
    st.markdown(f'Summary of {professor_name_input}:\n')
    
    prof_paper_df = find_best_paper(str(selected_university), str(professor_name_input))
    st.dataframe(prof_paper_df)
    st.markdown('<br>', unsafe_allow_html=True) 
    st.title("Compare the professor")


    col1, col2 = st.columns(2)
    with col1:
        selected_university_1 = st.selectbox("Select the first university", options=df['university_name'].unique())
        professor_list_1 = df[df['university_name']==selected_university_1]['professor_name'].unique()
        professor_name_input_1 = st.selectbox("Select the first professor:", options=professor_list_1)
        fig_1 = profile_individual(str(selected_university_1), str(professor_name_input_1))
        st.plotly_chart(fig_1)
    with col2:
        selected_university_2 = st.selectbox("Select the second university", options=df['university_name'].unique())
        professor_list_2 = df[df['university_name']==selected_university_2]['professor_name'].unique()
        professor_name_input_2 = st.selectbox("Select the second professor", options=professor_list_2)
        fig_2 = profile_individual(str(selected_university_2), str(professor_name_input_2))
        st.plotly_chart(fig_2)

#--------------------------------------------------------------------------------------------
# following is for the Professor page

elif selected_section == "Topics":
    st.header("Research Topics in Biomedical Engineering")
    

    image_folder = 'datasets/topics'
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
    st.markdown('<br>', unsafe_allow_html=True) 
    st.write("#### All 93201 papers")
    st.image('datasets/images/pca_plot.png', use_column_width=True)

    st.markdown('<br><br>', unsafe_allow_html=True) 

    st.write("#### 20 subtopics")
    topic_dist_df = pd.read_csv('datasets/topic_distribution.csv')
    topic_dist_chart = topic_distribution(topic_dist_df)
    st.altair_chart(topic_dist_chart, use_container_width=True)

    st.markdown('<br><br>', unsafe_allow_html=True) 

    st.write("#### University_topics")
    st.image('datasets/images/university_topic.png', use_column_width=True)
    st.markdown('<br><br>', unsafe_allow_html=True) 

    st.write("#### Along the time")
    topic_name_df = pd.read_csv('datasets/topic_distribution.csv')
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
    st.header("Current graduate positions as below:")



elif selected_section == "Ask us":
    st.title("Questions:")
    user_input = st.text_input("You: ", "")
    AZURE_API_KEY = '5f3dfecbd34d4bed939cd0e4b7abed63'  # Replace with your actual API key
    AZURE_ENDPOINT = 'https://prof-insight-ai-service.cognitiveservices.azure.com/'
    
    def get_azure_response(prompt):
        headers = {
            'Content-Type': 'application/json',
            'api-key': AZURE_API_KEY
        }
        
        data = {
            "prompt": prompt,
            "max_tokens": 100  # Control response length
        }
        
        response = requests.post(AZURE_ENDPOINT, headers=headers, json=data)
        
        if response.status_code == 200:
            response_json = response.json()
            return response_json['choices'][0]['text']  # Get response text
        else:
            return f"Error: {response.status_code}, {response.text}"

    if user_input:
        response = get_azure_response(user_input)
        st.write(f"AI Response: {response}")
    

elif selected_section == "About this project":
    st.header("Section 3")

#    st.write("Add any additional information or visualizations here.")
    st.image('datasets/images/pipeline_schematics.png', caption='Pipeline for data analysis', use_column_width=True)

    st.write("Author: Wuyang Gao")
    st.write("Last updated: Sep 6, 2024")

