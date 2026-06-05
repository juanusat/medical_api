from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(dotenv_path=Path(__file__).resolve().parent / '.env')

def _get_required_env(name, cast=str):
    value = os.getenv(name)
    if value is None or value == '':
        raise RuntimeError(f'Missing required environment variable: {name}')

    try:
        return cast(value)
    except (TypeError, ValueError) as exc:
        raise RuntimeError(f'Invalid value for environment variable: {name}') from exc