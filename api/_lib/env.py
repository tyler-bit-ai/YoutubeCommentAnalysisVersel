import os


def get_required_env(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def is_configured(name):
    return bool(os.environ.get(name, "").strip())
