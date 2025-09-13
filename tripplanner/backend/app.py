
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class ItineraryRequest(BaseModel):
    prompt: str

@app.post("/api/generate-itinerary")
def generate_itinerary(request: ItineraryRequest):
    # In a real application, you would use a library like OpenAI's GPT-3
    # or Google's Gemini to generate the itinerary based on the prompt.
    # For now, we will return a hardcoded sample itinerary.
    itinerary = {
        "title": "5-Day Andalusian Road Trip Adventure",
        "description": "A whirlwind tour of Southern Spain's most iconic cities.",
        "days": [
            {
                "day": 1,
                "title": "Arrival in Seville & Flamenco",
                "description": "Arrive in Seville, check into your hotel, and immerse yourself in the local culture with a traditional flamenco show.",
                "activities": [
                    {
                        "time": "Afternoon",
                        "description": "Arrive at Seville Airport (SVQ), pick up your rental car, and check into your hotel.",
                        "location": {
                            "name": "Seville Airport",
                            "lat": 37.4180,
                            "lng": -5.8931
                        }
                    },
                    {
                        "time": "Evening",
                        "description": "Experience an authentic flamenco show in the Triana neighborhood.",
                        "location": {
                            "name": "Triana, Seville",
                            "lat": 37.3830,
                            "lng": -6.0011
                        }
                    }
                ],
                "property_suggestions": [
                    {
                        "name": "Hotel Alfonso XIII",
                        "type": "Luxury Hotel",
                        "price": "$500/night"
                    },
                    {
                        "name": "EME Catedral Hotel",
                        "type": "Boutique Hotel",
                        "price": "$300/night"
                    }
                ]
            },
            {
                "day": 2,
                "title": "Seville's Historic Heart",
                "description": "Explore the rich history of Seville with visits to the Alcázar and the Cathedral.",
                "activities": [
                    {
                        "time": "Morning",
                        "description": "Visit the Royal Alcázar of Seville, a stunning palace complex.",
                        "location": {
                            "name": "Royal Alcázar of Seville",
                            "lat": 37.3826,
                            "lng": -5.9900
                        }
                    },
                    {
                        "time": "Afternoon",
                        "description": "Climb the Giralda tower for panoramic views of the city.",
                        "location": {
                            "name": "Giralda",
                            "lat": 37.3862,
                            "lng": -5.9925
                        }
                    }
                ],
                "property_suggestions": []
            }
        ]
    }
    return itinerary

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
