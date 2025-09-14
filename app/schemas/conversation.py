from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator, model_validator

from app.schemas.common import Location, DateRange, Money


class ConversationStage(str, Enum):
    """Stages of the conversation flow"""
    INITIAL = "initial"
    GATHERING_DESTINATION = "gathering_destination"
    GATHERING_DATES = "gathering_dates"
    GATHERING_PREFERENCES = "gathering_preferences"
    PLANNING = "planning"
    COMPLETED = "completed"
    ERROR = "error"


class QuestionType(str, Enum):
    """Types of questions that can be asked"""
    DESTINATION = "destination"
    DATES = "dates"
    DURATION = "duration"
    INTERESTS = "interests"
    PACE = "pace"
    BUDGET = "budget"
    CLARIFICATION = "clarification"
    DISAMBIGUATION = "disambiguation"


class ValidationStatus(str, Enum):
    """Validation status for trip parameters"""
    VALID = "valid"
    INCOMPLETE = "incomplete"
    INVALID = "invalid"
    NEEDS_CLARIFICATION = "needs_clarification"


class ErrorType(str, Enum):
    """Types of errors that can occur"""
    VALIDATION_ERROR = "validation_error"
    API_ERROR = "api_error"
    LLM_ERROR = "llm_error"
    STATE_ERROR = "state_error"


class ProcessingError(BaseModel):
    """Represents an error that occurred during processing"""
    error_type: ErrorType
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    recoverable: bool = True
    context: Optional[Dict[str, Any]] = None


class ValidationRules(BaseModel):
    """Validation rules for questions"""
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    pattern: Optional[str] = None
    allowed_values: Optional[List[str]] = None
    required: bool = True


class Question(BaseModel):
    """Represents a question to ask the user"""
    id: str
    text: str
    question_type: QuestionType
    required: bool = True
    options: Optional[List[str]] = None
    validation_rules: Optional[ValidationRules] = None
    context: Optional[str] = None
    
    @field_validator('id')
    @classmethod
    def validate_id(cls, v):
        if not v or not v.strip():
            raise ValueError('Question ID cannot be empty')
        return v.strip()
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError('Question text cannot be empty')
        return v.strip()


class QuestionResponse(BaseModel):
    """Represents a user's response to a question"""
    question_id: str
    response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    validated: bool = False
    validation_errors: List[str] = Field(default_factory=list)


class BudgetRange(BaseModel):
    """Budget range for the trip"""
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    currency: str = "INR"
    per_person: bool = True
    
    @field_validator('min_amount', 'max_amount')
    @classmethod
    def validate_amounts(cls, v):
        if v is not None and v < 0:
            raise ValueError('Budget amounts must be non-negative')
        return v
    
    @model_validator(mode='after')
    def validate_range(self):
        if self.min_amount is not None and self.max_amount is not None and self.min_amount > self.max_amount:
            raise ValueError('Minimum budget cannot be greater than maximum budget')
        return self


class UserPreferences(BaseModel):
    """User preferences for trip planning"""
    interests: List[str] = Field(default_factory=list)
    pace: Optional[str] = None  # "relaxed" | "moderate" | "packed"
    with_kids: bool = False
    must_do: List[str] = Field(default_factory=list)
    avoid: List[str] = Field(default_factory=list)
    accessibility_needs: List[str] = Field(default_factory=list)
    dietary_restrictions: List[str] = Field(default_factory=list)


class TripParameters(BaseModel):
    """Core trip planning parameters"""
    origin: Optional[Location] = None
    destinations: List[Location] = Field(default_factory=list)
    date_range: Optional[DateRange] = None
    nights: Optional[int] = None
    budget_range: Optional[BudgetRange] = None
    user_preferences: UserPreferences = Field(default_factory=UserPreferences)
    
    @field_validator('nights')
    @classmethod
    def validate_nights(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Number of nights must be positive')
        return v
    
    @field_validator('destinations')
    @classmethod
    def validate_destinations(cls, v):
        if len(v) > 10:  # Reasonable limit
            raise ValueError('Too many destinations (maximum 10)')
        return v
    
    def is_complete(self) -> bool:
        """Check if trip parameters are complete enough for planning"""
        has_destination = len(self.destinations) > 0
        has_timing = self.date_range is not None or self.nights is not None
        return has_destination and has_timing
    
    def get_missing_required_fields(self) -> List[str]:
        """Get list of missing required fields"""
        missing = []
        if not self.destinations:
            missing.append("destination")
        if not self.date_range and not self.nights:
            missing.append("dates_or_duration")
        return missing
    
    def get_completeness_score(self) -> float:
        """Get a score (0-1) indicating how complete the parameters are"""
        total_fields = 6  # destinations, timing, origin, budget, interests, pace
        completed_fields = 0
        
        if self.destinations:
            completed_fields += 1
        if self.date_range or self.nights:
            completed_fields += 1
        if self.origin:
            completed_fields += 1
        if self.budget_range:
            completed_fields += 1
        if self.user_preferences.interests:
            completed_fields += 1
        if self.user_preferences.pace:
            completed_fields += 1
            
        return completed_fields / total_fields


class ConversationContext(BaseModel):
    """Context information for the conversation"""
    last_user_input: str = ""
    last_agent_response: str = ""
    turn_number: int = 0
    disambiguation_context: Optional[Dict[str, Any]] = None
    processing_notes: List[str] = Field(default_factory=list)


class ConversationState(BaseModel):
    """Complete conversation state for persistent storage"""
    conversation_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Trip planning state
    trip_params: TripParameters = Field(default_factory=TripParameters)
    validation_status: ValidationStatus = ValidationStatus.INCOMPLETE
    
    # Conversation flow
    current_stage: ConversationStage = ConversationStage.INITIAL
    pending_questions: List[Question] = Field(default_factory=list)
    question_history: List[QuestionResponse] = Field(default_factory=list)
    
    # Context and preferences
    conversation_context: ConversationContext = Field(default_factory=ConversationContext)
    
    # Error tracking
    errors: List[ProcessingError] = Field(default_factory=list)
    
    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @field_validator('conversation_id')
    @classmethod
    def validate_conversation_id(cls, v):
        if not v or not v.strip():
            raise ValueError('Conversation ID cannot be empty')
        return v.strip()
    
    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow()
    
    def add_question_response(self, question_id: str, response: str) -> None:
        """Add a user response to a question"""
        question_response = QuestionResponse(
            question_id=question_id,
            response=response
        )
        self.question_history.append(question_response)
        self.update_timestamp()
    
    def get_last_question_response(self) -> Optional[QuestionResponse]:
        """Get the most recent question response"""
        return self.question_history[-1] if self.question_history else None
    
    def add_error(self, error_type: ErrorType, message: str, recoverable: bool = True, context: Optional[Dict[str, Any]] = None) -> None:
        """Add an error to the conversation state"""
        error = ProcessingError(
            error_type=error_type,
            message=message,
            recoverable=recoverable,
            context=context
        )
        self.errors.append(error)
        self.update_timestamp()
    
    def has_unrecoverable_errors(self) -> bool:
        """Check if there are any unrecoverable errors"""
        return any(not error.recoverable for error in self.errors)
    
    def clear_pending_questions(self) -> None:
        """Clear all pending questions"""
        self.pending_questions.clear()
        self.update_timestamp()
    
    def add_pending_question(self, question: Question) -> None:
        """Add a question to the pending list"""
        self.pending_questions.append(question)
        self.update_timestamp()
    
    def get_validation_errors(self) -> List[str]:
        """Get all validation errors from the current state"""
        errors = []
        
        # Check trip parameters completeness
        if self.validation_status == ValidationStatus.INCOMPLETE:
            missing_fields = self.trip_params.get_missing_required_fields()
            if missing_fields:
                errors.append(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Check for validation errors in question responses
        for response in self.question_history:
            if response.validation_errors:
                errors.extend(response.validation_errors)
        
        return errors
    
    def is_ready_for_planning(self) -> bool:
        """Check if the conversation state is ready for trip planning"""
        return (
            self.trip_params.is_complete() and
            self.validation_status == ValidationStatus.VALID and
            not self.has_unrecoverable_errors()
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return self.dict()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConversationState':
        """Create instance from dictionary for deserialization"""
        return cls(**data)
    
    def to_json(self) -> str:
        """Convert to JSON string for persistence"""
        return self.json()
    
    @classmethod
    def from_json(cls, json_str: str) -> 'ConversationState':
        """Create instance from JSON string"""
        return cls.parse_raw(json_str)


# Utility functions for state management
def create_new_conversation(conversation_id: str) -> ConversationState:
    """Create a new conversation state with default values"""
    return ConversationState(conversation_id=conversation_id)


def validate_conversation_state(state: ConversationState) -> List[str]:
    """Validate conversation state and return list of validation errors"""
    errors = []
    
    try:
        # Validate the state using Pydantic validation
        state.dict()
    except Exception as e:
        errors.append(f"State validation error: {str(e)}")
    
    # Additional business logic validation
    if state.current_stage == ConversationStage.COMPLETED and not state.trip_params.is_complete():
        errors.append("Conversation marked as completed but trip parameters are incomplete")
    
    if state.validation_status == ValidationStatus.VALID and not state.trip_params.is_complete():
        errors.append("Validation status is valid but trip parameters are incomplete")
    
    return errors


def merge_trip_parameters(existing: TripParameters, updates: Dict[str, Any]) -> TripParameters:
    """Merge updates into existing trip parameters without overwriting valid data"""
    # Create a copy of existing parameters
    merged_data = existing.dict()
    
    # Merge updates, being careful not to overwrite valid data with None/empty values
    for key, value in updates.items():
        if key in merged_data:
            if value is not None and value != [] and value != "":
                if key == "destinations" and isinstance(value, list):
                    # For destinations, append new ones if they're not already present
                    existing_destinations = merged_data.get("destinations", [])
                    for dest in value:
                        if dest not in existing_destinations:
                            existing_destinations.append(dest)
                    merged_data[key] = existing_destinations
                elif key == "user_preferences" and isinstance(value, dict):
                    # Merge user preferences
                    existing_prefs = merged_data.get("user_preferences", {})
                    for pref_key, pref_value in value.items():
                        if pref_value is not None and pref_value != [] and pref_value != "":
                            existing_prefs[pref_key] = pref_value
                    merged_data[key] = existing_prefs
                else:
                    merged_data[key] = value
    
    return TripParameters(**merged_data)