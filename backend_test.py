#!/usr/bin/env python3
"""
Comprehensive Backend API Tests for Farmer Voice Assistant
Tests all backend endpoints with multilingual support
"""

import requests
import json
import time
from typing import Dict, Any

# Use the production URL from frontend/.env
BASE_URL = "https://agri-assist-36.preview.emergentagent.com/api"

class FarmerAssistantTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.session_ids = []
        
    def log_test(self, test_name: str, success: bool, details: str, response_data: Any = None):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "details": details,
            "response_data": response_data,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {details}")
        if response_data and not success:
            print(f"   Response: {response_data}")
    
    def test_root_endpoint(self):
        """Test GET /api/ - Root endpoint"""
        try:
            response = self.session.get(f"{BASE_URL}/")
            
            if response.status_code == 200:
                data = response.json()
                if "message" in data and "status" in data:
                    self.log_test("Root Endpoint", True, f"Status: {data.get('status')}, Message: {data.get('message')}", data)
                    return True
                else:
                    self.log_test("Root Endpoint", False, "Missing required fields in response", data)
                    return False
            else:
                self.log_test("Root Endpoint", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Root Endpoint", False, f"Request failed: {str(e)}")
            return False
    
    def test_create_session(self, language: str = "en"):
        """Test POST /api/session - Create new session"""
        try:
            response = self.session.post(f"{BASE_URL}/session", params={"language": language})
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["id", "language", "created_at"]
                
                if all(field in data for field in required_fields):
                    session_id = data["id"]
                    self.session_ids.append(session_id)
                    self.log_test(f"Create Session ({language})", True, f"Session created: {session_id}", data)
                    return session_id
                else:
                    missing = [f for f in required_fields if f not in data]
                    self.log_test(f"Create Session ({language})", False, f"Missing fields: {missing}", data)
                    return None
            else:
                self.log_test(f"Create Session ({language})", False, f"HTTP {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            self.log_test(f"Create Session ({language})", False, f"Request failed: {str(e)}")
            return None
    
    def test_chat_api(self, session_id: str, message: str, language: str, test_name: str):
        """Test POST /api/chat - Chat with AI assistant"""
        try:
            payload = {
                "session_id": session_id,
                "message": message,
                "language": language
            }
            
            response = self.session.post(f"{BASE_URL}/chat", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["response", "language", "session_id"]
                
                if all(field in data for field in required_fields):
                    # Check if response is not empty
                    if data["response"] and len(data["response"].strip()) > 0:
                        # Verify language matches
                        if data["language"] == language:
                            self.log_test(test_name, True, f"Chat response received in {language}: {data['response'][:100]}...", data)
                            return True
                        else:
                            self.log_test(test_name, False, f"Language mismatch: expected {language}, got {data['language']}", data)
                            return False
                    else:
                        self.log_test(test_name, False, "Empty response from AI", data)
                        return False
                else:
                    missing = [f for f in required_fields if f not in data]
                    self.log_test(test_name, False, f"Missing fields: {missing}", data)
                    return False
            else:
                self.log_test(test_name, False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test(test_name, False, f"Request failed: {str(e)}")
            return False
    
    def test_ml_prediction(self):
        """Test POST /api/predict - ML crop prediction"""
        try:
            payload = {
                "crop_type": "rice",
                "soil_type": "alluvial", 
                "season": "kharif",
                "location": "Punjab",
                "rainfall_mm": 800,
                "irrigation": True
            }
            
            response = self.session.post(f"{BASE_URL}/predict", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                required_fields = ["predicted_yield", "confidence", "risk_level", "influential_factors", "recommendations"]
                
                if all(field in data for field in required_fields):
                    # Validate data types and ranges
                    issues = []
                    
                    if not isinstance(data["predicted_yield"], (int, float)) or data["predicted_yield"] <= 0:
                        issues.append("Invalid predicted_yield")
                    
                    if not isinstance(data["confidence"], (int, float)) or not (0 <= data["confidence"] <= 1):
                        issues.append("Invalid confidence (should be 0-1)")
                    
                    if data["risk_level"] not in ["Low", "Medium", "High"]:
                        issues.append("Invalid risk_level")
                    
                    if not isinstance(data["influential_factors"], list) or len(data["influential_factors"]) == 0:
                        issues.append("Invalid influential_factors")
                    
                    if not isinstance(data["recommendations"], list) or len(data["recommendations"]) == 0:
                        issues.append("Invalid recommendations")
                    
                    if issues:
                        self.log_test("ML Prediction", False, f"Data validation issues: {', '.join(issues)}", data)
                        return False
                    else:
                        self.log_test("ML Prediction", True, f"Yield: {data['predicted_yield']}, Confidence: {data['confidence']}, Risk: {data['risk_level']}", data)
                        return True
                else:
                    missing = [f for f in required_fields if f not in data]
                    self.log_test("ML Prediction", False, f"Missing fields: {missing}", data)
                    return False
            else:
                self.log_test("ML Prediction", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("ML Prediction", False, f"Request failed: {str(e)}")
            return False
    
    def test_get_messages(self, session_id: str):
        """Test GET /api/messages/{session_id} - Get chat history"""
        try:
            response = self.session.get(f"{BASE_URL}/messages/{session_id}")
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, list):
                    # Should have at least 2 messages (user + assistant) from previous chat test
                    if len(data) >= 2:
                        # Check message structure
                        for msg in data:
                            required_fields = ["id", "session_id", "role", "content", "language", "timestamp"]
                            if not all(field in msg for field in required_fields):
                                missing = [f for f in required_fields if f not in msg]
                                self.log_test("Get Messages", False, f"Message missing fields: {missing}", data)
                                return False
                            
                            if msg["role"] not in ["user", "assistant"]:
                                self.log_test("Get Messages", False, f"Invalid role: {msg['role']}", data)
                                return False
                        
                        self.log_test("Get Messages", True, f"Retrieved {len(data)} messages", data)
                        return True
                    else:
                        self.log_test("Get Messages", False, f"Expected at least 2 messages, got {len(data)}", data)
                        return False
                else:
                    self.log_test("Get Messages", False, "Response is not a list", data)
                    return False
            else:
                self.log_test("Get Messages", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Get Messages", False, f"Request failed: {str(e)}")
            return False
    
    def test_language_detection(self):
        """Test POST /api/detect-language - Language detection"""
        test_cases = [
            ("Hello, how are you?", "en"),
            ("मेरी फसल में पीले पत्ते हैं", "hi"),
            ("నా పంట ఆకులు పసుపు", "te")
        ]
        
        all_passed = True
        
        for text, expected_lang in test_cases:
            try:
                response = self.session.post(f"{BASE_URL}/detect-language", params={"text": text})
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if "language" in data and "text" in data:
                        detected_lang = data["language"]
                        if detected_lang == expected_lang:
                            self.log_test(f"Language Detection ({expected_lang})", True, f"Correctly detected {detected_lang}", data)
                        else:
                            self.log_test(f"Language Detection ({expected_lang})", False, f"Expected {expected_lang}, got {detected_lang}", data)
                            all_passed = False
                    else:
                        self.log_test(f"Language Detection ({expected_lang})", False, "Missing required fields", data)
                        all_passed = False
                else:
                    self.log_test(f"Language Detection ({expected_lang})", False, f"HTTP {response.status_code}: {response.text}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Language Detection ({expected_lang})", False, f"Request failed: {str(e)}")
                all_passed = False
        
        return all_passed
    
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🚀 Starting Farmer Voice Assistant Backend API Tests")
        print(f"🌐 Testing against: {BASE_URL}")
        print("=" * 80)
        
        # Test 1: Root endpoint
        self.test_root_endpoint()
        
        # Test 2: Create sessions
        session_en = self.test_create_session("en")
        session_hi = self.test_create_session("hi") 
        session_te = self.test_create_session("te")
        
        # Test 3: Chat API with different languages
        if session_en:
            self.test_chat_api(session_en, "What crops grow in kharif season?", "en", "Chat API (English)")
        
        if session_hi:
            self.test_chat_api(session_hi, "मेरी फसल में पीले पत्ते हैं", "hi", "Chat API (Hindi)")
        
        if session_te:
            self.test_chat_api(session_te, "నా పంట ఆకులు పసుపు", "te", "Chat API (Telugu)")
        
        # Test 4: ML Prediction
        self.test_ml_prediction()
        
        # Test 5: Get messages (use first session if available)
        if self.session_ids:
            self.test_get_messages(self.session_ids[0])
        
        # Test 6: Language detection
        self.test_language_detection()
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if total - passed > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['details']}")
        
        return passed == total

if __name__ == "__main__":
    tester = FarmerAssistantTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed! Backend APIs are working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the details above.")