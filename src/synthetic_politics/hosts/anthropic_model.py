import anthropic
from synthetic_politics.hosts.base import BaseProvider

class AnthropicMessagesProvider(BaseProvider):
    def __init__(self, modelKey, config):
        super().__init__(modelKey, config)
        self.client = anthropic.Anthropic(api_key=self.apiKey, timeout=config.timeOutSecs)

    #remove seed if not used
    def getAnswer(
        self,
        *,
        systemPrompt,
        userPrompt,
        temperature,
        top_p,
        maxOutputTokens,
        seed
    ):
        def _call():
            print("hier wird anthropic requested")
            print(self.config.modelID)
            response = self.client.messages.create(
                model = self.config.modelID,
                system = systemPrompt,
                #messages=[{"role": "user", "content": "was ist die hauptstadt von detuschland"}],
                messages = [{"role": "user", "content": userPrompt}],
                temperature = temperature,
                top_p = top_p,
                max_tokens = maxOutputTokens
            )
            #print(response)
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