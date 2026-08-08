import httpx
from fastapi import HTTPException

from app.core.config import settings

from .base import BaseLLM

class OllamaProvider(BaseLLM):

    @property
    def name(self) -> str:
        return settings.llm_provider

    @property
    def version(self) -> str:
        return "1.0"

    @property
    def model(self) -> str:
        return settings.llm_model

    @property
    def base_url(self) -> str:
        return settings.llm_base_url

    async def generate(
        self,
        prompt: str,
    ) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        url = f"{self.base_url}/api/generate"

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(url, json=payload)

                # Check if Ollama returned a success status code
                response.raise_for_status()

                result_json: dict = response.json()

                if "response" not in result_json:
                    raise HTTPException(
                        status_code=500,
                        detail="Invalid response received from Ollama."
                    )

                return result_json.get("response", "")

            except httpx.HTTPStatusError as exc:
                raise HTTPException(
                    status_code=exc.response.status_code,
                    detail=f"Ollama API returned an error: {exc.response.text}"
                )
            except httpx.RequestError as exc:
                raise HTTPException(
                    status_code=503,
                    detail=f"Could not connect to local Ollama server: {str(exc)}"
                )