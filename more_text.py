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

        # Latex
        st.latex(r"\begin{pmatrix} a&b\\c&d \end{pmatrix}")
        st.markdown("### [Latex (Format)](https://katex.org/docs/supported.html)")

        # Json
        json = {"a":"1,2,3", "b":"4,5,6"}
        st.json(json)

        # Code
        code = '''
        print("Hello World")
        def function_A():
            return "Me"'''
        st.code(code, language="python")

if __name__ == '__main__':
    stream = Stream()