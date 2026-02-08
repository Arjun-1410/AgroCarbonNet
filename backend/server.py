from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
from emergentintegrations.llm.chat import LlmChat, UserMessage
import joblib
import numpy as np
import pandas as pd
import base64
import httpx

# Import knowledge base
from crop_knowledge import (
    CROP_KNOWLEDGE, STATE_AGRI_INFO, PEST_DISEASE_CONTROL, GOVT_SCHEMES,
    get_crop_info, get_state_info
)
from weather_service import get_weather_advisory, weather_service

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'farmer_assistant')]

# Create the main app
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Get Emergent LLM Key
EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY', '')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load ML Model and Encoders
MODEL_DIR = ROOT_DIR / 'models'
DATA_DIR = ROOT_DIR / 'data'

try:
    yield_model = joblib.load(MODEL_DIR / 'yield_model.pkl')
    encoders = joblib.load(MODEL_DIR / 'encoders.pkl')
    model_stats = joblib.load(MODEL_DIR / 'model_stats.pkl')
    crop_data = pd.read_csv(DATA_DIR / 'india_crop_data.csv')
    logger.info(f"ML Model loaded successfully. Training R²: {model_stats['train_score']:.4f}")
    ML_MODEL_LOADED = True
except Exception as e:
    logger.warning(f"Could not load ML model: {e}. Using fallback predictions.")
    ML_MODEL_LOADED = False
    yield_model = None
    encoders = None
    model_stats = None
    crop_data = None

# Enhanced System Prompt - Human-like Conversational Assistant
SYSTEM_PROMPT = """You are Farmer Voice Assistant, an expert multilingual agricultural AI assistant designed specifically for Indian farmers. You communicate like a knowledgeable, caring agricultural officer who genuinely wants to help farmers succeed.

PERSONALITY & CONVERSATION STYLE:
- Be warm, empathetic, and supportive like a village elder who knows farming
- Ask clarifying questions when information is missing (max 2-3 at a time)
- Use relatable examples and comparisons farmers understand
- Share specific numbers and quantifiable benefits
- Celebrate farmer's good practices and gently correct issues

LANGUAGE RULES (CRITICAL):
- Detect the farmer's language automatically from their message
- Respond ONLY in the detected language (English, Hindi, or Telugu)
- Use simple, farmer-friendly wording with local terms
- Avoid technical jargon - explain in practical terms

STEP-BY-STEP GUIDANCE APPROACH:
When farmer asks a question:
1. First acknowledge their concern warmly
2. Ask 1-2 clarifying questions if needed (crop, location, soil, current situation)
3. Once you have enough info, provide step-by-step actionable advice
4. Always quantify benefits of your recommendations

BENEFITS ANALYSIS (ALWAYS INCLUDE):
For every recommendation, explain the tangible benefit:
- "If you reduce pesticide use by 30%, you can save Rs 2000/acre AND improve yield quality by 15%"
- "Using certified seeds costs Rs 500 more but gives Rs 5000 extra income"
- "IPM practices reduce input cost by 40% while increasing profit by 25%"
- "Drip irrigation saves 40% water and increases yield by 25-30%"

QUESTIONING PATTERNS:
If farmer says "मेरी फसल खराब हो रही है":
- "कौन सी फसल है? धान, गेहूं या कोई और?"
- "कितने दिन से यह समस्या है?"
- "क्या पत्ते पीले हैं, सूख रहे हैं, या कीड़े दिख रहे हैं?"

If farmer says "నా పంట దెబ్బతింటోంది":
- "ఏ పంట? వరి, పత్తి లేదా వేరేది?"
- "ఎన్ని రోజులుగా ఈ సమస్య ఉంది?"
- "ఆకులు పసుపు రంగులో ఉన్నాయా, ఎండిపోతున్నాయా, లేదా పురుగులు కనిపిస్తున్నాయా?"

KNOWLEDGE BASE ACCESS:
You have verified data from:
- Ministry of Agriculture & Farmers Welfare, Government of India
- ICAR (Indian Council of Agricultural Research) recommendations  
- State agricultural department guidelines
- Real-time weather data for agricultural advisories
- MSP (Minimum Support Price) 2024 data
- Historical crop production data (1997-2023)

CHART DATA REQUESTS:
When providing yield predictions or comparisons, mention:
"I can show you a chart comparing your expected yield with state and national averages."
"Would you like to see a visual breakdown of the factors affecting your yield?"

WEATHER INTEGRATION:
When location is known, provide weather-based advice:
- Current conditions and 7-day forecast impact
- Best time for spraying, irrigation, harvesting
- Storm/rain warnings for crop protection

MANDATORY RESPONSE ELEMENTS:
1. Warm acknowledgment
2. Clarifying questions OR detailed advice (not both)
3. Specific quantities (kg/ha, Rs/acre, % improvement)
4. Clear benefit statement
5. Follow-up question or next step

SAFETY DISCLAIMER (add when discussing chemicals):
Hindi: "रासायनिक दवाइयों का प्रयोग सावधानी से करें। मास्क और दस्ताने पहनें।"
Telugu: "రసాయన మందులు జాగ్రత్తగా వాడండి. మాస్క్ మరియు గ్లవ్స్ ధరించండి."
English: "Use chemicals carefully. Wear mask and gloves for protection."
"""

# Models
class ChatMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    role: str
    content: str
    language: str = "en"
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ChatRequest(BaseModel):
    session_id: str
    message: str
    language: Optional[str] = None
    farm_context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    language: str
    session_id: str
    ml_prediction: Optional[Dict[str, Any]] = None
    knowledge_context: Optional[Dict[str, Any]] = None
    weather_data: Optional[Dict[str, Any]] = None
    chart_data: Optional[Dict[str, Any]] = None

class FarmInput(BaseModel):
    crop_type: str
    soil_type: str
    season: str
    location: str  # State or District
    rainfall_mm: Optional[float] = None
    irrigation_percent: Optional[float] = None
    fertilizer_kg_ha: Optional[float] = None
    temperature_c: Optional[float] = None
    area_hectares: Optional[float] = None

class MLPrediction(BaseModel):
    predicted_yield_kg_ha: float
    predicted_yield_quintal_acre: float
    confidence_score: float
    risk_level: str
    state_avg_yield: Optional[float] = None
    national_avg_yield: Optional[float] = None
    influential_factors: List[Dict[str, Any]]
    recommendations: List[str]
    crop_info: Optional[Dict[str, Any]] = None
    comparison: str
    data_source: str = "Government of India Agricultural Statistics (2023)"

class Session(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    language: str = "en"
    farm_context: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Helper Functions
def detect_language(text: str) -> str:
    """Detect language from text"""
    telugu_chars = sum(1 for c in text if '\u0C00' <= c <= '\u0C7F')
    hindi_chars = sum(1 for c in text if '\u0900' <= c <= '\u097F')
    
    total = len(text)
    if total == 0:
        return "en"
    
    if telugu_chars / total > 0.15:
        return "te"
    elif hindi_chars / total > 0.15:
        return "hi"
    
    # Check for common Hindi words in Roman script
    hindi_words = ['kya', 'hai', 'mera', 'meri', 'kaise', 'karo', 'karna', 'fasal', 'kheti', 'pani', 'baarish']
    text_lower = text.lower()
    for word in hindi_words:
        if word in text_lower:
            return "hi"
    
    return "en"

def get_state_from_location(location: str) -> str:
    """Extract state name from location"""
    location_lower = location.lower()
    
    # District to state mapping
    district_state_map = {
        'guntur': 'andhra pradesh', 'krishna': 'andhra pradesh', 'nellore': 'andhra pradesh',
        'karimnagar': 'telangana', 'warangal': 'telangana', 'nizamabad': 'telangana',
        'ludhiana': 'punjab', 'amritsar': 'punjab', 'jalandhar': 'punjab',
        'meerut': 'uttar pradesh', 'lucknow': 'uttar pradesh', 'agra': 'uttar pradesh',
        'nagpur': 'maharashtra', 'pune': 'maharashtra', 'nashik': 'maharashtra',
        'indore': 'madhya pradesh', 'bhopal': 'madhya pradesh', 'ujjain': 'madhya pradesh',
        'ahmedabad': 'gujarat', 'rajkot': 'gujarat', 'surat': 'gujarat',
        'jaipur': 'rajasthan', 'jodhpur': 'rajasthan', 'bikaner': 'rajasthan',
        'bengaluru': 'karnataka', 'mysore': 'karnataka', 'belgaum': 'karnataka',
        'chennai': 'tamil nadu', 'coimbatore': 'tamil nadu', 'madurai': 'tamil nadu',
        'kolkata': 'west bengal', 'patna': 'bihar', 'ranchi': 'jharkhand'
    }
    
    for district, state in district_state_map.items():
        if district in location_lower:
            return state
    
    # Check if it's already a state name
    states = list(STATE_AGRI_INFO.keys())
    for state in states:
        if state in location_lower:
            return state
    
    return location_lower

def predict_yield_ml(farm_input: FarmInput) -> MLPrediction:
    """Predict crop yield using trained Random Forest model"""
    
    crop_info = get_crop_info(farm_input.crop_type)
    state_name = get_state_from_location(farm_input.location)
    state_info = get_state_info(state_name)
    
    # Default values based on knowledge base
    default_rainfall = 900
    default_irrigation = 60
    default_fertilizer = 150
    default_temp = 27
    
    if state_info:
        default_rainfall = state_info['rainfall_mm']['avg']
    
    if crop_info:
        yield_range = crop_info.get('yield_range_kg_ha', {'avg': 3000})
        default_yield = yield_range['avg']
    else:
        default_yield = 3000
    
    rainfall = farm_input.rainfall_mm or default_rainfall
    irrigation = farm_input.irrigation_percent or default_irrigation
    fertilizer = farm_input.fertilizer_kg_ha or default_fertilizer
    temperature = farm_input.temperature_c or default_temp
    
    predicted_yield = default_yield
    confidence = 0.75
    
    if ML_MODEL_LOADED and yield_model is not None:
        try:
            # Prepare features for model
            crop_key = farm_input.crop_type.lower().strip()
            if crop_key in encoders['Crop'].classes_:
                crop_encoded = encoders['Crop'].transform([crop_key.title()])[0]
            else:
                crop_encoded = 0
            
            soil_key = farm_input.soil_type.lower().strip()
            if soil_key in [s.lower() for s in encoders['Soil_Type'].classes_]:
                soil_encoded = encoders['Soil_Type'].transform([soil_key.title()])[0]
            else:
                soil_encoded = 0
            
            season_key = farm_input.season.lower().strip()
            if season_key in [s.lower() for s in encoders['Season'].classes_]:
                season_encoded = encoders['Season'].transform([season_key.title()])[0]
            else:
                season_encoded = 0
            
            # Find matching state/district in training data
            state_encoded = 0
            district_encoded = 0
            
            # Create feature array
            features = np.array([[
                state_encoded, district_encoded, crop_encoded,
                season_encoded, soil_encoded,
                rainfall, irrigation, fertilizer, temperature
            ]])
            
            predicted_yield = yield_model.predict(features)[0]
            confidence = min(0.92, model_stats['test_score'])
            
        except Exception as e:
            logger.warning(f"ML prediction error: {e}. Using knowledge-based estimate.")
            # Fall back to knowledge-based calculation
            if crop_info:
                yield_range = crop_info['yield_range_kg_ha']
                base_yield = yield_range['avg']
                
                # Adjust based on factors
                irrigation_factor = 1.0 + (irrigation - 50) / 100 * 0.3
                rainfall_factor = 1.0 if 600 < rainfall < 1200 else 0.85
                fertilizer_factor = 1.0 + (fertilizer - 100) / 200 * 0.2
                
                predicted_yield = base_yield * irrigation_factor * rainfall_factor * fertilizer_factor
                predicted_yield = max(yield_range['min'], min(yield_range['max'], predicted_yield))
    
    # Convert to quintal/acre
    predicted_yield_quintal_acre = predicted_yield * 0.0404686 / 10  # kg/ha to quintal/acre
    
    # Calculate risk level
    risk_score = 0
    risk_factors = []
    
    if irrigation < 40:
        risk_score += 2
        risk_factors.append("Low irrigation coverage")
    if rainfall < 500:
        risk_score += 2
        risk_factors.append("Insufficient rainfall")
    elif rainfall > 1500:
        risk_score += 1
        risk_factors.append("Excess rainfall - flood risk")
    if fertilizer < 80:
        risk_score += 1
        risk_factors.append("Low fertilizer application")
    
    if risk_score >= 3:
        risk_level = "High"
    elif risk_score >= 1:
        risk_level = "Medium"
    else:
        risk_level = "Low"
    
    # Get state and national averages from data
    state_avg = None
    national_avg = None
    
    if crop_data is not None:
        crop_match = crop_data[crop_data['Crop'].str.lower() == farm_input.crop_type.lower()]
        if not crop_match.empty:
            national_avg = crop_match['Yield_Kg_Ha'].mean()
            state_match = crop_match[crop_match['State'].str.lower().str.contains(state_name[:5])]
            if not state_match.empty:
                state_avg = state_match['Yield_Kg_Ha'].mean()
    
    # Generate influential factors
    factors = []
    
    if irrigation >= 70:
        factors.append({"factor": "Irrigation", "impact": "Positive", "detail": f"{irrigation}% coverage - excellent water availability"})
    elif irrigation >= 40:
        factors.append({"factor": "Irrigation", "impact": "Moderate", "detail": f"{irrigation}% coverage - adequate but can improve"})
    else:
        factors.append({"factor": "Irrigation", "impact": "Negative", "detail": f"{irrigation}% coverage - insufficient, consider bore wells"})
    
    if 600 < rainfall < 1200:
        factors.append({"factor": "Rainfall", "impact": "Positive", "detail": f"{rainfall}mm - optimal range"})
    else:
        factors.append({"factor": "Rainfall", "impact": "Risk", "detail": f"{rainfall}mm - {'below' if rainfall < 600 else 'above'} optimal"})
    
    if crop_info:
        optimal_soils = crop_info.get('optimal_soil', [])
        if farm_input.soil_type.title() in optimal_soils:
            factors.append({"factor": "Soil Type", "impact": "Positive", "detail": f"{farm_input.soil_type} is ideal for {farm_input.crop_type}"})
        else:
            factors.append({"factor": "Soil Type", "impact": "Moderate", "detail": f"{farm_input.soil_type} - consider soil amendments"})
    
    factors.append({"factor": "Fertilizer", "impact": "Positive" if fertilizer >= 120 else "Moderate", 
                   "detail": f"{fertilizer} kg/ha applied"})
    
    # Generate recommendations
    recommendations = []
    
    if crop_info:
        fert_rec = crop_info.get('fertilizer_recommendation', {})
        recommendations.append(f"Recommended fertilizer: N-{fert_rec.get('N', '120 kg/ha')}, P-{fert_rec.get('P', '60 kg/ha')}, K-{fert_rec.get('K', '40 kg/ha')}")
        
        if crop_info.get('tips'):
            recommendations.extend(crop_info['tips'][:2])
    
    if irrigation < 50:
        recommendations.append("Consider installing drip irrigation or micro-sprinklers to improve water efficiency")
    
    if risk_level == "High":
        recommendations.append("⚠️ High risk detected - Consider crop insurance under PMFBY scheme")
    
    recommendations.append("Get soil tested under Soil Health Card scheme for precise fertilizer recommendations")
    
    # Comparison text
    comparison = ""
    if national_avg:
        if predicted_yield > national_avg * 1.1:
            comparison = f"Your predicted yield is {((predicted_yield/national_avg)-1)*100:.0f}% above national average ({national_avg:.0f} kg/ha)"
        elif predicted_yield < national_avg * 0.9:
            comparison = f"Your predicted yield is {((national_avg/predicted_yield)-1)*100:.0f}% below national average ({national_avg:.0f} kg/ha)"
        else:
            comparison = f"Your predicted yield is near national average ({national_avg:.0f} kg/ha)"
    
    return MLPrediction(
        predicted_yield_kg_ha=round(predicted_yield, 2),
        predicted_yield_quintal_acre=round(predicted_yield_quintal_acre, 2),
        confidence_score=round(confidence, 2),
        risk_level=risk_level,
        state_avg_yield=round(state_avg, 2) if state_avg else None,
        national_avg_yield=round(national_avg, 2) if national_avg else None,
        influential_factors=factors[:5],
        recommendations=recommendations[:5],
        crop_info=crop_info,
        comparison=comparison,
        data_source="Government of India Agricultural Statistics (Ministry of Agriculture & Farmers Welfare, 2023)"
    )

# Store for active chat sessions
chat_sessions: Dict[str, LlmChat] = {}

async def get_or_create_chat(session_id: str) -> LlmChat:
    """Get existing chat or create new one"""
    if session_id not in chat_sessions:
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=SYSTEM_PROMPT
        ).with_model("openai", "gpt-4o")
        chat_sessions[session_id] = chat
    return chat_sessions[session_id]

def build_context_message(message: str, farm_context: Optional[Dict], language: str) -> str:
    """Build enriched context message with knowledge base data"""
    context_parts = []
    
    # Add farm context
    if farm_context:
        context_parts.append(f"Farm Details: {farm_context}")
        
        # Add crop-specific knowledge
        crop_type = farm_context.get('crop_type', '')
        if crop_type:
            crop_info = get_crop_info(crop_type)
            if crop_info:
                context_parts.append(f"Crop Knowledge ({crop_type}): Optimal soil: {crop_info.get('optimal_soil')}, "
                                   f"Yield range: {crop_info.get('yield_range_kg_ha')}, "
                                   f"Major pests: {crop_info.get('major_pests', [])[:3]}, "
                                   f"Key tips: {crop_info.get('tips', [])[:2]}")
        
        # Add state-specific knowledge
        location = farm_context.get('location', '')
        if location:
            state_name = get_state_from_location(location)
            state_info = get_state_info(state_name)
            if state_info:
                context_parts.append(f"Region Info ({state_name}): Major crops: {state_info.get('major_crops')[:5]}, "
                                   f"Typical rainfall: {state_info.get('rainfall_mm')}, "
                                   f"Agri helpline: {state_info.get('agri_helpline')}")
        
        # Generate ML prediction if enough data
        if all(k in farm_context for k in ['crop_type', 'soil_type', 'season', 'location']):
            try:
                farm_input = FarmInput(
                    crop_type=farm_context.get('crop_type', ''),
                    soil_type=farm_context.get('soil_type', ''),
                    season=farm_context.get('season', ''),
                    location=farm_context.get('location', ''),
                    rainfall_mm=farm_context.get('rainfall_mm'),
                    irrigation_percent=farm_context.get('irrigation_percent'),
                    fertilizer_kg_ha=farm_context.get('fertilizer_kg_ha'),
                    temperature_c=farm_context.get('temperature_c')
                )
                prediction = predict_yield_ml(farm_input)
                context_parts.append(f"ML Yield Prediction: {prediction.predicted_yield_kg_ha} kg/ha "
                                   f"({prediction.predicted_yield_quintal_acre} quintal/acre), "
                                   f"Confidence: {prediction.confidence_score*100:.0f}%, "
                                   f"Risk: {prediction.risk_level}, "
                                   f"Factors: {[f['factor'] + ':' + f['impact'] for f in prediction.influential_factors[:3]]}")
            except Exception as e:
                logger.warning(f"Could not generate ML prediction: {e}")
    
    # Build final message
    if context_parts:
        return f"[CONTEXT FOR ASSISTANT - Use this to provide accurate advice]\n{chr(10).join(context_parts)}\n\n[FARMER'S QUESTION in {language}]: {message}"
    else:
        return f"[FARMER'S QUESTION in {language}]: {message}"

# API Routes
@api_router.get("/")
async def root():
    return {
        "message": "Farmer Voice Assistant API",
        "status": "running",
        "ml_model_loaded": ML_MODEL_LOADED,
        "data_source": "Government of India Agricultural Statistics",
        "supported_languages": ["English", "Hindi", "Telugu"],
        "supported_crops": list(CROP_KNOWLEDGE.keys()),
        "supported_states": list(STATE_AGRI_INFO.keys())
    }

@api_router.post("/session", response_model=Session)
async def create_session(language: str = "en"):
    """Create a new chat session"""
    session = Session(language=language)
    try:
        await db.sessions.insert_one(session.dict())
    except Exception as e:
         logger.warning(f"Failed to save session to DB: {e}")
    return session

@api_router.get("/session/{session_id}", response_model=Session)
async def get_session(session_id: str):
    """Get session details"""
    session = await db.sessions.find_one({"id": session_id})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return Session(**session)

@api_router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message and get AI response with knowledge-enhanced context"""
    try:
        # Detect language
        detected_language = request.language or detect_language(request.message)
        
        # Build enriched context message
        enriched_message = build_context_message(
            request.message, 
            request.farm_context, 
            detected_language
        )
        
        # Get or create chat session
        chat_instance = await get_or_create_chat(request.session_id)
        
        # Send message to LLM
        user_message = UserMessage(text=enriched_message)
        response_text = await chat_instance.send_message(user_message)
        
        # Generate ML prediction for response if applicable
        ml_prediction = None
        knowledge_context = {}
        
        if request.farm_context:
            if all(k in request.farm_context for k in ['crop_type', 'soil_type', 'season', 'location']):
                try:
                    farm_input = FarmInput(
                        crop_type=request.farm_context.get('crop_type', ''),
                        soil_type=request.farm_context.get('soil_type', ''),
                        season=request.farm_context.get('season', ''),
                        location=request.farm_context.get('location', ''),
                        rainfall_mm=request.farm_context.get('rainfall_mm'),
                        irrigation_percent=request.farm_context.get('irrigation_percent'),
                        fertilizer_kg_ha=request.farm_context.get('fertilizer_kg_ha')
                    )
                    prediction = predict_yield_ml(farm_input)
                    ml_prediction = prediction.dict()
                except Exception as e:
                    logger.warning(f"ML prediction error: {e}")
            
            # Add knowledge context
            crop_info = get_crop_info(request.farm_context.get('crop_type', ''))
            if crop_info:
                knowledge_context['crop'] = {
                    'name': request.farm_context.get('crop_type'),
                    'optimal_season': crop_info.get('optimal_season'),
                    'top_states': crop_info.get('top_states')
                }
        
        # Store messages
        user_msg = ChatMessage(
            session_id=request.session_id,
            role="user",
            content=request.message,
            language=detected_language
        )
        assistant_msg = ChatMessage(
            session_id=request.session_id,
            role="assistant",
            content=response_text,
            language=detected_language
        )
        
        try:
            await db.messages.insert_many([user_msg.dict(), assistant_msg.dict()])
        except Exception as e:
            logger.warning(f"Failed to save messages to DB (likely MongoDB connection error): {e}")
        
        return ChatResponse(
            response=response_text,
            language=detected_language,
            session_id=request.session_id,
            ml_prediction=ml_prediction,
            knowledge_context=knowledge_context if knowledge_context else None
        )
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@api_router.get("/messages/{session_id}", response_model=List[ChatMessage])
async def get_messages(session_id: str):
    """Get chat history for a session"""
    messages = await db.messages.find({"session_id": session_id}).sort("timestamp", 1).to_list(100)
    return [ChatMessage(**msg) for msg in messages]

@api_router.post("/predict", response_model=MLPrediction)
async def predict(farm_input: FarmInput):
    """Get ML prediction for crop yield based on Government of India data"""
    return predict_yield_ml(farm_input)

@api_router.get("/crops")
async def get_crops():
    """Get list of supported crops with basic info"""
    crops = []
    for crop_key, info in CROP_KNOWLEDGE.items():
        crops.append({
            "name": crop_key.title(),
            "name_hi": info.get('name_hi'),
            "name_te": info.get('name_te'),
            "optimal_season": info.get('optimal_season'),
            "yield_range": info.get('yield_range_kg_ha'),
            "top_states": info.get('top_states')
        })
    return crops

@api_router.get("/crops/{crop_name}")
async def get_crop_details(crop_name: str):
    """Get detailed information about a specific crop"""
    crop_info = get_crop_info(crop_name)
    if not crop_info:
        raise HTTPException(status_code=404, detail=f"Crop '{crop_name}' not found in knowledge base")
    return crop_info

@api_router.get("/states")
async def get_states():
    """Get list of supported states with agricultural info"""
    states = []
    for state_key, info in STATE_AGRI_INFO.items():
        states.append({
            "name": state_key.title(),
            "name_hi": info.get('name_hi'),
            "name_te": info.get('name_te'),
            "major_crops": info.get('major_crops'),
            "rainfall_range": info.get('rainfall_mm'),
            "agri_helpline": info.get('agri_helpline')
        })
    return states

@api_router.get("/states/{state_name}")
async def get_state_details(state_name: str):
    """Get detailed information about a specific state"""
    state_info = get_state_info(state_name)
    if not state_info:
        raise HTTPException(status_code=404, detail=f"State '{state_name}' not found in knowledge base")
    return state_info

@api_router.get("/schemes")
async def get_schemes():
    """Get list of government schemes for farmers"""
    return GOVT_SCHEMES

@api_router.post("/detect-language")
async def detect_lang(text: str):
    """Detect language of text"""
    return {"language": detect_language(text), "text": text}

@api_router.get("/model-info")
async def get_model_info():
    """Get ML model information and statistics"""
    if not ML_MODEL_LOADED:
        return {"status": "not_loaded", "message": "Using knowledge-based predictions"}
    
    return {
        "status": "loaded",
        "train_score": model_stats['train_score'],
        "test_score": model_stats['test_score'],
        "n_samples": model_stats['n_samples'],
        "unique_states": model_stats['unique_states'],
        "unique_crops": model_stats['unique_crops'],
        "feature_importance": model_stats['feature_importance'],
        "data_source": "Government of India - Ministry of Agriculture & Farmers Welfare (2023)"
    }

@api_router.get("/weather/{location}")
async def get_weather(location: str, language: str = "en"):
    """Get weather data and agricultural advisory for a location"""
    weather_data = await get_weather_advisory(location, language)
    return weather_data

@api_router.post("/speech-to-text")
async def speech_to_text(file: UploadFile = File(...), language: str = "auto"):
    """Convert speech to text using OpenAI Whisper API - supports Hindi, Telugu, English"""
    try:
        # Read audio file
        contents = await file.read()
        
        # Language mapping for Whisper
        lang_map = {
            "hi": "hi",  # Hindi
            "te": "te",  # Telugu
            "en": "en",  # English
            "auto": None  # Auto-detect
        }
        
        whisper_lang = lang_map.get(language)
        
        # Prepare multipart form data for Whisper API
        import io
        
        # Create form data
        files = {
            'file': ('audio.m4a', io.BytesIO(contents), 'audio/m4a'),
            'model': (None, 'whisper-1'),
        }
        
        if whisper_lang:
            files['language'] = (None, whisper_lang)
        
        # Add prompt to help with agricultural terminology
        files['prompt'] = (None, 'This is a farmer asking about crops, farming, agriculture, पंट, फसल, खेती, धान, गेहूं, వరి, పంట, వ్యవసాయం')
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers={
                    "Authorization": f"Bearer {EMERGENT_LLM_KEY}",
                },
                files=files
            )
            
            if response.status_code != 200:
                logger.error(f"Whisper API error: {response.status_code} - {response.text}")
                raise HTTPException(status_code=500, detail=f"Speech recognition failed: {response.text}")
            
            result = response.json()
            transcribed_text = result.get('text', '')
            
            # Detect language of transcribed text
            detected_lang = detect_language(transcribed_text)
            
            return {
                "success": True,
                "text": transcribed_text,
                "detected_language": detected_lang,
                "confidence": "high" if len(transcribed_text) > 10 else "medium"
            }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Speech-to-text error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Speech recognition error: {str(e)}")

@api_router.post("/analyze-pest-image")
async def analyze_pest_image(file: UploadFile = File(...), language: str = "en", crop: str = ""):
    """Analyze uploaded image for pest/disease identification using GPT-4o Vision"""
    try:
        # Read image and convert to base64
        contents = await file.read()
        base64_image = base64.b64encode(contents).decode('utf-8')
        
        # Determine mime type
        content_type = file.content_type or "image/jpeg"
        
        # Create prompt for pest analysis
        analysis_prompt = f"""You are an expert agricultural scientist specializing in plant pathology and entomology in India.

Analyze this image of a crop (likely {crop if crop else 'unknown crop'}) and identify:

1. PEST/DISEASE IDENTIFICATION:
   - Name of the pest or disease (common name and scientific name if possible)
   - Confidence level (High/Medium/Low)

2. SYMPTOMS OBSERVED:
   - List the visible symptoms in the image
   - Stage of infection/infestation

3. CAUSE:
   - What caused this problem
   - Environmental factors that may have contributed

4. CONTROL MEASURES:
   a) Immediate Action (within 24-48 hours)
   b) Organic/Biological Control
   c) Chemical Control (with specific product names used in India, dosage per liter)
   d) Preventive measures for future

5. ECONOMIC IMPACT:
   - Estimated yield loss if untreated (%)
   - Cost of treatment vs potential loss

6. BENEFITS OF TREATMENT:
   - Expected recovery rate
   - Yield improvement after treatment

Respond in {language.upper()} language (en=English, hi=Hindi, te=Telugu).
Be specific with Indian brand names of pesticides/fungicides available in the market.
Include safety precautions for chemical application."""

        # Use OpenAI API directly for vision
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {EMERGENT_LLM_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4o",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": analysis_prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:{content_type};base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    "max_tokens": 2000
                }
            )
            
            if response.status_code != 200:
                logger.error(f"OpenAI Vision API error: {response.text}")
                raise HTTPException(status_code=500, detail="Image analysis failed")
            
            result = response.json()
            analysis_text = result['choices'][0]['message']['content']
            
            return {
                "success": True,
                "analysis": analysis_text,
                "language": language,
                "crop": crop,
                "disclaimer": {
                    "en": "This is an AI-based preliminary analysis. For severe infestations, consult a local agricultural officer.",
                    "hi": "यह AI आधारित प्रारंभिक विश्लेषण है। गंभीर संक्रमण के लिए स्थानीय कृषि अधिकारी से परामर्श लें।",
                    "te": "ఇది AI ఆధారిత ప్రాథమిక విశ్లేషణ. తీవ్రమైన ముట్టడికి స్థానిక వ్యవసాయ అధికారిని సంప్రదించండి."
                }.get(language, "This is an AI-based preliminary analysis.")
            }
            
    except Exception as e:
        logger.error(f"Pest image analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Image analysis error: {str(e)}")

@api_router.post("/chart-data/yield-comparison")
async def get_yield_comparison_chart(farm_input: FarmInput):
    """Generate chart data for yield comparison visualization"""
    prediction = predict_yield_ml(farm_input)
    
    # Prepare bar chart data for comparison
    chart_data = {
        "chart_type": "bar",
        "title": f"{farm_input.crop_type.title()} Yield Comparison",
        "data": {
            "labels": ["Your Prediction", "State Average", "National Average", "Best Case"],
            "values": [
                prediction.predicted_yield_kg_ha,
                prediction.state_avg_yield or prediction.predicted_yield_kg_ha * 0.9,
                prediction.national_avg_yield or prediction.predicted_yield_kg_ha * 0.85,
                prediction.crop_info.get('yield_range_kg_ha', {}).get('max', prediction.predicted_yield_kg_ha * 1.2) if prediction.crop_info else prediction.predicted_yield_kg_ha * 1.2
            ],
            "colors": ["#4CAF50", "#2196F3", "#FF9800", "#9C27B0"]
        },
        "unit": "kg/ha",
        "analysis": prediction.comparison
    }
    
    return chart_data

@api_router.post("/chart-data/factors")
async def get_factors_chart(farm_input: FarmInput):
    """Generate chart data for influential factors visualization"""
    prediction = predict_yield_ml(farm_input)
    
    # Prepare pie/donut chart for factors
    factor_values = {
        "Irrigation": 30 if prediction.influential_factors else 25,
        "Rainfall": 25,
        "Soil Type": 20,
        "Fertilizer": 15,
        "Season": 10
    }
    
    # Adjust based on actual factors
    for factor in prediction.influential_factors:
        impact = factor.get('impact', 'Moderate')
        if impact == 'Positive':
            factor_values[factor['factor']] = factor_values.get(factor['factor'], 20) + 5
        elif impact == 'Negative':
            factor_values[factor['factor']] = factor_values.get(factor['factor'], 20) - 5
    
    chart_data = {
        "chart_type": "pie",
        "title": "Factors Affecting Your Yield",
        "data": {
            "labels": list(factor_values.keys()),
            "values": list(factor_values.values()),
            "colors": ["#4CAF50", "#2196F3", "#FF9800", "#9C27B0", "#E91E63"]
        },
        "insights": prediction.influential_factors
    }
    
    return chart_data

@api_router.post("/chart-data/recommendations")
async def get_recommendations_chart(farm_input: FarmInput):
    """Generate chart data showing potential improvement with recommendations"""
    prediction = predict_yield_ml(farm_input)
    crop_info = prediction.crop_info or {}
    
    current_yield = prediction.predicted_yield_kg_ha
    max_yield = crop_info.get('yield_range_kg_ha', {}).get('max', current_yield * 1.3)
    
    # Calculate potential improvements
    improvements = []
    
    if farm_input.irrigation_percent and farm_input.irrigation_percent < 80:
        improvement = min(20, (80 - farm_input.irrigation_percent) * 0.3)
        improvements.append({
            "action": "Improve Irrigation",
            "action_hi": "सिंचाई में सुधार",
            "action_te": "నీటిపారుదల మెరుగుపరచండి",
            "current": current_yield,
            "potential": current_yield * (1 + improvement/100),
            "improvement_percent": improvement,
            "cost_estimate": "Rs 5,000-10,000/acre",
            "benefit_estimate": f"Rs {int(improvement * 200)}/quintal extra"
        })
    
    if not farm_input.fertilizer_kg_ha or farm_input.fertilizer_kg_ha < 150:
        improvement = 15
        improvements.append({
            "action": "Optimize Fertilizer",
            "action_hi": "उर्वरक अनुकूलन",
            "action_te": "ఎరువులను ఆప్టిమైజ్ చేయండి",
            "current": current_yield,
            "potential": current_yield * (1 + improvement/100),
            "improvement_percent": improvement,
            "cost_estimate": "Rs 2,000-3,000/acre",
            "benefit_estimate": f"Rs {int(improvement * 150)}/quintal extra"
        })
    
    improvements.append({
        "action": "Use Certified Seeds",
        "action_hi": "प्रमाणित बीज उपयोग",
        "action_te": "ధృవీకరించిన విత్తనాలు వాడండి",
        "current": current_yield,
        "potential": current_yield * 1.25,
        "improvement_percent": 25,
        "cost_estimate": "Rs 500-1,000/acre extra",
        "benefit_estimate": "Rs 4,000-6,000/acre extra income"
    })
    
    improvements.append({
        "action": "Implement IPM",
        "action_hi": "IPM अपनाएं",
        "action_te": "IPM అమలు చేయండి",
        "current": current_yield,
        "potential": current_yield * 1.15,
        "improvement_percent": 15,
        "cost_estimate": "Rs 1,500-2,500/acre",
        "benefit_estimate": "40% reduction in pesticide cost + 15% yield increase"
    })
    
    chart_data = {
        "chart_type": "horizontal_bar",
        "title": "Potential Yield Improvement Roadmap",
        "current_yield": current_yield,
        "max_potential_yield": max_yield,
        "improvements": improvements,
        "summary": {
            "total_potential_improvement": f"{((max_yield/current_yield) - 1) * 100:.0f}%",
            "estimated_additional_income": f"Rs {int((max_yield - current_yield) * 2)}/acre"
        }
    }
    
    return chart_data

@api_router.get("/chart-data/seasonal/{crop}")
async def get_seasonal_chart(crop: str):
    """Get seasonal calendar chart data for a crop"""
    crop_info = get_crop_info(crop)
    if not crop_info:
        raise HTTPException(status_code=404, detail=f"Crop '{crop}' not found")
    
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    # Create activity timeline
    activities = {
        "land_prep": [0] * 12,
        "sowing": [0] * 12,
        "growing": [0] * 12,
        "harvest": [0] * 12
    }
    
    sowing_months = crop_info.get('sowing_months', {})
    harvest_months = crop_info.get('harvest_months', {})
    
    # Map activities to months (simplified)
    for season, period in sowing_months.items():
        if "June" in period or "July" in period:
            activities["land_prep"][4:6] = [1, 1]
            activities["sowing"][5:7] = [1, 1]
            activities["growing"][6:10] = [1, 1, 1, 1]
        if "October" in period or "November" in period:
            activities["land_prep"][8:10] = [1, 1]
            activities["sowing"][9:11] = [1, 1]
            activities["growing"][10:12] = [1, 1]
            activities["growing"][0:2] = [1, 1]
    
    for season, period in harvest_months.items():
        if "October" in period or "November" in period:
            activities["harvest"][9:11] = [1, 1]
        if "February" in period or "March" in period:
            activities["harvest"][1:4] = [1, 1, 1]
    
    return {
        "chart_type": "calendar",
        "title": f"{crop.title()} - Seasonal Calendar",
        "crop": crop,
        "months": months,
        "activities": activities,
        "irrigation_stages": crop_info.get('irrigation_stages', []),
        "critical_periods": [
            {"stage": "Sowing", "tip": "Ensure adequate soil moisture"},
            {"stage": "Flowering", "tip": "Critical for yield - avoid water stress"},
            {"stage": "Harvest", "tip": "Harvest at right maturity"}
        ]
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
