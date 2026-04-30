import anthropic
from synthetic_politics.hosts.base import HostBase

class AnthropicMessagesHost(HostBase):
    def __init__(self, modelKey, config):
        super().__init__(modelKey, config)
        self.client = anthropic.Anthropic(api_key=self.apiKey, timeout=config.timeOutSecs)

    #remove seed if not used
    def getAnswer(self, *, systemPrompt, userPrompt, temperature, top_p, maxOutputTokens, seed):
        def _call():
            response = self.client.messages.create(
                model = self.config.modelID,
                system = systemPrompt,
                messages = [
                    {"role": "user", "content": userPrompt}
                ],
                temperature = temperature,
                top_p = top_p,
                max_tokens = maxOutputTokens
            )
            parts = []
            for block in response.content:
                text = getattr(block, "text", None)
                if text:
                    parts.append(text)
            return {
                "text": "\n".join(parts).strip(),
                "requestID": getattr(response, "id", None),
                "finishReason": getattr(response, "stopReason", None)
            }
        return self.retry(_call)