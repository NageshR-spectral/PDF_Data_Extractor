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
           # Load all pages of the PDF
            pages = loader.load()

            json_responses = []

            # Determine the number of sets based on the number of pages
            num_sets = (len(pages) + 4) // 5

            # Loop through sets of pages
            for set_number in range(num_sets):
                st.sidebar.header(f"Set {set_number + 1}")

                # Get pages for the current set
                start_index = set_number * 5
                end_index = min((set_number + 1) * 5, len(pages))
                set_pages = pages[start_index:end_index]

                # Combine content of pages in the set
                set_content = "\n".join([page.page_content for page in set_pages])

                # Display the content in the sidebar
                st.sidebar.text(f"Set {set_number + 1} Content:\n{set_content}\n")

                # Process the content and display JSON response
                chat_response = chat_handler(set_content)

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