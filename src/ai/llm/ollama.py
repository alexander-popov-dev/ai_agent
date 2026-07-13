from langchain_ollama import ChatOllama


class OllamaClient:
    def __init__(self):
        self.chat = ChatOllama(
            model="qwen2.5:3b",
            temperature=0.0,
        )
        