import openai
import json

openai.api_key = "YOUR_OPENAI_API_KEY"

topic = "AI in creative automation"
personas = [
    "Creative Professionals",
    "Small Agency Owners",
    "Tech-Savvy Freelancers"
]

prompt = f"""
Write a blog post outline and a 500-word draft about '{topic}'.
Then write three newsletter versions, each tailored for:
1. Creative Professionals
2. Small Agency Owners
3. Tech-Savvy Freelancers
Format output as JSON.
"""

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7
)

# Save to file
with open("content/blog_campaign.json", "w") as f:
    f.write(response.choices[0].message['content'])