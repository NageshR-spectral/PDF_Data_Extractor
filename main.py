from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import PDFPlumberLoader
import json
import streamlit as st
from utils import get_binary_file_downloader_html_from_string, chat_handler

class Main:

    def __init__(self, file_path):
        self.file_path = file_path

    def convert_pdf_to_text(self):
        
        # Display file path
        st.sidebar.subheader("File Information:")
        st.sidebar.text(f"File Name: {self.file_path.name}")

        # PDF to Text Conversion
        st.header("PDF to Text Conversion:")
        pdf_to_text_button = st.button("Convert PDF to Text")

        # Save the uploaded file to a temporary location
        with open("temp_pdf.pdf", "wb") as f:
            f.write(self.file_path.getvalue())

        if pdf_to_text_button:
            st.sidebar.subheader("Text Content:")
            loader = PyMuPDFLoader("temp_pdf.pdf")
            data = loader.load()
            content = data[0].page_content
            st.sidebar.text(content)

        # Chat Handling
        chat_button = st.button("Get JSON output")

        if chat_button:
            st.subheader("Chat Response:")
            loader = PDFPlumberLoader("temp_pdf.pdf")

            # Load all pages of the PDF
            pages = loader.load()

            json_responses = []

            # Loop through all pages and print the content
            for page_number, page in enumerate(pages, start=1):
                page_content = page.page_content
                st.sidebar.text(f"Page {page_number} Content:\n{page_content}\n")

                chat_response = chat_handler(page_content)

                try:
                    json_response = json.loads(chat_response)
                    st.json(json_response)  # Display JSON on Streamlit

                    # Append the JSON response to the list
                    json_responses.append(json_response)

                except json.JSONDecodeError as e:
                    st.error(f"Error decoding JSON: {e}")

            # Combine all JSON responses into a single JSON object
            final_json_response = {}
            for response in json_responses:
                final_json_response.update(response)

            # Convert combined JSON data to a string
            final_json_string = json.dumps(final_json_response, indent=2)

            # Provide download link for the final JSON string
            st.success("All JSON data extracted successfully!")
            st.markdown(get_binary_file_downloader_html_from_string(final_json_string, 'Download Combined JSON'),
                        unsafe_allow_html=True)