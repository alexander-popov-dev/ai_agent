from application import settings
from engine.ai_provider.providers import Provider
from ai.providers.google import GoogleProvider
from ai.providers.ollama import OllamaProvider
from ai.providers.openrouter import OpenRouterProvider

ai_settings =  settings.get_ai_project_settings()

PROVIDERS = {
    Provider.GOOGLE: GoogleProvider,
    Provider.OLLAMA: OllamaProvider,
    Provider.OPENROUTER: OpenRouterProvider,
}

SECRETS = {
    Provider.GOOGLE: ai_settings.google_api_key,
    Provider.OPENROUTER: ai_settings.openrouter_api_key,
}