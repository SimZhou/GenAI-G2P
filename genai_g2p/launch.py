import sys
import os
from omegaconf import OmegaConf
from argparse import ArgumentParser
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import re
from loguru import logger

from .provider.max_token_mapping import MAX_TOKEN_MAPPING

from .g2p_converter import G2PConverter
from .g2p_config import G2PConfig

def main():
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", type=Path, required=True)
    args = parser.parse_args()

    config = load_config(args.config)
    logger.info(config)
    os.makedirs(config['output_dir'], exist_ok=True)

    results = process_models(config)
    for model, result in zip(config.models, results):
        write_results_to_file(result, config['output_dir'] / f'results_{model.provider}_{model.model_name}.txt')

def load_config(config_path):
    if not os.path.exists(config_path):
        print(f"Config file {config_path} not found.")
        sys.exit(1)

    base_config = OmegaConf.structured(G2PConfig)
    user_config = OmegaConf.load(config_path)
    merged_config = OmegaConf.merge(base_config, user_config)
    return OmegaConf.create(OmegaConf.to_container(merged_config, resolve=True))

def resolve_links_in_prompt(prompt: str):
    import requests
    from pathlib import Path
    
    def get_content(reference):
        """Helper function to get content from a file or URL"""
        # Check if the reference is a URL
        if reference.startswith(('http://', 'https://')):
            try:
                response = requests.get(reference)
                response.raise_for_status()
                response.encoding = response.apparent_encoding
                return response.text
            except Exception as e:
                raise Exception(f"Error fetching URL {reference}: {str(e)}")

        # Otherwise, treat it as a file path
        else:
            try:
                file_path = Path(reference)
                if not file_path.exists():
                    raise Exception(f"File not found: {reference}")
                return file_path.read_text(encoding='utf-8')
            except Exception as e:
                raise Exception(f"Error reading file {reference}: {str(e)}")
    
    # Find all @-enclosed references and replace them with their content
    return re.sub(r'@(.*?)@', lambda match: '\n```\n' + get_content(match.group(1)) + '\n```\n', prompt)

def process_models(config):
    with ThreadPoolExecutor(max_workers=len(config.models)) as executor:
        futures = []
        for model in config.models:
            resolved_prompt = resolve_links_in_prompt(getattr(model, 'system_prompt', ''))
            logger.info(f"Processing model: {model.provider} {model.model_name}, system prompt: {resolved_prompt}")
            futures.append(executor.submit(
                G2PConverter(
                    provider=model.provider,
                    model_name=model.model_name,
                    max_tokens=MAX_TOKEN_MAPPING[model.model_name],
                    mode=config.mode,
                    g=config.g.lower(),
                    p=config.p.lower(),
                    system_prompt=resolved_prompt
                ).convert_file, config.input_file)
            )
        results = [
            future.result()
            for future in futures
        ]
    return results

def write_results_to_file(results, output_file):
    try:
        with open(output_file, 'w') as f:
            f.write(results)
        print(f"Results written to {output_file}")
    except Exception as e:
        print(f"Error writing results to file: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()