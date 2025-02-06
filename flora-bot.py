from flask import Flask, request, jsonify

class FLORA:
    def __init__(self):
        self.name = "FLORA"
        self.role = "Festival AI Assistant for Festival Florece & Premios Florece"
        self.personality = "Friendly, energetic, and helpful"
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

app = Flask(__name__)
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

if __name__ == '__main__':
    app.run(debug=True)
