from os import environ

def get_env(name) -> str | None:
    return environ.get(name)