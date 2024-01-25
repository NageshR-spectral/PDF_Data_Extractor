import openai
import streamlit as st
from main import Main 
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


def main():
   
    st.set_page_config(page_title="PDF Processing App", page_icon="📄")

    st.title("PDF to Text Conversion and JSON output")

    file_path = st.file_uploader("Upload a PDF file", type=["pdf"])

    if file_path:
        main_obj = Main(file_path)
        # Check whether the temp file already exists
        if "temp_pdf.pdf" in os.listdir():
            os.remove("temp_pdf.pdf")  # Remove existing temporary file
            main_obj.convert_pdf_to_text()
        else:
            main_obj.convert_pdf_to_text()

if __name__ == "__main__":
    main()