"""
Load configuration options from config/config.json
and accessible from elsewhere
"""
import json

CONFIG_FILEPATH: str = "config/config.json"

def get_configs() -> dict:
    """
    Return dictionary of project configurations,
    or None if file is empty.
    """
    try:
        with open(CONFIG_FILEPATH, "r") as f:
            configs: dict = json.load(f)
        
        return configs
    except json.decoder.JSONDecodeError:
        """Likely empty file, return none instead"""
        init_configs()

def init_configs() -> dict:
    """
    Initialize config file if necessary
    Returns default configs
    """

    default_configs: dict = {
        "data_source": "data/horror_movies.csv",
        "logging_level": "INFO",
        "log_format": "%(asctime)s | %(levelname)s | %(message)s",
    }
    with open(CONFIG_FILEPATH, "w") as f:
        json.dump(default_configs, f, indent=4)

    return default_configs


# init configs if this file is directly ran
if __name__ == "__main__":
    init_configs()