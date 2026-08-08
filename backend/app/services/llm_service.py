
from app.providers.llm.factory import LLMFactory


class LLMService:

    def __init__(self) -> None:
        pass

    async def generate(self, prompt: str)-> str:
        provider = LLMFactory.get_llm()

        return await provider.generate(prompt)
