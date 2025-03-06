from .openai import OpenAIProvider
from .volcengine import VolcEngineProvider
from .deepseek import DeepseekProvider
from .dashscope import DashscopeProvider

def create_provider(provider_name: str, model_name: str, system_prompt: str = None, **kwargs):
    if provider_name.lower() == "openai":
        return OpenAIProvider(model_name, system_prompt, **kwargs)
    elif provider_name.lower() == "volcengine":
        return VolcEngineProvider(model_name, system_prompt, **kwargs)
    elif provider_name.lower() == "deepseek":
        return DeepseekProvider(model_name, system_prompt, **kwargs)
    elif provider_name.lower() == "dashscope":
        return DashscopeProvider(model_name, system_prompt, **kwargs)
    else:
        raise ValueError(f"Unsupported provider: {provider_name}")