import openai

openai.api_key = "sk-1234567890abcdef1234567890abcdef1234567890abcdef"
client = openai.OpenAI()

def generate_response(prompt):
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
