import os
from typing import Dict, List, Optional, Union, Any

from .base import Provider
from openai import OpenAI

class DashscopeProvider(Provider):
    """
    Provider that interfaces with Dashscope's API using an OpenAI-compatible interface.
    API documentation: https://bailian.console.aliyun.com/?spm=a2c4g.11186623.nav-v2-dropdown-menu-0.d_main_0_4.382d7980W38pU1#/model-market/detail/qwq-32b-preview
    """
    def __init__(
        self,
        model: str = "qwen-max-2025-01-25",   # From: https://help.aliyun.com/zh/model-studio/getting-started/models
        system_prompt: str = "You are a helpful assistant.",
        **kwargs
    ):
        # Initialize base provider
        super().__init__(model)
        # If no API key is provided, attempt to read it from environment variables
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("Dashscope API key not provided. Please set the DASHSCOPE_API_KEY environment variable.")
        self.client = OpenAI(api_key=self.api_key, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1", timeout=120, max_retries=2)
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
        
        if kwargs.get('stream', False):
            return response

        # Include reasoning results
        if hasattr(response.choices[0].message, 'reasoning_content'):
            return response.choices[0].message.reasoning_content, response.choices[0].message.content
        else:
            return None, response.choices[0].message.content
