import re
from pathlib import Path
from synthetic_politics.qc import normalizeGeneratedText, wordCount
from synthetic_politics.generation_schemas import SpeechDocumentation
from synthetic_politics.data_helper import readJsonl, createParquet

CHUNK_SIZE = 250

def splitWords(text):
    text = re.sub(r"\s+", " ", str(text)).strip()
    return text.split

def chunkText(text):
    words = splitWords(text)
    return [" ".join(words[i : i + CHUNK_SIZE]) for i in range(0, len(words), CHUNK_SIZE)]

def rawtoSpeeches(rawPath):
    rows = readJsonl(rawPath)
    speeches = []
    for row in rows:
        if not row.get("parseOK", False):
            continue
        parsed = row.get("parsedJson") or {}
        gen_text = normalizeGeneratedText(parsed.get("generatedText", ""))
        if not gen_text:
            continue
        speeches.append(
            SpeechDocumentation(
                speechID=row["sampleID"],
                speakerID=None,
                name=None,
                faction=row.get("partyPreset"),
                date=row.get("createdAt", "")[:10],
                text=gen_text,
                wordCount=wordCount(gen_text),
                kwHits=None,
                embScore=None,
                cecore=None,
                topic=row.get("topicFamily"),
                sampleID=row["sampleID"],
                modelKey=row["modelKey"],
                modelID=row["modelID"],
                host=row["host"],
                promptVersion=row["promptVersion"],
                promptCondition=row["promptCondition"],
                topicFamily=row["topicFamily"],
                subTopic=row["subTopic"],
                partyAffiliation=row["partyPreset"],
                speakerRole=row["speakerRole"],
                textType=row["textType"],
                targetLength=row["targetLength"],
                register=row["register"],
                temperature=float(row["temperature"]),
                top_p=float(row["top_p"]),
                maxOutputTokens=int(row["maxOutputTokens"]),
                seed=int(row["seed"]),
            ).toDict()
        )
    return speeches

def speechToChunks(speeches):
    rows = []
    for speech in speeches:
        if not speech["text"]:
            continue
        for chunkID, chunk in enumerate(chunkText(speech["text"], CHUNK_SIZE)):
            rows.append(
                {
                    "dataset": "syn",
                    "topic": speech["topic"],
                    "speechID": speech["speechID"],
                    "personID": speech["personID"],
                    "name": speech["name"],
                    "faction": speech["faction"],
                    "date": speech["date"],
                    "chunkID": chunkID,
                    "chunkText": chunk
                }
            )
    return rows

def transformAll(rawPath, speechOut, chunksOut):
    speeches = rawtoSpeeches(rawPath)
    chunks = speechToChunks(speeches)
    createParquet(speechOut, speeches)
    createParquet(chunksOut, chunks)
    return len(speeches), len(chunks)
        