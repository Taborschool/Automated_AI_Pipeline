from openai import OpenAI
import json
from dotenv import load_dotenv
import os



load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
print("OpenAI client ready!")

def generate_blog_content(topic):
    prompt = f"""
    You are an expert Marketer and Content Creator.
    Write a blog post outline and a short-form draft (400-600 words) on the topic '{topic}'.
    Then, create three newsletter versions for these personas:
    1. Creative Professionals
    2. Marketing Executives
    3. Tech Entrepreneurs
    Newsletters should be 100-150 words, tailored for each persona.
    Output as JSON only ,no explanations or extra text. MAke sure the JSON is properly formatted:
    {{
        "outline": ...,
        "blog_draft": ...,
        "newsletters": {{
            "Creative Professionals": "...",
            "Marketing Executives": "...",
            "Tech Entrepreneurs": "..."
        }}
    }}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=3000
    )
    content = response.choices[0].message.content.strip()

    try:
        blog_json = json.loads(content)
    except json.JSONDecodeError:
        print("Failed to parse JSON from the response. returning raw content.")
        blog_json = {"raw_content": content}
    return blog_json


#topic = input("Enter the campaign topic: ")
#blog_json = generate_blog_content()
#print(blog_json)
