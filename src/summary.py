import openai

# Replace with your actual OpenAI API key
openai.api_key = 'your-api-key-here'

def summarize_paragraph(paragraph):
    response = openai.Completion.create(
        engine="gpt-4",  # You can use other engines like "gpt-3.5-turbo"
        prompt=f"Summarize the following paragraph:\n\n{paragraph}",
        max_tokens=1000,  # Adjust as needed
        n=1,
        stop=None,
        temperature=0.5,
    )
    summary = response.choices[0].text.strip()
    return summary

# Example paragraph to summarize
paragraph = """
OpenAI's mission is to ensure that artificial general intelligence (AGI) benefits all of humanity. OpenAI will build safe and useful AI, or help others achieve this. OpenAI will be transparent about its progress and challenges and work with others in the AI community to address global challenges. OpenAI aims to directly build safe and beneficial AI, or to help others achieve this outcome.
"""

summary = summarize_paragraph(paragraph)
print("Summary:", summary)