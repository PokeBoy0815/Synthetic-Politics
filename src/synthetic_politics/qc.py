import json
import re

from synthetic_politics.generation_schemas import GenerationDocumentation, GenerationSpecifications

REQUIRED_JSON_KEYS = {
    "sampleID",
    "topicFamily",
    "subtopic",
    "partyPreset",
    "speakerRole",
    "textType",
    "register",
    "generatedText"
}

def extractJsonObject(rawText):
    rawText = str(rawText).strip()

    #try direct parse
    try:
        parsed = json.loads(rawText)
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        pass

    #use helper fun to extract json from text
    candidate = _sliceOuterJsonObject(rawText)
    if candidate is None:
        return None

    try:
        parsed = json.loads(candidate)
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        pass

    repaired = _escapeControlCharsInsideStrings(candidate)
    try:
        parsed = json.loads(repaired)
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        return None
    

#format to json if not complete json
def _sliceOuterJsonObject(rawText):
    text = str(rawText).strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    return text[start : end + 1]

#removes text elements and makes everything machine readable
def _escapeControlCharsInsideStrings(input):
    out = []
    inString = False
    escape = False

    for ch in input:
        if inString:
            if escape:
                out.append(ch)
                escape = False
                continue

            if ch == "\\":
                out.append(ch)
                escape = True
                continue

            if ch == '"':
                out.append(ch)
                inString = False
                continue

            if ch == "\n":
                out.append("\\n")
                continue
            if ch == "\r":
                out.append("\\r")
                continue
            if ch == "\t":
                out.append("\\t")
                continue

            out.append(ch)
        else:
            out.append(ch)
            if ch == '"':
                inString = True

    return "".join(out)

def normalizeGeneratedText(text):
    text = str(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def wordCount(text: str) -> int:
    return len(re.findall(r"\w+", str(text), flags=re.UNICODE))

#adds flaggs to output json depending on missing values or other issues
def qcFlagsFor(spec, parsedJson, rawText, finishReason):
    flags = []

    if parsedJson is None:
        flags.append("json_parse_failed")
        return flags

    missing = REQUIRED_JSON_KEYS - set(parsedJson.keys())
    if missing:
        flags.append(f"missingKeys:{','.join(sorted(missing))}")

    genText = normalizeGeneratedText(parsedJson.get("generatedText", ""))
    wc = wordCount(genText)

    try:
        lo, hi = [int(x) for x in spec.targetLength.split("-")]
        if wc < lo:
            flags.append("tooShort")
        if wc > hi:
            flags.append("tooLong")
    except Exception:
        flags.append("invalidTargetLength")

    if not genText:
        flags.append("emptyText")

    if finishReason == "length":
        flags.append("outputTruncated")

    if "```" in rawText:
        flags.append("markdownFencePresent")


    return flags

def finalizeRecord(record, spec):
    parsed = extractJsonObject(record.rawText)
    if parsed is not None:
        parsed["sample_id"] = spec.sampleID
        parsed["topic_family"] = spec.topicFamily
        parsed["subtopic"] = spec.subTopic
        parsed["party_anchor"] = spec.partyAffiliation
        parsed["speaker_role"] = spec.speakerRole
        parsed["text_type"] = spec.textType
        parsed["register"] = spec.register
    flags = qcFlagsFor(spec, parsed, record.rawText, record.finishingReason)
    critical_flags = {
        "json_parse_failed",
        "empty_text",
        "output_truncated",
    }
    parse_ok = not any(flag in critical_flags for flag in flags)
    return GenerationDocumentation(
        sampleID=record.sampleID,
        modelKey=record.modelKey,
        modelID=record.modelID,
        host=record.host,
        promptVersion=record.promptVersion,
        promptCondition=record.promptCondition,
        topicFamily=record.topicFamily,
        subTopic=record.subTopic,
        partyAffilitation=record.partyAffilitation,
        speakerRole=record.speakerRole,
        textType=record.textType,
        targetLength=record.targetLength,
        register=record.register,
        temperature=record.temperature,
        top_p=record.top_p,
        maxOutputTokens=record.maxOutputTokens,
        seed=record.seed,
        sysPrompt=record.sysPrompt,
        userPrompt=record.userPrompt,
        rawText=record.rawText,
        parsedJSON=parsed,
        parseOK=parse_ok,
        qcFlags=flags,
        requestID=record.requestID,
        finishingReason=record.finishingReason,
        error=record.error,
        timeStamp=record.timeStamp,
    )