import utils
import streamlit as st
import os
import openai
openai.api_key = utils.get_openai_api_key()
from retriever import retrieval_function
from llama_index import SimpleDirectoryReader

fp = "TheRBook.pdf"
documents = SimpleDirectoryReader(
    input_files=[fp]
).load_data()


button_style = """
<style>
div.stButton > button:first-child {
    background-color: #0099ff;
    color: white;
}
div.stButton > button:first-child:hover {
    background-color: #0077cc;
}
</style>
"""


def main():
    st.title("Your raggedy Rag friend")
    st.markdown(button_style, unsafe_allow_html=True)

    book= st.selectbox("Choose your book", [None, "The R Book", "R for Data Science"])

    if book:
        with st.form("prompt_form", clear_on_submit=False):
            placeholder_text = "What's your query"
            query = st.text_area("Your Question:", placeholder=placeholder_text, height=100)
            prompt_submitted = st.form_submit_button("Look up information")

        if prompt_submitted:
            text = retrieval_function(book, query, retrieve_only=False)
            st.write(text)

            if st.button("Try Another Question"):
                st.experimental_rerun()


if __name__ == "__main__":
    main()
