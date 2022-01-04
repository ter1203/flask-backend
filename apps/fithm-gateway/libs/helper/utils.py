from typing import Dict


def dict_get(source: Dict, key: str, default=None):
    """Safely get value from dict"""

    return source[key] if isinstance(source, Dict) and key in source else default
