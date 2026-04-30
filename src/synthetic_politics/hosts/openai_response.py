from openai import OpenAI
from synthetic_politics.hosts.base import HostBase

class OpenAIResponsesHost(HostBase):
    def __init__(self, modelKey, config):
        super().__init__(modelKey, config)
        kwargs = {"api_key": self.apiKey, "timeout": config.timeOutSecs}
        if config.baseURL:
            kwargs["base_url"] = config.baseURL
        self.client = OpenAI(**kwargs)

    def getAnswer(self, *, systemPrompt, userPrompt, temperature, top_p, maxOutputTokens, seed):
        def _call():
            response = self.client.responses.create(
                model=self.config.modelID,
                instructions=systemPrompt,
                input=userPrompt,
                temperature=temperature,
                top_p=top_p,
                max_output_tokens=maxOutputTokens,
                text={"format": {"type": "text"}},
            )
            return {
                "text": getattr(response, "output_text", "") or "",
                "requestID": getattr(response, "id", None),
                "finishReason": getattr(response, "status", None),
            }

        return self.retry(_call)