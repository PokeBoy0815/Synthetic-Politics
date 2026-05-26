from __future__ import annotations

from openai import OpenAI

from synthetic_politics.hosts.base import BaseProvider


class OpenRouterProvider(BaseProvider):
    def __init__(self, model_key, config):
        super().__init__(model_key, config)
        self.client = OpenAI(
            api_key=self.apiKey,
            base_url=config.baseURL or "https://openrouter.ai/api/v1",
            timeout=config.timeOutSecs,
            default_headers={
                # optional, but recommended by OpenRouter
                "HTTP-Referer": "https://github.com/markus-weinberger/synthetic-politics",
                "X-OpenRouter-Title": "Synthetic Politics",
            },
        )

    def getAnswer(
        self,
        *,
        systemPrompt: str,
        userPrompt: str,
        temperature: float,
        top_p: float,
        maxOutputTokens: int,
        seed: int,
    ) -> dict:
        def _call():
            response = self.client.chat.completions.create(
                model=self.config.modelID,
                messages=[
                    {"role": "system", "content": systemPrompt},
                    {"role": "user", "content": userPrompt},
                ],
                temperature=temperature,
                top_p=top_p,
                max_tokens=maxOutputTokens,
            )
            choice = response.choices[0]
            return {
                "text": choice.message.content or "",
                "requestID": getattr(response, "id", None),
                "finishReason": getattr(choice, "finishReason", None),
            }

        return self.retry(_call)