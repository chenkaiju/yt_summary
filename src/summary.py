from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import os
import tiktoken

class Summary():
    
    def __init__(self, env_path) -> None:
        
        self._env_path = env_path
        self._openai_apikey = None
        
    def read_openai_apikey(self):
        
        if self._openai_apikey:
            return self._openai_apikey
        
        if self._env_path:
            if not os.path.exists(self._env_path):
                raise FileNotFoundError(f".env file not found at {self._env_path}")
            load_dotenv(self._env_path)
        else:
            load_dotenv(find_dotenv())

        self._openai_apikey = os.getenv('OPENAI_API_KEY')

        if self._openai_apikey:
            return self._openai_apikey
        else:
            raise EnvironmentError("OPENAI_API_KEY not found in .env file")


    def count_tokens(self, text, model="gpt-4o-mini"):
        enc = tiktoken.encoding_for_model(model)
        return len(enc.encode(text))
        

    def split_text_by_tokens(self, text, max_tokens=7000, model="gpt-40-mini"):
        enc = tiktoken.encoding_for_model(model)
        tokens = enc.encode(text)
        chunks = []
        for i in range(0, len(tokens), max_tokens):
            chunk_tokens = tokens[i:i+max_tokens]
            chunk_text = enc.decode(chunk_tokens)
            chunks.append(chunk_text)
        return chunks


    def summarize_text(self, text, model="gpt-4o-mini", max_tokens=1000, temperature=0.5):
        
        client = OpenAI(
            # This is the default and can be omitted
            api_key=self.read_openai_apikey(),
        )    
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你很擅長做重點整理."},
                {"role": "user", "content": f"給我這段話的重點整理:\n\n{text}"}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message['content']


    def summarize_chunk(self, chunk, model="gpt-4o-mini"):
        
        client = OpenAI(
            # This is the default and can be omitted
            api_key=self.read_openai_apikey(),
        )    
        
        response = client.chat.completions.create(
            model=model,  # You can use other models as well
            messages=[
                {"role": "system", "content": "你很擅長做重點整理."},
                {"role": "user", "content": f"給我這段話詳細的重點整理，另外再給我三句文章裡有趣的句子:\n\n{chunk}"}
            ],
            max_tokens=1000,  # Adjust as needed
            temperature=0.5
        )
        
        summary = response.choices[0].message.content
        
        return summary
        
            
    def summarize_paragraph(self, paragraph, model="gpt-4o-mini", output_file_prefix="summary"):
                
        client = OpenAI(
                # This is the default and can be omitted
                api_key=self.read_openai_apikey(),
            )
        
        # Generate a timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create the full filename with the timestamp postfix
        output_file = f"{output_file_prefix}_{timestamp}.txt"
        
        response = client.chat.completions.create(
            model="gpt-4",  # You can use other models as well
            messages=[
                {"role": "system", "content": "你很擅長做重點整理."},
                {"role": "user", "content": f"給我這段文字的十個重點，500字左右，不含作者介紹跟業配資訊。另外再給我三句文章裡有趣的句子。用適合即時通訊軟體的格式輸出:\n\n{paragraph}"}
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


if __name__=="__main__":
    
    worker = Summary(env_path="./openai_apikey.env")
    transcript_file = "./transcript_notimestamp_long.txt"
    model = "gpt-4o-mini"
    paragraph = ""
    with open(transcript_file) as f:
        paragraph = f.read()
        content_length = len(paragraph)
    
    while content_length > 7000:
        
        # Split the long paragraph into chunks
        chunks = worker.split_text_by_tokens(text=paragraph, model=model)
        summaries = [worker.summarize_chunk(chunk, model=model) for chunk in chunks]
        paragraph = " ".join(summaries)
        print("summarized paragraph:", paragraph)
        content_length = len(paragraph)
        
    summary = worker.summarize_paragraph(paragraph, model=model, output_file_prefix="summary")
    print("Summary:", summary)
