"""
Weather Service for Indian Agriculture
Uses Open-Meteo API (free, no key required)
Provides real-time weather and agricultural advisories
"""

import httpx
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# Indian state capitals coordinates for weather data
INDIA_LOCATIONS = {
    "andhra pradesh": {"lat": 16.5062, "lon": 80.6480, "city": "Vijayawada"},
    "telangana": {"lat": 17.3850, "lon": 78.4867, "city": "Hyderabad"},
    "punjab": {"lat": 30.7333, "lon": 76.7794, "city": "Chandigarh"},
    "haryana": {"lat": 30.7333, "lon": 76.7794, "city": "Chandigarh"},
    "uttar pradesh": {"lat": 26.8467, "lon": 80.9462, "city": "Lucknow"},
    "maharashtra": {"lat": 19.0760, "lon": 72.8777, "city": "Mumbai"},
    "madhya pradesh": {"lat": 23.2599, "lon": 77.4126, "city": "Bhopal"},
    "gujarat": {"lat": 23.0225, "lon": 72.5714, "city": "Ahmedabad"},
    "rajasthan": {"lat": 26.9124, "lon": 75.7873, "city": "Jaipur"},
    "karnataka": {"lat": 12.9716, "lon": 77.5946, "city": "Bengaluru"},
    "tamil nadu": {"lat": 13.0827, "lon": 80.2707, "city": "Chennai"},
    "west bengal": {"lat": 22.5726, "lon": 88.3639, "city": "Kolkata"},
    "bihar": {"lat": 25.5941, "lon": 85.1376, "city": "Patna"},
    "odisha": {"lat": 20.2961, "lon": 85.8245, "city": "Bhubaneswar"},
    "kerala": {"lat": 8.5241, "lon": 76.9366, "city": "Thiruvananthapuram"},
    "assam": {"lat": 26.1445, "lon": 91.7362, "city": "Guwahati"},
    "jharkhand": {"lat": 23.3441, "lon": 85.3096, "city": "Ranchi"},
    "chhattisgarh": {"lat": 21.2514, "lon": 81.6296, "city": "Raipur"},
    "uttarakhand": {"lat": 30.3165, "lon": 78.0322, "city": "Dehradun"},
    "himachal pradesh": {"lat": 31.1048, "lon": 77.1734, "city": "Shimla"},
}

# District coordinates (major agricultural districts)
DISTRICT_COORDS = {
    # Andhra Pradesh
    "guntur": {"lat": 16.3067, "lon": 80.4365},
    "krishna": {"lat": 16.6100, "lon": 80.7214},
    "east godavari": {"lat": 17.0, "lon": 82.0},
    "west godavari": {"lat": 16.9174, "lon": 81.3399},
    "kurnool": {"lat": 15.8281, "lon": 78.0373},
    "anantapur": {"lat": 14.6819, "lon": 77.6006},
    # Telangana
    "karimnagar": {"lat": 18.4386, "lon": 79.1288},
    "warangal": {"lat": 17.9784, "lon": 79.5941},
    "nizamabad": {"lat": 18.6725, "lon": 78.0941},
    "khammam": {"lat": 17.2473, "lon": 80.1514},
    # Punjab
    "ludhiana": {"lat": 30.9010, "lon": 75.8573},
    "amritsar": {"lat": 31.6340, "lon": 74.8723},
    "jalandhar": {"lat": 31.3260, "lon": 75.5762},
    "patiala": {"lat": 30.3398, "lon": 76.3869},
    # Uttar Pradesh
    "meerut": {"lat": 28.9845, "lon": 77.7064},
    "lucknow": {"lat": 26.8467, "lon": 80.9462},
    "agra": {"lat": 27.1767, "lon": 78.0081},
    "varanasi": {"lat": 25.3176, "lon": 82.9739},
    "gorakhpur": {"lat": 26.7606, "lon": 83.3732},
    # Maharashtra
    "nagpur": {"lat": 21.1458, "lon": 79.0882},
    "pune": {"lat": 18.5204, "lon": 73.8567},
    "nashik": {"lat": 19.9975, "lon": 73.7898},
    "kolhapur": {"lat": 16.7050, "lon": 74.2433},
    # Gujarat
    "ahmedabad": {"lat": 23.0225, "lon": 72.5714},
    "rajkot": {"lat": 22.3039, "lon": 70.8022},
    "surat": {"lat": 21.1702, "lon": 72.8311},
    # Rajasthan
    "jaipur": {"lat": 26.9124, "lon": 75.7873},
    "jodhpur": {"lat": 26.2389, "lon": 73.0243},
    "bikaner": {"lat": 28.0229, "lon": 73.3119},
    # Karnataka
    "belgaum": {"lat": 15.8497, "lon": 74.4977},
    "mysore": {"lat": 12.2958, "lon": 76.6394},
    "dharwad": {"lat": 15.4589, "lon": 75.0078},
    # Tamil Nadu
    "chennai": {"lat": 13.0827, "lon": 80.2707},
    "coimbatore": {"lat": 11.0168, "lon": 76.9558},
    "madurai": {"lat": 9.9252, "lon": 78.1198},
    "thanjavur": {"lat": 10.7870, "lon": 79.1378},
}

class WeatherService:
    """Weather service using Open-Meteo API"""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
    
    def get_coordinates(self, location: str) -> Optional[Dict[str, float]]:
        """Get coordinates for a location"""
        location_lower = location.lower().strip()
        
        # Check districts first
        for district, coords in DISTRICT_COORDS.items():
            if district in location_lower:
                return coords
        
        # Check states
        for state, data in INDIA_LOCATIONS.items():
            if state in location_lower:
                return {"lat": data["lat"], "lon": data["lon"]}
        
        return None
    
    async def get_weather(self, location: str) -> Optional[Dict[str, Any]]:
        """Get current and forecast weather for location"""
        coords = self.get_coordinates(location)
        if not coords:
            return None
        
        try:
            params = {
                "latitude": coords["lat"],
                "longitude": coords["lon"],
                "current": "temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m",
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,weather_code",
                "timezone": "Asia/Kolkata",
                "forecast_days": 7
            }
            
            response = await self.client.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Process current weather
            current = data.get("current", {})
            daily = data.get("daily", {})
            
            weather_info = {
                "location": location,
                "coordinates": coords,
                "current": {
                    "temperature_c": current.get("temperature_2m"),
                    "humidity_percent": current.get("relative_humidity_2m"),
                    "precipitation_mm": current.get("precipitation"),
                    "wind_speed_kmh": current.get("wind_speed_10m"),
                    "condition": self._get_weather_condition(current.get("weather_code", 0))
                },
                "forecast": [],
                "agricultural_advisory": []
            }
            
            # Process 7-day forecast
            if daily:
                for i in range(min(7, len(daily.get("time", [])))):
                    weather_info["forecast"].append({
                        "date": daily["time"][i],
                        "max_temp_c": daily["temperature_2m_max"][i],
                        "min_temp_c": daily["temperature_2m_min"][i],
                        "precipitation_mm": daily["precipitation_sum"][i],
                        "rain_probability": daily["precipitation_probability_max"][i],
                        "condition": self._get_weather_condition(daily["weather_code"][i])
                    })
            
            # Generate agricultural advisory
            weather_info["agricultural_advisory"] = self._generate_agri_advisory(weather_info)
            
            return weather_info
            
        except Exception as e:
            logger.error(f"Weather API error: {e}")
            return None
    
    def _get_weather_condition(self, code: int) -> str:
        """Convert WMO weather code to description"""
        conditions = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }
        return conditions.get(code, "Unknown")
    
    def _generate_agri_advisory(self, weather: Dict) -> list:
        """Generate agricultural advisories based on weather"""
        advisories = []
        current = weather.get("current", {})
        forecast = weather.get("forecast", [])
        
        temp = current.get("temperature_c", 25)
        humidity = current.get("humidity_percent", 60)
        
        # Temperature advisories
        if temp > 40:
            advisories.append({
                "type": "heat_stress",
                "severity": "high",
                "message_en": "Extreme heat alert! Avoid field work 11 AM - 4 PM. Irrigate in evening only.",
                "message_hi": "अत्यधिक गर्मी की चेतावनी! सुबह 11 से शाम 4 बजे तक खेत में काम न करें। शाम को ही सिंचाई करें।",
                "message_te": "తీవ్ర వేడి హెచ్చరిక! 11 AM - 4 PM మధ్య పొలం పనులు చేయకండి. సాయంత్రం మాత్రమే నీరు పెట్టండి."
            })
        elif temp > 35:
            advisories.append({
                "type": "heat_advisory",
                "severity": "medium",
                "message_en": "High temperature. Provide shade for nurseries. Mulch to conserve moisture.",
                "message_hi": "उच्च तापमान। नर्सरी को छाया दें। पानी बचाने के लिए मल्चिंग करें।",
                "message_te": "అధిక ఉష్ణోగ్రత. నర్సరీలకు నీడ ఇవ్వండి. తేమ కాపాడటానికి మల్చింగ్ చేయండి."
            })
        elif temp < 10:
            advisories.append({
                "type": "cold_advisory",
                "severity": "medium",
                "message_en": "Low temperature. Protect crops from frost. Irrigate in morning to reduce frost damage.",
                "message_hi": "कम तापमान। फसलों को पाले से बचाएं। पाले के नुकसान को कम करने के लिए सुबह सिंचाई करें।",
                "message_te": "తక్కువ ఉష్ణోగ్రత. పంటలను మంచు నుండి రక్షించండి. మంచు నష్టాన్ని తగ్గించడానికి ఉదయం నీరు పెట్టండి."
            })
        
        # Rain forecast advisories
        total_rain_7days = sum(f.get("precipitation_mm", 0) or 0 for f in forecast[:7])
        
        if total_rain_7days > 100:
            advisories.append({
                "type": "heavy_rain_warning",
                "severity": "high",
                "message_en": f"Heavy rainfall expected ({total_rain_7days:.0f}mm in 7 days). Ensure field drainage. Postpone fertilizer application.",
                "message_hi": f"भारी बारिश की संभावना ({total_rain_7days:.0f}mm 7 दिनों में)। खेत में जल निकासी सुनिश्चित करें। उर्वरक डालने में देरी करें।",
                "message_te": f"భారీ వర్షం అంచనా ({total_rain_7days:.0f}mm 7 రోజుల్లో). పొలంలో డ్రైనేజీ నిర్ధారించుకోండి. ఎరువులు వేయడం వాయిదా వేయండి."
            })
        elif total_rain_7days > 50:
            advisories.append({
                "type": "rain_expected",
                "severity": "low",
                "message_en": f"Good rainfall expected ({total_rain_7days:.0f}mm). Favorable for sowing. Complete land preparation.",
                "message_hi": f"अच्छी बारिश की संभावना ({total_rain_7days:.0f}mm)। बुवाई के लिए अनुकूल। भूमि की तैयारी पूरी करें।",
                "message_te": f"మంచి వర్షం అంచనా ({total_rain_7days:.0f}mm). విత్తనానికి అనుకూలం. భూమి సిద్ధం పూర్తి చేయండి."
            })
        elif total_rain_7days < 5:
            advisories.append({
                "type": "dry_spell",
                "severity": "medium",
                "message_en": "Dry spell expected. Plan irrigation. Watch for pest buildup in dry conditions.",
                "message_hi": "सूखे की संभावना। सिंचाई की योजना बनाएं। सूखी परिस्थितियों में कीटों पर नजर रखें।",
                "message_te": "పొడి వాతావరణం అంచనా. నీటిపారుదల ప్రణాళిక చేయండి. పొడి పరిస్థితుల్లో పురుగుల పెరుగుదలను గమనించండి."
            })
        
        # Humidity advisories (disease risk)
        if humidity > 85:
            advisories.append({
                "type": "disease_risk",
                "severity": "medium",
                "message_en": "High humidity increases disease risk. Apply preventive fungicide. Avoid overhead irrigation.",
                "message_hi": "उच्च आर्द्रता से रोग का खतरा बढ़ता है। निवारक फफूंदनाशक लगाएं। ऊपरी सिंचाई से बचें।",
                "message_te": "అధిక తేమ వల్ల వ్యాధుల ప్రమాదం పెరుగుతుంది. నివారణ శిలీంద్ర నాశిని చల్లండి. పై నుండి నీరు పెట్టడం మానండి."
            })
        
        # Spray timing advisory
        if current.get("wind_speed_kmh", 0) < 10:
            advisories.append({
                "type": "spray_favorable",
                "severity": "info",
                "message_en": "Low wind - favorable for pesticide/fertilizer spraying. Best time: early morning or late evening.",
                "message_hi": "कम हवा - कीटनाशक/उर्वरक छिड़काव के लिए अनुकूल। सबसे अच्छा समय: सुबह जल्दी या शाम देर से।",
                "message_te": "తక్కువ గాలి - పురుగుమందు/ఎరువుల పిచికారికి అనుకూలం. ఉత్తమ సమయం: పొద్దున్నే లేదా సాయంత్రం."
            })
        elif current.get("wind_speed_kmh", 0) > 20:
            advisories.append({
                "type": "spray_unfavorable",
                "severity": "info",
                "message_en": "High wind - avoid spraying pesticides/fertilizers. Risk of drift and wastage.",
                "message_hi": "तेज हवा - कीटनाशक/उर्वरक छिड़काव न करें। बहाव और बर्बादी का खतरा।",
                "message_te": "అధిక గాలి - పురుగుమందులు/ఎరువులు పిచికారీ చేయకండి. కొట్టుకుపోయే ప్రమాదం."
            })
        
        return advisories
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


# Singleton instance
weather_service = WeatherService()


async def get_weather_advisory(location: str, language: str = "en") -> Dict[str, Any]:
    """Get weather and agricultural advisory for a location"""
    weather = await weather_service.get_weather(location)
    
    if not weather:
        return {
            "error": True,
            "message": "Could not fetch weather data for this location"
        }
    
    # Format advisories in the requested language
    lang_key = f"message_{language}"
    formatted_advisories = []
    
    for advisory in weather.get("agricultural_advisory", []):
        formatted_advisories.append({
            "type": advisory["type"],
            "severity": advisory["severity"],
            "message": advisory.get(lang_key, advisory.get("message_en"))
        })
    
    return {
        "error": False,
        "location": weather["location"],
        "current": weather["current"],
        "forecast_7day": weather["forecast"],
        "advisories": formatted_advisories,
        "data_source": "Open-Meteo Weather API"
    }
