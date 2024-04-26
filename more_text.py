import streamlit as st

class Stream():
    def __init__(self):
        # Title
        st.title("Title Dummy")
        st.header("Header Dummy")
        st.subheader("Subheader for me")
        st.text("My name is YES Wheelchair, I was born 19th March 2011")

        # Markdown
        st.markdown("># Hello *World*")
        st.markdown("---")
        st.markdown("### [Google](https://www.google.com)")

        # Caption
        st.caption("Hi I am Caption")

if __name__ == '__main__':
    stream = Stream()
