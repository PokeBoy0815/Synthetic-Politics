from pathlib import Path
import yaml

from synthetic_politics.pormpt_construction import loadSysPrompt, buildUserPrompt
from synthetic_politics.qc import finalizeRecord
from synthetic_politics.generation_schemas import GenerationDocumentation, GenerationSpecifications, ModelConfigurations
from synthetic_politics.data_helper import appendJsonl
from synthetic_politics.hosts.anthropic_model import AnthropicMessagesHost
from synthetic_politics.hosts.openai_response import OpenAIResponsesHost
from synthetic_politics.hosts.github_model import GitHubModelsHost
from synthetic_politics.hosts.openai_compareable import OpenAICompatibleHost

HOST_MAP={
    "openaiResponses": OpenAIResponsesHost,
    "opneaiComparable": OpenAICompatibleHost,
    "anthropicMessages": AnthropicMessagesHost,
    "githubModels": GitHubModelsHost
}


def loadModelConfigs(path):
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
        out = {}
        for key, value in cfg["models"].items():
            #debug print
            print(value)
            out[key] = ModelConfigurations(**value)
        return out

def buildHost(modelKey, modelConfig):
    host_cls = HOST_MAP.get(modelConfig.host)
    if host_cls is None:
        raise ValueError(f"unsupported host type: {modelConfig.host}")
    return host_cls(modelKey, modelConfig)
    
def genOne(spec, host):
    userPrompt = buildUserPrompt(spec)
    result = host.generate(
        systemPrompt=loadSysPrompt,
        userPrompt=userPrompt,
        temperature=spec.temperature,
        top_p=spec.top_p,
        maxOutputTokens=spec.maxOutputTokens,
        seed=spec.seed
    )

    preliminary = GenerationDocumentation(
        sampleID=spec.sampleID,
        modelKey=spec.modelKey,
        modelID=host.config.modelID,
        host=host.config.host,
        promptVersion=spec.promptVersion,
        promptCondition=spec.promptCondition,
        topicFamily=spec.topicFamily,
        subTopic=spec.subTopic,
        partyAffilitation=spec.partyAffiliation,
        speakerRole=spec.speakerRole,
        textType=spec.textType,
        targetLength=spec.targetLength,
        register=spec.register,
        temperature=spec.temperature,
        top_p=spec.top_p,
        maxOutputTokens=spec.maxOutputTokens,
        seed=spec.seed,
        sysPrompt=loadSysPrompt,
        userPrompt=userPrompt,
        rawText=result.get("text", ""),
        parsedJSON=None,
        parseOK=False,
        requestID=result.get("requestID"),
        finishingReason=result.get("finishReason"),
        error=None,
    )
    
    return finalizeRecord(preliminary, spec)

def genMultiple(specs, modelConfigs, outPath):
    hosts = {}
    for spec in specs:
        if spec.modelKey not in hosts:
            hosts[spec.modelKey] = buildHost(spec.modelKey, modelConfigs[spec.modelKey])
        provider = hosts[spec.modelKey]
        try:
            record = genOne(spec, provider)
        except Exception as exc:  # noqa: BLE001
            record = GenerationDocumentation(
                sampleID=spec.sampleID,
                modelKey=spec.modelKey,
                modelID=modelConfigs[spec.modelKey].modelID,
                host=modelConfigs[spec.modelKey].host,
                promptVersion=spec.promptVersion,
                promptCondition=spec.promptCondition,
                topicFamily=spec.topicFamily,
                subTopic=spec.subTopic,
                partyAffilitation=spec.partyAffiliation,
                speakerRole=spec.speakerRole,
                textType=spec.textType,
                targetLength=spec.targetLength,
                register=spec.register,
                temperature=spec.temperature,
                top_p=spec.top_p,
                maxOutputTokens=spec.maxOutputTokens,
                seed=spec.seed,
                sysPrompt=loadSysPrompt,
                userPrompt=buildUserPrompt(spec),
                rawText="",
                parsedJSON=None,
                parseOK=False,
                qcFlags=["requestFailed"],
                error=str(exc),
            )
        appendJsonl(outPath, record.toDict())
