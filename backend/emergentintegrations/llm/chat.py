import httpx
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class UserMessage:
    def __init__(self, text: str):
        self.text = text

class LlmChat:
    def __init__(self, api_key: str, session_id: str, system_message: str):
        self.api_key = api_key
        self.session_id = session_id
        self.system_message = system_message
        self.model = "gpt-4o"
        self.history: List[Dict[str, str]] = [
            {"role": "system", "content": system_message}
        ]

    def with_model(self, provider: str, model: str):
        self.model = model
        return self

    async def send_message(self, message: UserMessage) -> str:
        self.history.append({"role": "user", "content": message.text})
        
        if not self.api_key or self.api_key == "your_key_here":
            # Mock response if no key provided
            mock_response = "I am a mock AI assistant. Please provide a valid API Key in .env to get real responses."
            self.history.append({"role": "assistant", "content": mock_response})
            return mock_response

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": self.history,
            "temperature": 0.7,
            "max_tokens": 1000
        }

        if self.api_key.startswith("sk-or-v1"):
            base_url = "https://openrouter.ai/api/v1/chat/completions"
            headers["HTTP-Referer"] = "https://github.com/AgroBot/AgroBot" 
            headers["X-Title"] = "AgroBot"
            # OpenRouter requires 'openai/' prefix for GPT models usually, or we should use a default if not set
            if self.model == "gpt-4o":
                 payload["model"] = "openai/gpt-4o"
        else:
            base_url = "https://api.openai.com/v1/chat/completions"

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    base_url,
                    headers=headers,
                    json=payload
                )
                
                if response.status_code != 200:
                    error_msg = f"API Error ({response.status_code}): {response.text}"
                    logger.error(error_msg)
                    return f"I encountered an error connecting to the AI service. Details: {error_msg}"

                data = response.json()
                content = data['choices'][0]['message']['content']
                self.history.append({"role": "assistant", "content": content})
                return content
                
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return f"Sorry, I am having trouble connecting to the server. Error: {str(e)}"
