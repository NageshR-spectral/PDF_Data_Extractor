import openai
import base64

openai_api_key = "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"
# openai.api_key = "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"

def chat_handler(text):
    model_engine = "gpt-3.5-turbo"  # Update with your desired OpenAI model
    content = """You are an expert in insurance field and an helpful assistant who analyze the text data extracted from the pdf or images and provides the output in JSON format.\nNow your task is to analyze the provided text and provide the output in JSON format based on your analysis.\nIt is important to make sure the output is clean and usable for business purposes.\nMaintain consistency in output format by preserving the sequence of extracted data.\nEnsure that the JSON output remains uniform across different inputs.\nIf there is no content, then keep the value null.\nMake sure the font remains the same while generating the output."""
    
    prompt = f"""{text} is the text extracted from the pdf.\nNow your task is to analyze the provided text and provide the output in JSON format based on your analysis.\nPrioritize clear formatting and concise representation of data to enhance the user experience and business purposes.\nMaintain consistency in output format by preserving the sequence of extracted data.\nEnsure that the JSON output remains uniform across different inputs.\nDo not add unnecessary content outside the text data provided to you.\nBe precise while creating the JSON because this output will be used for business purposes.\nAlso make sure the font remains the same in the output."""

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