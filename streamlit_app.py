import streamlit as st

st.title("🎈 Jaime's app")

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
generate_images = st.Page("pages/generate_images.py", title="Generate New Images", icon=":material/auto_awesome:")
upload_images_page = st.Page("pages/upload_images.py", title="Upload Generated Images", icon=":material/drive_folder_upload:")
delete_images_page = st.Page("pages/delete_images.py", title="Delete Generated Images", icon=":material/delete:")
settings = st.Page("pages/settings.py", title="Settings", icon=":material/settings:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [home, profile],
            "Tasks": [generate_images, upload_images_page, delete_images_page],
            "Utilities": [settings, logout_page]
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()