from openai import OpenAI
from synthetic_politics.hosts.base import BaseProvider

class OpenAICompatibleProvider(BaseProvider):
    def __init__(self, modelKey, config):
        super().__init__(modelKey, config)
        self.client = OpenAI(
            api_key=self.apiKey,
            base_url=config.baseURL,
            timeout=config.timeOutSecs
        )

    def getAnswer(self, *, systemPrompt, userPrompt, temperature, top_p, maxOutputTokens, seed):
        def _call():
            #print("iamopneai")
            response = self.client.chat.completions.create(
                model=self.config.modelID,
                messages=[
                    {"role": "system", "content": systemPrompt},
                    {"role": "user", "content": userPrompt},
                ],
                temperature=temperature,
                top_p=top_p,
                max_tokens=maxOutputTokens
            )
            choice = response.choices[0]
            return {
                "text": choice.message.content or "",
                "requestID": getattr(response, "id", None),
                "finishReason": getattr(choice, "finishReason", None)
            }

        return self.retry(_call)