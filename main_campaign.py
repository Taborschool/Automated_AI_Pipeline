# main_campaign.py
import requests
import random
import sqlite3
import os
from datetime import datetime, timezone
from openai import OpenAI
from dotenv import load_dotenv
from Generate_content import generate_blog_content
load_dotenv()


# === CONFIG ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY")
BASE_URL = "https://api.hubapi.com"
OPENAI_MODEL = "gpt-4o-mini"
client = OpenAI(api_key=OPENAI_API_KEY)

# === SETUP LOCAL DATABASE ===
def init_db():
    conn = sqlite3.connect("campaigns.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            persona TEXT,
            open_rate REAL,
            click_rate REAL,
            unsubscribe_rate REAL,
            summary TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()
def init_db():
    conn = sqlite3.connect("campaigns.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            persona TEXT,
            open_rate REAL,
            click_rate REAL,
            unsubscribe_rate REAL,
            summary TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()
    return

def create_or_update_contact(contact):
    """Create or update a contact in HubSpot."""
    url = f"{BASE_URL}/crm/v3/objects/contacts"
    headers = {"Authorization": f"Bearer {HUBSPOT_API_KEY}", "Content-Type": "application/json"}
    data = {
        "properties": {
            "email": contact["email"],
            "firstname": contact["name"],
            "persona": contact["persona"]
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"✅ Created contact: {contact['email']}")
    elif response.status_code == 409:
        print(f"ℹ️ Contact already exists: {contact['email']}")
    else:
        print(f"⚠️ HubSpot contact error: {response.text}")

def log_campaign_to_hubspot(topic, persona, summary):
    """Log campaign event in HubSpot (custom object recommended for real use)."""
    url = f"{BASE_URL}/crm/v3/objects/notes"
    headers = {"Authorization": f"Bearer {HUBSPOT_API_KEY}", "Content-Type": "application/json"}
    data = {
        "properties": {
            "hs_note_body": f"Campaign '{topic}' sent to {persona} segment.\nSummary: {summary}",
            "hs_timestamp": datetime.now(timezone.utc).isoformat()
        }
    }
    requests.post(url, headers=headers, json=data)


def simulate_performance():
    """Simulate newsletter performance metrics."""
    return {
        "open_rate": round(random.uniform(0.4, 0.8), 2),
        "click_rate": round(random.uniform(0.05, 0.25), 2),
        "unsubscribe_rate": round(random.uniform(0.0, 0.05), 2)
    }


def generate_summary(performance_data):
    """AI Summary"""
    prompt = f"""
    Analyze this newsletter performance data and summarize which persona performed best and why.
    Data: {performance_data}
    Provide 1–2 actionable suggestions for next campaign.
    """
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# === MAIN WORKFLOW ===
def run_campaign(topic):
    print(f"\n🚀 Running campaign on topic: {topic}")

    # STEP 1: Generate blog + newsletter content
    blog_content = generate_blog_content(topic)
    print("📝 Content generated successfully!")

    # STEP 2: Define contacts
    contacts = [
        {"name": "Alice", "email": "alice@agency.com", "persona": "Creative Professionals"},
        {"name": "Bob", "email": "bob@brand.com", "persona": "Marketing Executives"},
        {"name": "Carol", "email": "carol@startup.io", "persona": "Tech Entrepreneurs"}
    ]

    # STEP 3: Simulate campaign performance
    performance_data = {}
    for contact in contacts:
        metrics = simulate_performance()
        performance_data[contact["persona"]] = metrics
        print(f"\n📨 Sent newsletter to {contact['email']} ({contact['persona']})")
        print(f"Open Rate: {metrics['open_rate']*100}% | Click Rate: {metrics['click_rate']*100}% | Unsubscribe: {metrics['unsubscribe_rate']*100}%")

    # STEP 4: AI summary from OpenAI
    summary = generate_summary(performance_data)
    print("\n📊 AI Campaign Summary:\n", summary)

    # STEP 5: Save to local database
    conn = sqlite3.connect("campaigns.db")
    c = conn.cursor()
    for persona, data in performance_data.items():
        c.execute("""
            INSERT INTO campaigns (topic, persona, open_rate, click_rate, unsubscribe_rate, summary, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (topic, persona, data["open_rate"], data["click_rate"], data["unsubscribe_rate"], summary, datetime.now(timezone.utc).isoformat()))
    conn.commit()
    conn.close()

    # STEP 6: Return structured data for dashboard
    return {
        "topic": topic,
        "outline": blog_content.get("outline"),
        "blog_draft": blog_content.get("blog_draft"),
        "newsletters": blog_content.get("newsletters"),
        "performance": performance_data,
        "summary": summary
    }

if __name__ == "__main__":
    init_db()
    topic = input("Enter your campaign topic: ")
    run_campaign(topic)
