from .base import Provider
import requests

class OpenAIProvider(Provider):
    def complete(self, prompt: str) -> str:
        url = "https://api.openai.com/v1/completions"
        payload = {
            "model": self.model_name,  # 例如 "text-davinci-003"
            "prompt": prompt,
            "max_tokens": 150,
            "temperature": 0.7
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.post(url, json=payload, headers=headers)
        r = response.json()
        if "choices" in r and len(r["choices"]) > 0:
            return r["choices"][0]["text"].strip()
        else:
            raise Exception("Invalid response from OpenAI API") 