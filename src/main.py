import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post

# Options for length and language
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]

# Custom styles
st.markdown("""
    <style>
    .header {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        background: -webkit-linear-gradient(45deg, #6a11cb, #2575fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 10px;
    }

    .card {
        background-color: #fefefe;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Main app layout
def main():
    # Gradient Header
    st.markdown('<div class="header">քօֆȶքɨʟօȶ</div>', unsafe_allow_html=True)

    # Card start
    st.markdown('<div class="card">', unsafe_allow_html=True)

    fs = FewShotPosts()
    tags = fs.get_tags()

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_tag = st.selectbox("Topic", options=tags)

    with col2:
        selected_length = st.selectbox("Length", options=length_options)

    with col3:
        selected_language = st.selectbox("Language", options=language_options)

    st.markdown('</div>', unsafe_allow_html=True)  # End of card

    # Generate button centered
    colA, colB, colC = st.columns([1.5, 1, 1])
    with colB:
        generate_clicked = st.button("Generate")

    if generate_clicked:
        post = generate_post(selected_length, selected_language, selected_tag)

        # Output post in center
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.success(post)


# Run the app
if __name__ == "__main__":
    main()
