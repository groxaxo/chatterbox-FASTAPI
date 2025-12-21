# Chatterbox FastAPI Configuration Guide

This guide explains how to configure default parameters for the Chatterbox FastAPI server, particularly for controlling the text-to-speech generation style.

## Environment Variables

You can configure default generation parameters using environment variables. These can be set in a `.env` file in the project root or exported in your shell.

### Available Parameters

| Variable | Description | Default | Recommended Range |
|----------|-------------|---------|-------------------|
| `DEFAULT_TEMPERATURE` | Controls randomness in generation | `1.4` | 0.1 - 1.5 |
| `DEFAULT_CFG_WEIGHT` | Classifier-Free Guidance weight | `0.35` | 0.1 - 1.0 |
| `DEFAULT_EXAGGERATION` | Controls emotional expressiveness | `1.7` | 0.0 - 2.0 |

### Using a .env file

Create a file named `.env` in the root directory (`/home/op/chatterbox-FASTAPI-1/`) with your desired values:

```bash
# .env
DEFAULT_TEMPERATURE=1.4
DEFAULT_CFG_WEIGHT=0.35
DEFAULT_EXAGGERATION=1.7
```

### Using Shell Environment Variables

You can also pass these variables directly when launching the server:

```bash
export DEFAULT_TEMPERATURE=0.8
export DEFAULT_EXAGGERATION=1.0
./launch_server.sh
# or
DEFAULT_TEMPERATURE=0.8 ./launch_server.sh
```

## Changing Hardcoded Defaults

If you prefer to change the fallback defaults in the code (when no environment variables are present), edit the following file:

`api/config.py`

```python
# Generation Defaults
DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", "1.4"))
DEFAULT_CFG_WEIGHT = float(os.getenv("DEFAULT_CFG_WEIGHT", "0.35"))
DEFAULT_EXAGGERATION = float(os.getenv("DEFAULT_EXAGGERATION", "1.7"))
```

Changing the second argument in `os.getenv` changes the hardcoded default.
