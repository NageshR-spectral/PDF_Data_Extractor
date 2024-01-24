import openai
import base64


# openai.api_key = "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"

def chat_handler(text):
    model_engine = "gpt-3.5-turbo"  # Update with your desired OpenAI model
    content = f"""You are a helpful assistant that provides information about PDFs and images.\n{text} is the text extracted from the pdf.\n Now your task is to analyze the text provided and provide information based on the analysis.\n Make sure the output that user want is clean and usable for business purposes.\n Do not add unnecessary content if there is no answer for the question.\n Also make sure the font remains the same in the output."""
    
    prompt = """provide the important content in json format.\n Make sure the output that user want is clean and usable for business purposes.\n Do not add unnecessary content if there is no answer for the question.\n Also make sure the font remains the same in the output."""

    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": content},
            {"role": "user", "content": prompt},
        ],
    )
    return response['choices'][0]['message']['content']

def get_binary_file_downloader_html_from_string(json_string, file_label='File'):
    bin_str = base64.b64encode(json_string.encode()).decode()
    href = f'<a href="data:application/json;base64,{bin_str}" download="{file_label}.json">{file_label}</a>'
    return href