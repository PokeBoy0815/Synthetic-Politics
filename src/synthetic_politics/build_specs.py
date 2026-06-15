import uuid
from synthetic_politics.generation_schemas import GenerationSpecifications
import itertools
import math

"""
def _normalizeSubtopicEntry(entry):

    if isinstance(entry, str):
        return {
            "name": entry,
            "issueFocus": None,
            "speechGoal": None,
            "requiredAspects": []
        }
    elif isinstance(entry, dict):        
        return {
            "name": entry.get("name"),
            "issueFocus": entry.get("issueFocus"),
            "speechGoal": entry.get("speechGoal"),
            "requiredAspects": list(entry.get("requiredSpects", [])) or []
        }
"""

    
def _normalizeSubtopicEntry(entry) -> dict:
    if isinstance(entry, str):
        return {
            "name": entry,
            "weight": None,
            "issueFocus": None,
            "speechGoal": None,
            "requiredAspects": [],
        }

    if isinstance(entry, dict):
        name = entry.get("name")
        if not name:
            raise ValueError(f"Subtopic entry is missing required field 'name': {entry}")

        return {
            "name": name,
            "weight": entry.get("weight"),
            "issueFocus": entry.get("issueFocus"),
            "speechGoal": entry.get("speechGoal"),
            "requiredAspects": list(entry.get("requiredAspects", []) or []),
        }

    raise TypeError(f"Unsupported subtopic entry type: {type(entry)!r}")


def buildSpecs(datasetConfig: dict, modelKeys: list[str]) -> list['GenerationSpecifications']:
    defaults = datasetConfig["defaultGeneration"]
    promptConditions = datasetConfig["promptConditions"]
    topics = datasetConfig["topics"]
    partyPresets = datasetConfig["partyPresets"]
    speakerRoles = datasetConfig["selection"]["speakerRoles"]
    textTypes = datasetConfig["selection"]["textTypes"]

    strategy = datasetConfig["synthesis_strategy"]
    topic_total_per_model_condition = int(strategy["topic_total_per_model_condition"])
    party_anchor_conditions = set(strategy["use_party_anchors_for_conditions"])

    style_pairs = list(itertools.product(speakerRoles, textTypes))
    style_cycle = itertools.cycle(style_pairs)

    specs: list[GenerationSpecifications] = []

    for model_key in modelKeys:
        seed_cycle = itertools.cycle(int(s) for s in defaults["seeds"])

        for topic_family, raw_subtopic_entries in topics.items():
            subtopic_entries = [_normalizeSubtopicEntry(e) for e in raw_subtopic_entries]
            subtopic_weights = {
                entry["name"]: float(entry["weight"] if entry["weight"] is not None else 1.0)
                for entry in subtopic_entries
            }

            for prompt_condition in promptConditions.keys():
                subtopic_counts = _allocate_counts(topic_total_per_model_condition, subtopic_weights)

                for entry in subtopic_entries:
                    subtopic_name = entry["name"]
                    subtopic_total = subtopic_counts[subtopic_name]
                    if subtopic_total == 0:
                        continue

                    if prompt_condition in party_anchor_conditions:
                        anchor_counts = _allocate_counts(
                            subtopic_total,
                            {anchor: 1.0 for anchor in partyPresets},
                        )

                        for partyPreset, n_specs in anchor_counts.items():
                            for _ in range(n_specs):
                                speakerRole, textType = next(style_cycle)
                                specs.append(
                                    GenerationSpecifications(
                                        sampleID=str(uuid.uuid4()),
                                        topicFamily=topic_family,
                                        subTopic=subtopic_name,
                                        partyPreset=partyPreset,
                                        speakerRole=speakerRole,
                                        textType=textType,
                                        targetLength=str(defaults["targetLength"]),
                                        register=str(defaults["register"]),
                                        promptCondition=prompt_condition,
                                        modelKey=model_key,
                                        temperature=float(defaults["temperature"]),
                                        top_p=float(defaults["top_p"]),
                                        maxOutputTokens=int(defaults["maxOutputTokens"]),
                                        seed=next(seed_cycle),
                                        promptVersion=str(datasetConfig["promptVersion"]),
                                        issueFocus=entry["issueFocus"],
                                        speechGoal=entry["speechGoal"],
                                        #requiredAspects=entry["requiredAspects"]
                                    )
                                )
                    else:
                        for _ in range(subtopic_total):
                            speakerRole, textType = next(style_cycle)
                            specs.append(
                                GenerationSpecifications(
                                    sampleID=str(uuid.uuid4()),
                                        topicFamily=topic_family,
                                        subTopic=subtopic_name,
                                        partyPreset=partyPreset,
                                        speakerRole=speakerRole,
                                        textType=textType,
                                        targetLength=str(defaults["targetLength"]),
                                        register=str(defaults["register"]),
                                        promptCondition=prompt_condition,
                                        modelKey=model_key,
                                        temperature=float(defaults["temperature"]),
                                        top_p=float(defaults["top_p"]),
                                        maxOutputTokens=int(defaults["maxOutputTokens"]),
                                        seed=next(seed_cycle),
                                        promptVersion=str(datasetConfig["promptVersion"]),
                                        issueFocus=entry["issueFocus"],
                                        speechGoal=entry["speechGoal"],
                                        requiredAspects=entry["requiredAspects"]
                                )
                            )

    return specs
"""
strategy = datasetConfig["synthesis_strategy"]
    topic_total_per_model = int(strategy["topic_total_per_model"])
    prompt_condition_weights = {
        k: float(v) for k, v in strategy["prompt_condition_weights"].items()
    }
    party_anchor_conditions = set(strategy["use_party_anchors_for_conditions"])

    style_pairs = list(itertools.product(speakerRoles, textTypes))
    style_cycle = itertools.cycle(style_pairs)

    specs: list['GenerationSpecifications'] = []

    for modelKey in modelKeys:
        seed_cycle = itertools.cycle(int(s) for s in defaults["seeds"])

        for topicFamily, raw_subtopic_entries in topics.items():
            subtopic_entries = [_normalizeSubtopicEntry(e) for e in raw_subtopic_entries]

            subtopic_weights = {
                entry["name"]: float(entry["weight"] if entry["weight"] is not None else 1.0)
                for entry in subtopic_entries
            }
            subtopic_counts = _allocate_counts(topic_total_per_model, subtopic_weights)

            for entry in subtopic_entries:
                #print(entry)
                subtopic_name = entry["name"]
                subtopic_total = subtopic_counts[subtopic_name]
                if subtopic_total == 0:
                    continue

                condition_counts = _allocate_counts(subtopic_total, prompt_condition_weights)

                for promptCondition, condition_total in condition_counts.items():
                    if condition_total == 0:
                        continue

                    if promptCondition in party_anchor_conditions:
                        anchor_counts = _allocate_counts(
                            condition_total,
                            {partyPreset: 1.0 for partyPreset in partyPresets},
                        )

                        for partyPreset, n_specs in anchor_counts.items():
                            for _ in range(n_specs):
                                speakerRole, textType = next(style_cycle)
                                specs.append(
                                    GenerationSpecifications(
                                        sampleID=str(uuid.uuid4()),
                                        topicFamily=topicFamily,
                                        subTopic=subtopic_name,
                                        partyPreset=partyPreset,
                                        speakerRole=speakerRole,
                                        textType=textType,
                                        targetLength=str(defaults["targetLength"]),
                                        register=str(defaults["register"]),
                                        promptCondition=promptCondition,
                                        modelKey=modelKey,
                                        temperature=float(defaults["temperature"]),
                                        top_p=float(defaults["top_p"]),
                                        maxOutputTokens=int(defaults["maxOutputTokens"]),
                                        seed=next(seed_cycle),
                                        promptVersion=str(datasetConfig["promptVersion"]),
                                        issueFocus=entry["issueFocus"],
                                        speechGoal=entry["speechGoal"],
                                        requiredAspects=entry["requiredAspects"],
                                    )
                                )
                    else:
                        for _ in range(condition_total):
                            speakerRole, textType = next(style_cycle)
                            specs.append(
                                GenerationSpecifications(
                                    sampleID=str(uuid.uuid4()),
                                    topicFamily=topicFamily,
                                    subTopic=subtopic_name,
                                    partyPreset="",
                                    speakerRole=speakerRole,
                                    textType=textType,
                                    targetLength=str(defaults["targetLength"]),
                                    register=str(defaults["register"]),
                                    promptCondition=promptCondition,
                                    modelKey=modelKey,
                                    temperature=float(defaults["temperature"]),
                                    top_p=float(defaults["top_p"]),
                                    maxOutputTokens=int(defaults["maxOutputTokens"]),
                                    seed=next(seed_cycle),
                                    promptVersion=str(datasetConfig["promptVersion"]),
                                    issueFocus=entry["issueFocus"],
                                    speechGoal=entry["speechGoal"],
                                    requiredAspects=entry["requiredAspects"],
                                )
                            )

    return specs
"""




def _allocate_counts(total: int, weights: dict[str, float]) -> dict[str, int]:
    if total <= 0:
        return {k: 0 for k in weights}

    weight_sum = sum(float(v) for v in weights.values())
    if weight_sum <= 0:
        raise ValueError("Weights must sum to a positive value.")

    raw = {k: total * (float(v) / weight_sum) for k, v in weights.items()}
    base = {k: math.floor(v) for k, v in raw.items()}
    remainder = total - sum(base.values())

    ranked = sorted(raw.keys(), key=lambda k: (raw[k] - base[k]), reverse=True)
    for k in ranked[:remainder]:
        base[k] += 1

    return base

#debugging fun
def summarizeSpecs(specs: list[GenerationSpec]) -> dict:
    from collections import Counter

    return {
        "n_specs": len(specs),
        "by_topic": dict(Counter(s.topic_family for s in specs)),
        "by_prompt_condition": dict(Counter(s.prompt_condition for s in specs)),
        "by_topic_subtopic": dict(Counter((s.topic_family, s.subtopic) for s in specs)),
    }