"""The CLI configuration interface"""

from dataclasses import dataclass, field
from typing import Optional, List, Any, Tuple, Dict
from omegaconf import MISSING
from pathlib import Path

@dataclass
class Model:
    provider: str = MISSING
    model_name: str = MISSING
    system_prompt: str = ''
    prompt: str = ''

@dataclass
class G2PConfig:
    """The root configuration structure"""
    hparams: Any = MISSING
    input_file: Path = MISSING
    output_dir: Path = MISSING
    mode: str = 'predict'
    g: str = 'English'
    p: str = 'cmudict'
    models: List[Model] = field(default_factory=lambda: [Model()])
