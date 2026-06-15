import yaml
from pathlib import Path

#v2 !!
SYSTEM_PROMPT = """
You generate original synthetic German parliamentary political texts for academic research.
Write in German only.
The output must sound like a plausible contemporary Wahlperiode 20 Bundestag plenary speech.
Avoid theatrical, archaic, overly literary, or implausible parliamentary formulas.
Do not invent a party identity, faction, politician, or office unless this is explicitly provided in the context.
Do not reproduce known speeches or quote real politicians.
Do not explain your reasoning.
Output only one JSON object.
Your response must start with "{" and end with "}".
Do not write any text before or after the JSON object.
Return valid JSON only.
""".strip()

def build_message(specification):
    return [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": buildUserPrompt(specification)}]


def buildUserPrompt(spec):
    sampleID = _get(spec, "sampleID", "")
    topicFamily = _get(spec, "topicFamily", "")
    subTopic = _get(spec, "subTopic", "")
    speakerRole = _get(spec, "speakerRole", "")
    textType = _get(spec, "textType", "")
    register = _get(spec, "register", "")
    issueFocus = _get(spec, "issueFocus", "")
    speechGoal = _get(spec, "speechGoal", "")

    partyLine, contextLine = makeOptional(spec)

    issueFocusPart = f"- issueFocus: {issueFocus}" if issueFocus else ""
    speechGoalPart = f"- speechGoal: {speechGoal}" if speechGoal else ""

    promptCondition = _get(spec, "promptCondition", "minC1")

    if promptCondition == "minC1":
        anchorRule = (
            'If no party preset is provided in the context, set "partyPreset" to an empty string in the JSON.\n'
            "If no party preset is provided in the context, do not mention or imply a specific party, faction, politician, or named political group in the speech."
        )
    else:
        anchorRule = (
            'If a party preset is provided, copy it exactly into the JSON field "partyPreset".\n'
            "If a party preset is provided, use it only as a broad political orientation for argumentative emphasis and style."
        )
    return f"""
Create one original synthetic German parliamentary political text.

Kontext:
- sampleID: {sampleID}
- topicFamily: {topicFamily}
- subTopic: {subTopic}
- speakerRole: {speakerRole}
- textType: {textType}
- setting: German Bundestag plenary debate
- register: {register}
{partyLine}
{issueFocusPart}
{speechGoalPart}
{contextLine}


Task:
Write one original synthetic German parliamentary speech of 650 to 750 words.


The speech should:
- address the subtopic directly and stay within the topic family,
- sound like a plausible contemporary Bundestag plenary contribution,
- end with a political evaluation, proposal, or demand.


Structure:
- Write exactly 4 substantial paragraphs.
- Paragraph 1: introduce the issue and explain why it matters.
- Paragraph 2: describe the core problem and its consequences.
- Paragraph 3: develop the political argument and briefly contrast it with an opposing view.
- Paragraph 4: conclude with a summary and a clear call to action.


Requirements:
- The text must be written in German.
- Output only one JSON object.
- Your response must start with "{{" and end with "}}".
- Do not add any text before the opening "{{" or after the closing "}}".
- It must be original and not resemble a known speech too closely.
- Avoid theatrical, archaic, or implausible parliamentary formulas.
- Use a sober, policy-oriented parliamentary tone.
- Use plausible Bundestag-style address forms such as "Herr Präsident", "Frau Präsidentin", or "Meine Damen und Herren".
- Do not use forms such as "Herr/Frau Präsidentin", "Ehrwürdige Abgeordneten", "Guten Tag", or "Herr Abgeordneter".
- Do not include metadata inside the speech text.
- Do not include explanations or notes.
- Do not include markdown fences.
- Copy metadata fields exactly from the provided context and do not invent or modify them.
- {anchorRule}
- Do not write short paragraphs.
- Do not end the speech early.
- Do not wrap the JSON in triple backticks.


Return valid JSON with the keys:
sampleID, topicFamily, subTopic, partyPreset, speakerRole, textType, register, generatedText
""".strip()


#Dictionaries and object-like specifications can be imported
def _get(spec, key, default=None):
    if isinstance(spec, dict):
        return spec.get(key, default)
    return getattr(spec, key, default)

def _formatRequiredAspects(requiredAspects):
    aspects = list(requiredAspects or [])
    if not aspects:
        return ''
    lines = ['requiredAspects:']
    for aspect in aspects:
        lines.append(f" - {aspect}")
    return '\n'.join(lines)

#Outputs partyLine and ContextLine
def makeOptional(spec):
    promptCondition = _get(spec, "promptCondition", "minC1")
    partyPreset = _get(spec, "partyPreset", "")
    speakerRole =_get(spec, "speakerRole", "")

    if promptCondition == "C1_minimal":
        return ("", "")
    elif promptCondition == "partyPresC2":
        return (
            f"- partyPreset: {partyPreset}",
            (
                "Additional instruction:\n"
                "If a party preset is provided, use it only as a broad orientation "
                "for argumentative emphasis and policy style.\n"
                "Do not imitate real politicians or known speeches.\n"
                "Do not explicitly name the party unless it fits naturally into the speech."
            )
        )
    elif promptCondition == "C3_parliamentary_context":
        return (
            f"- partyPreset: {partyPreset}",
            (
                "- debateContext: ongoing Bundestag plenary debate\n"
                f"- roleContext: {speakerRole}\n\n"
                "Additional instruction:\n"
                "Use the party preset only as a broad orientation for argumentative emphasis "
                "and policy style.\n"
                "Do not imitate real politicians or known speeches.\n"
                "Do not explicitly name the party unless it fits naturally into the speech."
            )
        )

    return ("", "")