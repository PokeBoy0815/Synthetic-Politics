import uuid
from pathlib import Path
from synthetic_politics.generation_schemas import GenerationSpecifications


#
def _normalizeSubtopicEntry(entry):

    if isinstance(entry, str):
        return {
            "name": entry,
            "issueFocus": None,
            "speechGoal": None,
            "requiredAspects": []
        }
    elif isinstance(entry, dict):
        name = entry.get("name")
        
        return {
            "name": entry,
            "issueFocus": entry.get("issueFocus"),
            "speechGoal": entry.get("speechGoal"),
            "requiredAspects": list(entry.get("requiredSpects", [])) or []
        }


def buildSpecs(datasetConfig, modelKeys):
    defaults = datasetConfig["defaultGeneration"]
    promptConditions =datasetConfig["promptConditions"]
    topics = datasetConfig["topics"]
    partyPresets = datasetConfig["partyPresets"]
    speakerRoles = datasetConfig["speakerRoles"]
    textTypes = datasetConfig["selection"]["textTypes"]
    seeds = defaults["seeds"]

    specs = []

    for modelKey in modelKeys:
        for topicFamily, subtopic_entries in topics.items():
            for entry in subtopic_entries:
                subtopicConfig = _normalizeSubtopicEntry(entry)

                for partyPreset in partyPresets:
                    for speakerRole in speakerRoles:
                        for textType in textTypes:
                            for promptCondition in promptConditions.keys():
                                for seed in seeds:
                                    specs.append(
                                        GenerationSpecifications(
                                            sampleID=str(uuid.uuid4()),
                                            topicFamily=topicFamily,
                                            subTopic=subtopicConfig["name"],
                                            partyAffiliation=partyPreset,
                                            speakerRole=speakerRole,
                                            textType=textType,
                                            targetLength=str(defaults["targetLength"]),
                                            register=str(defaults["register"]),
                                            promptCondition=promptCondition,
                                            modelKey=modelKey,
                                            temperature=float(defaults["temperature"]),
                                            top_p=float(defaults["top_p"]),
                                            maxOutputTokens=int(defaults["maxOutputTokens"]),
                                            seed=int(seed),
                                            promptVersion=str(datasetConfig["promptVersion"]),

                                            #neu
                                            issueFocus=subtopicConfig["issueFocus"],
                                            speechGoal=subtopicConfig["speechGoal"],
                                            requiredAspects=subtopicConfig["requiredAspects"],
                                        )
                                    )
    
    return specs