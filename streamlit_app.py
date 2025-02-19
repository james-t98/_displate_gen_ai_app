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

profile = st.Page("pages/profile.py", title="About Me", icon=":material/manage_accounts:")
home = st.Page("pages/home.py", title="Home", icon=":material/home:")

sentiment_analysis = st.Page("pages/sentiment_analysis.py", title="Sentiment Analysis", icon=":material/psychology:")

generate_images = st.Page("pages/generate_images.py", title="Generate New Images", icon=":material/auto_awesome:")
upload_images_page = st.Page("pages/images.py", title="Generated Images", icon=":material/drive_folder_upload:")

auto = st.Page("pages/automotive.py", title="Formula 1 Project", icon=":material/sports_motorsports:")

sport_football = st.Page("pages/sport_football.py", title="Football Project", icon=":material/sports_soccer:")
sport_basketball = st.Page("pages/sport_basketball.py", title="Basketball Project", icon=":material/sports_basketball:")

health = st.Page("pages/health.py", title="HealthCare Project", icon=":material/medical_information:")

finance = st.Page("pages/finance.py", title="FinTech Project", icon=":material/account_balance:")

research_astronomy = st.Page("pages/research_astronomy.py", title="Astronomy Project", icon=":material/rocket_launch:")
research_oceanic = st.Page("pages/research_oceanic.py", title="Ocean/Marine Project", icon=":material/tsunami:")

settings = st.Page("pages/settings.py", title="Settings", icon=":material/settings:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [home, profile],
            "Natural Language Processing": [sentiment_analysis],
            "Computer Vision": [generate_images, upload_images_page],
            "Automotive": [auto],
            "Sport": [sport_football, sport_basketball],
            "HealthCare": [health],
            "Finance": [finance],
            "Research": [research_astronomy, research_oceanic],
            "Utilities": [settings, logout_page]
        },
        expanded=False
    )
else:
    pg = st.navigation([login_page])

pg.run()