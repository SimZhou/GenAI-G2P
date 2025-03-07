from ..provider import create_provider
from pathlib import Path
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from loguru import logger
import re

class G2PConverter:
    def __init__(self, provider, model_name, mode = 'predict', g = 'English', p = 'cmudict', system_prompt = None, max_split_length = 50, **kwargs):
        self.provider = create_provider(provider, model_name, system_prompt)
        self.mode = mode
        self.g = g
        self.p = p
        if not system_prompt:
            logger.warning(f"No system_prompt provided, using default system_prompt for {self.mode} mode")
            self.system_prompt = self.build_default_system_prompt(self.mode, self.g, self.p)
            self.provider.system_prompt = self.system_prompt
        # For batch G2P
        self.max_split_length = max_split_length

    def build_default_system_prompt(self, mode = 'predict', g = 'English', p = 'cmudict') -> str:
        if mode == 'predict':
            return f"You are a linguistic expert specialized in phonetic transcription from {g} to {p}.\nProvide accurate phonetic transcriptions for each line without extra explanation, keep the original text at the beginning of each line.\nColumn 1 is the text, column 2+ is the existing phonetic transcription.\nIf explanation is necessary, provide them in brackets to the line end."
        elif mode == 'correction':
            return f"You are a linguistic expert specialized in phonetic transcription from {g} to {p}.\nProvide correction of the existing phonetic transcriptions for column 1 in each line without extra explanation, keep the original text at the beginning of each line.\nColumn 1 is the text, column 2+ is the existing phonetic transcription.\nThe existing transcription may not be accurate, so think carefully and correct them if necessary.\nIf explanation is needed, provide them in brackets to the line end."

    def convert(self, text: str) -> str:
        return self.provider.completion(text)[1]

    def convert_file(self, input_file: Path, mode = 'predict') -> str:
        prompts_splitted = self.read_file_to_prompt(input_file, mode, self.max_split_length)
        with ThreadPoolExecutor(max_workers=len(prompts_splitted)) as executor:
            results = list(tqdm(executor.map(self.provider.completion, prompts_splitted), total=len(prompts_splitted), desc="Converting files"))
        parsed_results = "\n".join([self.parse_result(result) for reasoning_result, result in results])
        return parsed_results
    
    def read_file_to_prompt(self, input_file: Path, mode = 'predict', max_split_length = 1000) -> list[str]:
        if mode == 'predict':
            lines = [line.strip().split(' ', 1)[0] for line in open(input_file, 'r').readlines()]
        elif mode == 'correction':
            lines = [line.strip() for line in open(input_file, 'r').readlines()]
        else:
            raise ValueError(f"Unsupported mode: {mode}")
        return ["```\n" + "\n".join(lines[i:i + max_split_length]) + "\n```" for i in range(0, len(lines), max_split_length)]
    
    def parse_result(self, result: str) -> str:
        if self.p == 'cmudict':
            return self.parse_cmudict(result)
        elif self.p == 'ipa':
            return self.parse_ipa(result)
        else:
            raise ValueError(f"Unsupported phonetic transcription format: {self.p}")
    
    def parse_cmudict(self, result: str) -> str:
        return re.sub(r'^[`\n]+|[`\n]+$', '', result)
    
    def parse_ipa(self, result: str) -> str:
        return result
