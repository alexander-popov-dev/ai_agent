from enum import StrEnum


class Provider(StrEnum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    GOOGLE = "google"
    OPENROUTER = "openrouter"