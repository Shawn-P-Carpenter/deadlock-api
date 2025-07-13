from enum import Enum

class BaseUrl(str, Enum):
    BASE_ASSETS = "https://assets.deadlock-api.com"
    BASE_API = "https://api.deadlock-api.com"