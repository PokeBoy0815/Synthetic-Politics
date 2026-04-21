from __future__ import annotations
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone

def getTimeAsIso():
    return datetime.now(timezone.utc).isoformat.replace("+00:00", "Z")

@dataclass
class GenerationSpecifications:
    sampleID: str
    topicFamily: str
    subTopic: str
    partyAfiliation: str
    speakerRole: str
    textType: str
    targetLength: str
    register: str
    promptCondition: str
    modelKey: str
    temperature: str
    top_p: float
    maxOutputTokens: int
    seed: int
    promptVersion: str

    def toDict(self):
          return asdict(self)
    
@dataclass
class ModelConfigurations:
    host: str
    modelID: str
    APIKeyFromEnv: str
    baseURL: str | None=None
    timeOutSecs: int=120
    maxRetries: int=3
    apiVersion: str | None=None
    org: str | None=None


@dataclass
class GenerationDocumentation:
    sampleID: str
    modelKey: str
    modelID: str
    host: str
    promptVersion: str
    promptCondition: str
    topicFamiy: str
    subTopic: str
    partyAffiliation: str
    speakerRole: str
    textType: str
    targetLength: str
    register: str
    temperature: float
    top_p: float
    maxOutputTokes: int
    seed: int
    sysPrompt: str
    userPropmt: str
    rawText: str
    parsedJSON: dict[str, Any] | None
    parseOK: bool
    qcFlags: list[str]=field(default_factory=list)
    requestID: str | None=None
    finishingReason: str | None=None
    error: str | None=None
    timeStamp: str=field(default_factory=getTimeAsIso)

    def toDict(self):
        return asdict(self)
    
@dataclass
class SpeechDocumentation:
    speechID: str
    speakerID: str | None
    name: str | None
    faction: str | None
    date: str
    text: str
    wordCount: int
    kwHits: int | None
    embScore: float |None
    ceScore: float | None
    topic: str
    sampleID: str
    modelKey: str
    modelID: str
    host: str
    promptVersion: str
    promptCondition: str
    topicFamily: str
    subTopic: str
    partyAffiliation: str
    speakerRole: str
    textType: str
    targetLength: str
    register: str
    temperature: float
    top_p: float
    maxOutputTokens: int
    seed: int
    sourceDataSet: str="syn"

    def toDict(self):
        return asdict(self)
    



