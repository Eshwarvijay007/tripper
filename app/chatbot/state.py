from typing import Dict, List, Optional, Any
from langgraph.graph import MessagesState

class TripState(MessagesState):
    summary: str = ""
    history: List[Dict] = []   # store last 4 messages (role + content)
    query: str = ""
    intent: Optional[str] = None
    preferences: Dict[str, Any] = {}
    missing_fields: List[str] = []
    answer: Optional[str] = None
    itinerary_done: bool = False
    final_output: Optional[Dict[str, Any]] = None
    trip_plan: Optional[Dict[str, Any]] = None  # For storing raw trip plan data
    
    def __init__(self, **data):
        """Initialize state with proper defaults"""
        # Set defaults for missing fields
        defaults = {
            "summary": "",
            "history": [],
            "query": "",
            "intent": None,
            "preferences": {},
            "missing_fields": [],
            "answer": None,
            "itinerary_done": False,
            "final_output": None,
            "trip_plan": None
        }
        
        # Merge defaults with provided data
        for key, default_value in defaults.items():
            if key not in data:
                data[key] = default_value
        
        super().__init__(**data)
    
    def update_preferences(self, new_prefs: Dict[str, Any]) -> None:
        """Update preferences while preserving existing values"""
        if not hasattr(self, 'preferences') or not self.preferences:
            self.preferences = {}
        
        for key, value in new_prefs.items():
            if value is not None:  # Only update if new value is not None
                self.preferences[key] = value
    
    def add_message_to_history(self, role: str, content: str) -> None:
        """Add a message to history and maintain last 4 messages"""
        if not hasattr(self, 'history') or not self.history:
            self.history = []
            
        self.history.append({"role": role, "content": content})
        if len(self.history) > 4:
            self.history = self.history[-4:]
    