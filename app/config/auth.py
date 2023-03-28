import os


def set_up():
    """Sets up configuration for the app"""
    config = {
        "DOMAIN": os.getenv("DOMAIN", "your.domain.com"),
        "API_AUDIENCE": os.getenv("API_AUDIENCE", "your.audience.com"),
        "ALGORITHMS": os.getenv("ALGORITHMS", "RS256"),
    }
    return config
