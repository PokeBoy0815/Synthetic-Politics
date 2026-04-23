import os
import time
from abc import ABC, abstractmethod

from synthetic_politics.generation_schemas import ModelConfigurations

class BaseProvider(ABC):
    def __init__(self, modelKey: str, config: ModelConfigurations):
        self.modelKey =modelKey
        self.config = config
        #api key aus venv
        self.apiKey = os.getenv(config.APIKeyFromEnv)
        if self.apiKey is None:
            raise ValueError(
                f"Env variable {config.APIKeyFromEnv} is not available for '{modelKey}'"
            )

@abstractmethod
def getAnswer(self, *, systemPrompt: str, userPrompt: str, temperature: float, top_p: float, maxOutputTokens: int, seed: int):
    print("not implemented")

def retry(self, fn):
    lastError =None
    for i in range(1, self.config.maxRetries + 1):
        try:
            return fn()
        except Exception as exc:
            lastError = exc
            if i==self.config.maxRetries:
                raise
            #muss vermutlich noch angepasst werden
            time.sleep(2) 