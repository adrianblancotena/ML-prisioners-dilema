# save_progress.py
import json

SAVE_FILE = 'saved_strategies.json'

def save_strategy(ia_name, strategy):
    """Guarda la estrategia de una IA en un archivo JSON."""
    try:
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data[ia_name] = strategy

    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f)

def load_strategy(ia_name):
    """Carga la estrategia de una IA desde un archivo JSON."""
    try:
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
            return data.get(ia_name, None)
    except (FileNotFoundError, json.JSONDecodeError):
        return None
