from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import os

def read_openai_apikey(env_path=None):
    # Load the .env file from the specified path or default location
    if env_path:
        if not os.path.exists(env_path):
            raise FileNotFoundError(f".env file not found at {env_path}")
        load_dotenv(env_path)
    else:
        # Load default .env file using find_dotenv() to search the file automatically
        load_dotenv(find_dotenv())

    # Get the API key from the environment
    openai_apikey = os.getenv('openai_apikey')

    if openai_apikey:
        return openai_apikey
    else:
        raise EnvironmentError("openai_apikey not found in .env file")

def summarize_chunk(chunk):
    
    try:
        custom_env_path = "./openai_apikey.env"
        api_key = read_openai_apikey(custom_env_path)
        print(f"OpenAI API key: {api_key}")
    except EnvironmentError as e:
        print(e)
        
    client = OpenAI(
        # This is the default and can be omitted
        api_key=api_key,
    )

    response = client.chat.completions.create(
        model="gpt-4",  # You can use other models as well
        messages=[
            {"role": "system", "content": "你很擅長做重點整理."},
            {"role": "user", "content": f"給我這段話詳細的重點整理:\n\n{chunk}"}
        ],
        max_tokens=1000,  # Adjust as needed
        temperature=0.5
    )
    
    summary = response.choices[0].message.content
    
    return summary
    
        
def summarize_paragraph(paragraph, output_file_prefix):
    
    try:
        custom_env_path = "./openai_apikey.env"
        api_key = read_openai_apikey(custom_env_path)
        print(f"OpenAI API key: {api_key}")
    except EnvironmentError as e:
        print(e)
        
    client = OpenAI(
        # This is the default and can be omitted
        api_key=api_key,
    )
    
    # Generate a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create the full filename with the timestamp postfix
    output_file = f"{output_file_prefix}_{timestamp}.txt"
    
    response = client.chat.completions.create(
        model="gpt-4",  # You can use other models as well
        messages=[
            {"role": "system", "content": "你很擅長做重點整理."},
            {"role": "user", "content": f"給我這部影片的十個重點，500字左右，不含作者介紹跟業配資訊。另外再給我三句影片裡有趣的句子。用適合即時通訊軟體的格式輸出:\n\n{paragraph}"}
        ],
        max_tokens=1000,  # Adjust as needed
        temperature=0.5
    )
    
    summary = response.choices[0].message.content

    # Save the summary to a file with the timestamped filename
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(summary)
    
    print(f"Summary saved to {output_file}")
    return summary

def split_text(text, max_length=1500):
    # Split text into chunks of max_length tokens (approximate)
    chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    return chunks

if __name__=="__main__":
    
    paragraph = ""
    with open('transcript_notimestamp.txt') as f:
        paragraph = f.read()

    summary = summarize_paragraph(paragraph, output_file_prefix="summary")
    
    # Split the long paragraph into chunks
    # chunks = split_text(paragraph)
    # summaries = [summarize_chunk(chunk) for chunk in chunks]
    # all_summary = " ".join(summaries)
    # print("all summary:", all_summary)

    # with open("./all_summary.txt", "r", encoding="utf-8") as file:
    #     all_summary = file.read()
    # summary = summarize_paragraph(all_summary, output_file_prefix="summary")    
    print("Summary:", summary)
