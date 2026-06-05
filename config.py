from get_env import _get_required_env

class Config:
    DB_HOST = _get_required_env('DB_HOST')
    DB_USER = _get_required_env('DB_USER')
    DB_PASSWORD = _get_required_env('DB_PASSWORD')
    DB_NAME = _get_required_env('DB_NAME')
    DB_PORT = _get_required_env('DB_PORT', int)
    SECRET_KEY = _get_required_env('SECRET_KEY')
