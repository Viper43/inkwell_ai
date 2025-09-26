import streamlit as st
from few_shot import FewShotPost
from post_generator import generate_post

length_options = ['short', 'medium', 'long', 'very long']
language_options = ['English', 'Hinlish']

def main():
    st.title('linkedin post generator')
    col1, col2, col3 = st.columns(3)
    fs = FewShotPost()
    with col1:
        # Dropdown for Titles
        selected_tag = st.selectbox("Title", options=fs.get_unique_tags())

    with col2:
        # Dropdown for length category
        selected_length = st.selectbox("Length", options=length_options)
    
    with col3:
        # Dropdown for Language
        selected_language = st.selectbox("Language", options=language_options)

    if st.button('Generate Post'):
        post = generate_post(selected_length, selected_tag, selected_language)
        st.subheader('Generated Post')
        st.write(post)

if __name__ == "__main__":
    main()