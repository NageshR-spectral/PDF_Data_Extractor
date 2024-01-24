import openai
import streamlit as st
from main import Main 

openai.api_key = "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"


def main():
   
    st.set_page_config(page_title="PDF Processing App", page_icon="📄")

    st.title("PDF to Text Conversion and JSON output")

    file_path = st.file_uploader("Upload a PDF file", type=["pdf"])

    if file_path:
        main_obj = Main(file_path)
        main_obj.convert_pdf_to_text()

if __name__ == "__main__":
    main()