import streamlit as st
import json
from langchain_community.document_loaders import PDFPlumberLoader
from utils import get_binary_file_downloader_html_from_string, chat_handler

class Main:

    def __init__(self, file_path):
        self.file_path = file_path

    def convert_pdf_to_text(self):
        st.title("PDF to Text Conversion and Chat Handling")

        # Display file path
        st.sidebar.subheader("File Information:")
        st.sidebar.text(f"File Path: {self.file_path.name}")

        # Chat Handling
        st.header("Chat Handling:")
        chat_button = st.button("Handle Chat")

        if chat_button:
            st.subheader("Chat Response:")
            loader = PDFPlumberLoader(self.file_path)

            # Load all pages of the PDF
            pages = loader.load()

            # List to store JSON responses for each page
            json_responses = []

            # Loop through all pages and print the content
            for page_number, page in enumerate(pages, start=1):
                page_content = page.page_content
                st.text(f"Page {page_number} Content:\n{page_content}\n")

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

            # Remove duplicate data from the combined JSON response
            cleaned_json_response = remove_duplicates(final_json_response)

            # Convert cleaned JSON data to a string
            cleaned_json_string = json.dumps(cleaned_json_response, indent=2)

            # Provide download link for the cleaned JSON string
            st.success("All JSON data extracted and cleaned successfully!")
            st.markdown(get_binary_file_downloader_html_from_string(cleaned_json_string, 'Download Cleaned JSON'),
                        unsafe_allow_html=True)

def remove_duplicates(json_data):
    unique_data = {}
    seen_keys = set()
    
    for key, value in json_data.items():
        if key not in seen_keys:
            unique_data[key] = value
            seen_keys.add(key)
    
    return unique_data

def main():
    st.set_page_config(page_title="PDF Processing App", page_icon="📄")

    file_path = st.file_uploader("Upload a PDF file", type=["pdf"])

    if file_path:
        main_obj = Main(file_path)
        main_obj.convert_pdf_to_text()

if __name__ == "__main__":
    main()
