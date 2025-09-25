import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

class ExtractedPassenger(BaseModel):
    pclass: int = Field(..., description="1, 2, or 3")
    name: str = Field(..., description="Passenger name")
    sex: str = Field(..., description="male or female")
    age: float | None = None
    sibsp: int = Field(default=0, description="Number of siblings/spouses")
    parch: int = Field(default=0, description="Number of parents/children")
    fare: float | None = None
    embarked: str = Field(default="S", description="Port of embarkation: C, Q, or S")

class ExtractionResult(BaseModel):
    passenger: ExtractedPassenger
    reasoning: str

SYSTEM_PROMPT = (
    "You extract Titanic passenger info from a user's natural language message.\n"
    "ONLY process messages about Titanic passengers. If the message is not about a passenger, return is_relevant: false.\n"
    "REQUIRED fields (never null): pclass (1|2|3), name (string), sex (male|female)\n"
    "OPTIONAL fields (can be null): age (number), fare (number)\n"
    "DEFAULT fields: sibsp=0, parch=0, embarked='S'\n"
    "IMPORTANT EXTRACTION RULES:\n"
    "- 'first class' or '1st class' = pclass: 1\n"
    "- 'second class' or '2nd class' = pclass: 2\n"
    "- 'third class' or '3rd class' = pclass: 3\n"
    "- 'girl' or 'woman' or 'female' = sex: 'female'\n"
    "- 'boy' or 'man' or 'male' = sex: 'male'\n"
    "- 'Cherbourg' = embarked: 'C'\n"
    "- 'Queenstown' = embarked: 'Q'\n"
    "- 'Southampton' = embarked: 'S'\n"
    "- Extract age numbers (e.g., '8 years old' = age: 8)\n"
    "- Extract fare numbers (e.g., '30 pounds' = fare: 30)\n"
    "Always provide a name, even if generic like 'Unknown Passenger'.\n"
    "Always provide a sex, infer from context if needed.\n"
    "Always provide a pclass, infer from context if needed.\n"
    "Return valid JSON with keys: is_relevant (boolean), passenger (object), reasoning (string)."
)

USER_TEMPLATE = (
    "Message: {message}\n"
    "Output strictly in JSON with keys: is_relevant (boolean), passenger (object), reasoning (string)."
)

def apply_manual_extraction_rules(message: str, passenger_data: dict) -> dict:
    """Apply manual extraction rules as fallback when LLM fails"""
    import re
    
    # Default values
    result = {
        "pclass": 3,
        "name": "Unknown Passenger",
        "sex": "unknown",
        "age": None,
        "sibsp": 0,
        "parch": 0,
        "fare": None,
        "embarked": "S"
    }
    
    # Update with existing data
    result.update(passenger_data)
    
    message_lower = message.lower()
    
    # Extract class
    if "first class" in message_lower or "1st class" in message_lower:
        result["pclass"] = 1
    elif "second class" in message_lower or "2nd class" in message_lower:
        result["pclass"] = 2
    elif "third class" in message_lower or "3rd class" in message_lower:
        result["pclass"] = 3
    
    # Extract sex
    if any(word in message_lower for word in ["girl", "woman", "female", "lady", "mother", "daughter", "miss", "ms", "mrs"]):
        result["sex"] = "female"
    elif any(word in message_lower for word in ["boy", "man", "male", "gentleman", "father", "son", "captain", "mr", "mister", "sir", "mr", "mister", "captain"]):
        result["sex"] = "male"
    
    # Extract age
    age_match = re.search(r'(\d+)\s*years?\s*old', message_lower)
    if age_match:
        result["age"] = float(age_match.group(1))
    
    # Extract fare
    fare_match = re.search(r'(\d+(?:\.\d+)?)\s*pounds?', message_lower)
    if fare_match:
        result["fare"] = float(fare_match.group(1))
    
    # Extract embarked port
    if "cherbourg" in message_lower:
        result["embarked"] = "C"
    elif "queenstown" in message_lower:
        result["embarked"] = "Q"
    elif "southampton" in message_lower:
        result["embarked"] = "S"
    
    # Extract family relationships
    if "with her parents" in message_lower or "with his parents" in message_lower:
        result["parch"] = 2  # Parents
    elif "with parents" in message_lower:
        result["parch"] = 2
    elif "traveling alone" in message_lower or "alone" in message_lower:
        result["sibsp"] = 0
        result["parch"] = 0
    
    return result

async def extract_passenger_from_message(message: str) -> ExtractionResult:
    llm = ChatOpenAI(
        model=OPENAI_MODEL, 
        temperature=0.2,
        api_key=OPENAI_API_KEY
    )
    prompt = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": USER_TEMPLATE.format(message=message)},
    ]
    resp = await llm.ainvoke(prompt)
    content = resp.content
    
    print(f"LLM Response: {content}")
    
    import json
    try:
        data = json.loads(content)
        print(f"Parsed JSON: {data}")
        
        # Check if the message is relevant to Titanic passengers
        is_relevant = data.get("is_relevant", True)
        if not is_relevant:
            raise ValueError("Message is not about a Titanic passenger")
        
        passenger_data = data["passenger"]
        print(f"Passenger data from LLM: {passenger_data}")
        
        # Apply manual extraction rules as fallback
        passenger_data = apply_manual_extraction_rules(message, passenger_data)
        print(f"Passenger data after manual rules: {passenger_data}")
        
        # Ensure required fields have defaults
        if not passenger_data.get("name"):
            passenger_data["name"] = "Unknown Passenger"
        if not passenger_data.get("sex"):
            passenger_data["sex"] = "unknown"
        if not passenger_data.get("pclass"):
            passenger_data["pclass"] = 3  # Default to third class
        
        passenger = ExtractedPassenger(**passenger_data)
        reasoning = data.get("reasoning", "Extracted passenger information from natural language")
        return ExtractionResult(passenger=passenger, reasoning=reasoning)
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        print(f"LLM parsing error: {e}")
        # Check if it's a relevance error
        if "not about a Titanic passenger" in str(e):
            raise ValueError("This message is not about a Titanic passenger. Please ask about a specific passenger on the Titanic.")
        
        # Fallback: create a basic passenger with manual extraction
        fallback_passenger = apply_manual_extraction_rules(message, {})
        return ExtractionResult(
            passenger=ExtractedPassenger(**fallback_passenger),
            reasoning=f"Failed to parse LLM response, using manual extraction. Error: {str(e)}"
        )
