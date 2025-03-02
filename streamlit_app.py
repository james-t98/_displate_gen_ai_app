import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

portfolio = st.Page("pages/portfolio.py", title="Portfolio", icon=":material/home:")
profile = st.Page("pages/profile.py", title="About Me", icon=":material/manage_accounts:")

chat_bot = st.Page("pages/chat_bot.py", title="LLM ChatBot", icon=":material/filter_drama:")
image_generation = st.Page("pages/generative_images.py", title="Image Generation", icon=":material/auto_awesome:")

sentiment_analysis = st.Page("pages/sentiment_analysis.py", title="Sentiment Analysis", icon=":material/psychology:")

computer_vision_image_classification = st.Page("pages/computer_vision_image_classification.py", title="Image Classification", icon=":material/auto_awesome:")

auto = st.Page("pages/automotive.py", title="Formula 1 Project", icon=":material/sports_motorsports:")

sport_football = st.Page("pages/sport_football.py", title="Football Project", icon=":material/sports_soccer:")
sport_basketball = st.Page("pages/sport_basketball.py", title="Basketball Project", icon=":material/sports_basketball:")

health = st.Page("pages/health.py", title="HealthCare Project", icon=":material/medical_information:")

finance = st.Page("pages/finance.py", title="FinTech Project", icon=":material/account_balance:")

research_astronomy = st.Page("pages/research_astronomy.py", title="Astronomy Project", icon=":material/rocket_launch:")
research_oceanic = st.Page("pages/research_oceanic.py", title="Ocean/Marine Project", icon=":material/tsunami:")

apartment_hunter = st.Page("pages/apartment_hunting.py", title="Apartment Hunter", icon=":material/apartment:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Home": [portfolio, profile],
            "Generative AI": [chat_bot, image_generation],
            "Natural Language Processing": [sentiment_analysis],
            "Computer Vision": [computer_vision_image_classification],
            "Automotive": [auto],
            "Sport": [sport_football, sport_basketball],
            "HealthCare": [health],
            "Finance": [finance],
            "Research": [research_astronomy, research_oceanic],
            "Personal": [apartment_hunter],
            "Utilities": [logout_page]
        },
        expanded=False
    )
else:
    pg = st.navigation([login_page])

pg.run()