   
   
   
import streamlit as st
from streamlit_option_menu import option_menu
from app_utils import switch_page
import streamlit as st
from PIL import Image



#im = Image.open("icon.png")
st.set_page_config(page_title = "AI Interviewer", layout = "centered") #page_icon=im
home_title = "AI Interviewer"
x=1
if x==1:
    home_introduction = "Welcome to AI Interviewer, empowering your interview preparation with generative AI."
    with st.sidebar:
        st.markdown('AI Interviewer')
   
    st.markdown(
        "<style>#MainMenu{visibility:hidden;}</style>",
        unsafe_allow_html=True
    )
   # st.image(im, width=100)
    st.markdown(f"""# {home_title} <span style=color:#2E9BF5><font size=5></font></span>""",unsafe_allow_html=True)
    st.markdown("""\n""")
    #st.markdown("#### Greetings")
    st.markdown("Welcome to AI Interviewer! 👏 AI Interviewer is your personal interviewer powered by generative AI that conducts mock interviews."
                "You can upload your resume and enter job descriptions, and AI Interviewer will ask you customized questions.")
    #st.markdown("""\n""")
    st.markdown("#### Get started!")
    st.markdown("Select one of the following choices to start your interview!")
    selected = option_menu(
            menu_title= None,
            options=["Professional", "Behavioral", "Resume"],
            icons = ["cast", "cloud-upload", "cast"],
            default_index=0,
            orientation="horizontal",
        )
    if selected == 'Professional':
        st.info("""
            📚In this session, the AI Interviewer will assess your technical skills as they relate to the job description.
            - Start, introduce yourself and enjoy！ """)
        if st.button("Start Interview!"):
            switch_page("Professional Screen")
    if selected == 'Behavioral':
        st.info("""
        📚In this session, the AI Interviewer will assess your soft skills as they relate to the job description.
       
        - Start, introduce yourself and enjoy！ 
        """)
        if st.button("Start Interview!"):
            switch_page("Behavioral Screen")
    if selected == 'Resume':
        st.info("""
        📚In this session, the AI Interviewer will review your resume and discuss your past experiences.
        - Start, introduce yourself and enjoy！ """
        ) #        - Choose your favorite interaction style (chat/voice)

        if st.button("Start Interview!"):
            switch_page("Resume Screen")


    st.markdown("""\n""")

