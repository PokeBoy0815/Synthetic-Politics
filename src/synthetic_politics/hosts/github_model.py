import httpx
from synthetic_politics.hosts.base import HostBase

class GitHubModelsProvider(HostBase):
    def __init__(self, modelKey, config):
        super().__init__(modelKey, config)
        self.baseURL = (config.baseURL or "https://models.github.ai").rstrip("/")
        self.apiVersion = config.apiVersion or "2026-03-10"
        self.org = config.org
        self.timeout = config.timeOutSecs

    def getAnswer(self, *, systemPrompt, userPrompt, temperature, top_p, maxOutputTokens, seed):
        url = f"{self.baseURL}/inference/chat/completions"
        if self.org:
            url = f"{self.baseURL}/orgs/{self.org}/inference/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.apiKey}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": str(self.apiVersion)
        }

        payload = {
            "model": self.config.modelID,
            "messages": [
                {"role": "system", "content": systemPrompt},
                {"role": "user", "content": userPrompt},
            ],
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": maxOutputTokens,
            "seed": seed,
            "response_format": {"type": "json_object"},
            "stream": False
        }

        def _call():
            response = httpx.post(url, headers=headers, json=payload, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            choice = (data.get("choices") or [{}])[0]
            message = choice.get("message") or {}
            return {
                "text": message.get("content", "") or "",
                "requestID": response.headers.get("x-github-request-id"),
                "finishReason": choice.get("finishReason")
            }

        return self.retry(_call)