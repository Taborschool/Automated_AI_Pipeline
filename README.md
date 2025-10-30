# Automated_AI_Pipeline
Palona AI project 
Flow Chart: 

User enters a topic → Frontend sends request to Flask API.

Flask API triggers the Campaign Workflow Engine.

Workflow Engine:

Calls OpenAI for content.

Simulates performance.

Calls OpenAI for campaign summary.

Saves results to SQLite.

Optionally updates HubSpot.

Workflow Engine returns structured JSON → Frontend parses it.

Dashboard displays content in pre-defined boxes and renders performance charts.
Dashboard visualization of:  
- Outline
- Blog Draft
- Newletters
- AI summary
- Performance Chart 
TO WORK: call app.py, and set OPENAI and GITHUB API keys prior! 

MAIN ARCHIECTURE:
generate_blog_content(topic) -> Calls OpenAI to generate content.

simulate_performance() -> Generates random metrics.

generate_summary(performance_data) -> Calls OpenAI to summarize mock data and find improvements. 

