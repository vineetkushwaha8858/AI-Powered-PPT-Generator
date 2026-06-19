import os, requests
from dotenv import load_dotenv
load_dotenv()

class FastUniversalAISystem:
    def __init__(self):
        self.nvidia_api_key = os.getenv("NVIDIA_API_KEY")
        if not self.nvidia_api_key:
            raise RuntimeError("NVIDIA_API_KEY missing in env file")
        self.nvidia_base_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        self.nvidia_model = "meta/llama-3.1-8b-instruct"

    def call_llm_fast(self, prompt, cache_key=None):
        try:
            headers = {
                "Authorization": f"Bearer {self.nvidia_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": self.nvidia_model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 200,
                "temperature": 0.3,
                "top_p": 0.8,
                "stream": False
            }
            response = requests.post(self.nvidia_base_url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                return content
            return ""
        except:
            return ""
