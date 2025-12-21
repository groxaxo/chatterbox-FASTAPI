
import os

# Model Settings
# Can be overridden by environment variables
DEFAULT_TEMPERATURE = float(os.getenv("CHATTERBOX_TEMPERATURE", "0.5"))
DEFAULT_CFG_WEIGHT = float(os.getenv("CHATTERBOX_CFG_WEIGHT", "0.35"))
DEFAULT_EXAGGERATION = float(os.getenv("CHATTERBOX_EXAGGERATION", "1.0"))

# Constants
SAMPLE_RATE = 24000
