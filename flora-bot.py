import os
import requests
from flask import Flask, request, jsonify

# WhatsApp API Credentials
WHATSAPP_PHONE_ID = "543517102183346"
WHATSAPP_ACCESS_TOKEN = "EAAJIJSGjDzQBO00QCGUWZCbxyNlXmZBwB950uxbrmZCZBXCY2un4LVxTRSNp2RGEEQ8C58GYDtprIvl77uZAspKpmNHXwyxcIDaOxqf4Jeda9ACaGrUWLZBPmnMUFZAW9F48jh4EvI9uHQZCKIZBMQBUj472I1ZCQ2SmZAzC0QdZBrx3h1kOFt90bhXl5FPizpr6vNUZC1FcYzLRvbR5R7oux6yB5zRAErYB0rycPMAOe5nQa"
WHATSAPP_API_URL = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_ID}/messages"

# Webhook Verify Token
VERIFY_TOKEN = "FestivalFloreceSecret"  # Choose a custom string

app = Flask(__name__)

# Privacy Policy Route
@app.route('/privacy-policy', methods=['GET'])
def privacy_policy():
    return """
    <html>
    <head><title>Privacy Policy</title></head>
    <body>
        <h1>Privacy Policy for Festival Florece</h1>
        <p>Festival Florece does not collect, store, or share any personal data. All interactions are processed in real-time and not retained.</p>
        <p>For inquiries, contact us at festivalflorece.com.</p>
    </body>
    </html>
    """, 200

class FLORA:
    def __init__(self):
        self.name = "Festival Florece Assistant"
        self.role = "Your official assistant for Festival Florece & Premios Florece"
        self.personality = "Helpful and engaging, providing official festival information"
        self.features = {
            "schedule": "The festival schedule includes various performances, workshops, and ceremonies. Let me know if you're looking for a specific event!",
            "ticketing": "Tickets can be purchased online or at the entrance. There are different categories, including VIP and general admission.",
            "venue_info": "The festival is held at multiple venues. You can check the interactive map for stage locations, restrooms, and food stalls.",
            "vendor_support": "Vendors and sponsors can set up booths, and I can provide assistance with logistics, payments, and placements.",
            "social_media": "Follow our official pages on Instagram, Facebook, and Twitter for live updates and announcements.",
            "emergency_support": "For emergencies, visit the first aid station or contact festival security. Lost & found is located at the information booth."
        }
    
    def get_info(self, feature):
        return self.features.get(feature, "I'm here to help! Let me know what you need information on.")
    
    def handle_query(self, query):
        query = query.lower()
        print(f"Received query: {query}")  # Debugging line

        keywords = {
            "schedule": ["schedule", "events", "performances", "workshops"],
            "ticketing": ["ticket", "pass", "entry", "admission"],
            "venue_info": ["venue", "location", "map", "directions"],
            "vendor_support": ["vendor", "sponsor", "booth", "logistics"],
            "social_media": ["social media", "instagram", "facebook", "twitter"],
            "emergency_support": ["emergency", "first aid", "lost & found", "security"]
        }
        
        for feature, words in keywords.items():
            if any(word in query for word in words):
                return self.get_info(feature)
        
        return "I'm here to help! Let me know what you need information on."

flora = FLORA()

@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        data = request.get_json()
        user_input = data.get('q', '')
    else:
        user_input = request.args.get('q', '')

    response = flora.handle_query(user_input)
    return jsonify({"response": response})

# WhatsApp Webhook Verification
@app.route('/whatsapp-webhook', methods=['GET', 'POST'])
def whatsapp_webhook():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == VERIFY_TOKEN:
            return challenge, 200
        return "Verification failed", 403
    
    data = request.get_json()
    if "messages" in data.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {}):
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        sender_number = message["from"]
        user_text = message["text"]["body"]
        response_text = flora.handle_query(user_text)
        send_whatsapp_message(sender_number, response_text)
    return jsonify({"status": "received"})

def send_whatsapp_message(to, message):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": message},
        "type": "text"
    }
    requests.post(WHATSAPP_API_URL, json=payload, headers=headers)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # Render uses dynamic ports
    app.run(host="0.0.0.0", port=port)

@app.route("/", methods=['GET'])
def home():
    return """
    <html>
    <head><title>Festival Florece Assistant</title></head>
    <body>
        <h1>Welcome to the Festival Florece Assistant</h1>
        <p>This is the official assistant for Festival Florece & Premios Florece.</p>
        <p>For WhatsApp support, message us directly.</p>
    </body>
    </html>
    """, 200
