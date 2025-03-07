# GenAI-G2P: A tool for phonetic transcription with GenAI

## Quick Start
### Prepare API Keys
First, you should prepare your own API Keys from LLM providers, and fill them into `.ENV.API_KEYS.example`.
### Load API Keys
```bash
# Load API Keys into environment
source .ENV.API_KEYS.example
```
### Run Demo
```bash
# Run an example, to predict a list of english words into CMU Dict phonetic representationss
python -m genai_g2p.launch --config example/00_CMUDict_predict/predict_CMUDict.yaml
```

