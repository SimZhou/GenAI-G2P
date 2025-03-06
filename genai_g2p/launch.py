import sys
import os
from omegaconf import OmegaConf
from argparse import ArgumentParser
from pathlib import Path

from .g2p_converter import G2PConverter
from .g2p_config import G2PConfig

def main():
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", type=Path, required=True)
    args = parser.parse_args()

    config = load_config(args.config)
    print(config)
    os.makedirs(config['output_dir'], exist_ok=True)

    results = process_models(config, mode=config.mode)
    write_results_to_file(results, config['output_dir'] / 'results.txt')

def load_config(config_path):
    if not os.path.exists(config_path):
        print(f"Config file {config_path} not found.")
        sys.exit(1)

    base_config = OmegaConf.structured(G2PConfig)
    user_config = OmegaConf.load(config_path)
    merged_config = OmegaConf.merge(base_config, user_config)
    return OmegaConf.create(OmegaConf.to_container(merged_config, resolve=True))

def process_models(config, mode = 'predict'):
    if mode == 'predict':
        results = [
            G2PConverter(
                provider=model.provider,
                model_name=model.model_name,
                mode=config.mode,
                g=config.g.lower(),
                p=config.p.lower(),
                prompt=getattr(model, 'prompt', '')
            ).convert_file(config.input_file)
            for model in config.models
        ]
    elif mode == 'correction':
        # results = [
        #     G2PConverter(
        #         provider=model.provider,
        #         model_name=model.model_name,
        #         mode=config.mode,
        #         g=config.g,
        #         p=config.p,
        #         prompt=getattr(model, 'prompt', '')
        #     ).convert_file(config.input_file)
        #     for model in config.models
        pass
    return results

def write_results_to_file(results, output_file):
    try:
        with open(output_file, 'w') as f:
            f.writelines(f"{res}\n" for res in results)
        print(f"Results written to {output_file}")
    except Exception as e:
        print(f"Error writing results to file: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()