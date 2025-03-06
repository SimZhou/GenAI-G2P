import os
from typing import Dict, List, Optional, Union, Any

from .base import Provider
from openai import OpenAI

class DeepseekProvider(Provider):
    """
    Provider that interfaces with Deepseek's API using an OpenAI-compatible interface.
    API documentation: https://api-docs.deepseek.com/zh-cn/guides/reasoning_model#%E8%AE%BF%E9%97%AE%E6%A0%B7%E4%BE%8B
    """
    def __init__(
        self,
        model: str = "deepseek-chat",   # From: https://api-docs.deepseek.com/zh-cn/api/list-models
        system_prompt: str = "You are a helpful assistant.",
        **kwargs
    ):
        # Initialize base provider
        super().__init__(model)
        # If no API key is provided, attempt to read it from environment variables
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("Deepseek API key not provided. Please set the DEEPSEEK_API_KEY environment variable.")
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com", timeout=120, max_retries=2)     # for backward compatibility, you can still use `https://api.deepseek.com/v1` as `base_url`.
        self.model = model
        self.system_prompt = system_prompt
        self.extra_params = {}
        self.extra_params.update(kwargs)

    def completion(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7, **kwargs) -> Any:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            **{**self.extra_params, **kwargs}
        )
        # Include reasoning results
        if hasattr(response.choices[0].message, 'reasoning_content'):
            return response.choices[0].message.reasoning_content, response.choices[0].message.content
        else:
            return None, response.choices[0].message.content
