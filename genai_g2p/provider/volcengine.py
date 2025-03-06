import os
from typing import Dict, List, Optional, Union, Any

from .base import Provider
from volcenginesdkarkruntime import Ark


class VolcEngineProvider(Provider):
    """Provider that uses ByteDance's VolcEngine API (火山引擎) for text-to-phonetics conversion.
    
    ARK SDK Doc: https://www.volcengine.com/docs/82379/1319847
    API Doc: https://www.volcengine.com/docs/82379/1302008
    Price: https://www.volcengine.com/docs/82379/1099320#%E5%90%8E%E4%BB%98%E8%B4%B9%EF%BC%88%E6%8C%89tokens%E4%BD%BF%E7%94%A8%E9%87%8F%E4%BB%98%E8%B4%B9%EF%BC%89
    Model List: https://www.volcengine.com/docs/82379/1330310
    Prompt Guide: https://www.volcengine.com/docs/82379/1221660
    DeepSeek-R1 Prompt Guide: https://www.volcengine.com/docs/82379/1449737#%E6%8F%90%E7%A4%BA%E8%AF%8D%E4%BC%98%E5%8C%96%E5%BB%BA%E8%AE%AE
    """
    def __init__(
        self,
        model: str = "doubao-1-5-pro-256k-250115",
        system_prompt: str = "You are a helpful assistant.",
        **kwargs
    ):
        """
        Initialize the VolcEngine provider.

        Args:
            api_key: VolcEngine API key. If not provided, will be read from ARK_API_KEY environment variable.
            model: Model to use. Default is 'doubao-1-5-pro-256k-250115'.
            temperature: Sampling temperature.
            api_base: Base URL for the VolcEngine API.
            **kwargs: Additional parameters to pass to the API call.
        """
        super().__init__(model)
        self.api_key = os.getenv("ARK_API_KEY")
        if not self.api_key:
            raise ValueError("VolcEngine API key not provided. Please set the ARK_API_KEY environment variable.")
        self.client = Ark(
            api_key=self.api_key,
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            timeout=120,
            max_retries=2,
        )
        self.model = model
        self.system_prompt = system_prompt
        self.extra_params = {}
        self.extra_params.update(kwargs)

    def completion(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7, **kwargs) -> Any:
        response = self.client.chat.completions.create(
            model = self.model,
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ],
            max_tokens = max_tokens,
            temperature = temperature,
            **{**self.extra_params, **kwargs},          # 额外参数，可以设置例如temperature, topP等
                                                        #          参考文档：https://www.volcengine.com/docs/82379/1298454#%E8%AF%B7%E6%B1%82%E5%8F%82%E6%95%B0
                                                        # 一些示例重要参数：
                                                        # max_tokens: 最大输出tokens数，默认4096。各个模型可配上限不同，详细见 https://www.volcengine.com/docs/82379/1330310
                                                        # temperature: 0: 确定性输出，1: 随机性输出，默认为1
                                                        # top_p: 0: 确定性输出，1: 随机性输出，默认为0.7

            extra_headers={'x-is-encrypted': 'false'}   # 火山引擎支持免费开启推理会话应用层加密
        )
        # Include reasoning results
        if hasattr(response.choices[0].message, 'reasoning_content'):
            return response.choices[0].message.reasoning_content, response.choices[0].message.content
        else:
            return None, response.choices[0].message.content
