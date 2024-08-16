from openai import OpenAI

# Replace with your actual OpenAI API key
api_key = ''
client = OpenAI(
    # This is the default and can be omitted
    api_key=api_key,
)

def summarize_paragraph(paragraph):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # You can use other models as well
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"做一個500字內的摘要:\n\n{paragraph}"}
        ],
        max_tokens=1000,  # Adjust as needed
        temperature=0.5
    )
    summary = response.choices[0].message.content.strip()
    return summary
# Example paragraph to summarize
paragraph = ""
with open('transcript.txt') as f:
    paragraph = f.read()


summary = summarize_paragraph(paragraph)
print("Summary:", summary)