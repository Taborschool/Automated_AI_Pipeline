import openai
import json

openai.api_key = "YOUR_OPENAI_API_KEY"

def gen_blog_content(idea, personas, output_file="content/blog_campaign.json"):
    if len(personas) == 0: 
        raise ValueError ("You must have at least one persona.") 
#persona list, and index    
    personas_list = ""
    for idx, persona in enumerate(persona, 1):
        persona_list += f"{idx}. {persona}/n"
# API Prompt     
    prompt = f"""
    you are an Expert Marketer, Write a blog post outline and a 500-600 word draft about '{idea}'.
    Then write {len(personas)} newsletter versions, each tailored for:
    '{persona_list}'
    Format output as JSON.
    """
    



response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7
)

# Save to file
    content = response.choices[0].message['content']
    with open(output_file, "w") as f:
        f.write(content)
    return content
#input variables 
idea_input = input("Enter your blog idea: ")
personas_input = input("Enter personas separated by commas: ").split(",")
personas_input = [p.strip() for p in personas_input if p.strip()]
generate_blog_content(idea_input, personas_input)
