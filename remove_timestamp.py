import re

def remove_timestamp(text):
    # 使用正則表達式去掉時間戳
    cleaned_text = re.sub(r'\[\d{2}:\d{2}:\d{2}\.\d{3} -> \d{2}:\d{2}:\d{2}\.\d{3}\] ', '', text)
    return cleaned_text

if __name__ == "__main__":
    
    input_file = "./transcript.txt"
    output_file = "./transcript_notimestamp.txt"
    
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            cleaned_line = remove_timestamp(line)
            outfile.write(cleaned_line)
            