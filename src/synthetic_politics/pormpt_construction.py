import yaml
from pathlib import Path

def build_message(specification):
    return [{"role": "system", "content": loadSysPrompt()}, {"role": "user", "content": buildUserPrompt(specification)}]

def loadSysPrompt():
    path = Path(__file__).parent.parent.parent / "config" / "sys_prompt.yaml"
    with open(path, "r", encoding="utf-8") as f:
        #print(yaml.safe_load(f))
        return yaml.safe_load(f).get("systemPrompt", "")

def buildUserPrompt(spec):
    sampleID = _get(spec, "sampleID", "")
    topicFamily = _get(spec, "topicFamily", "")
    subTopic = _get(spec, "subTopic", "")
    speakerRole = _get(spec, "speakerRole", "")
    textType = _get(spec, "textType", "")
    targetLength = _get(spec, "targetLength", "")
    register = _get(spec, "register", "")
    issueFocus = _get(spec, "issueFocus", "")
    speechGoal = _get(spec, "speechGoal", "")
    requiredAspects = _get(spec, "requiredAspects", []) or []

    partyLine, contextLine = makeOptional(spec)

    issueFocusPart = f"- issueFocus: {issueFocus}" if issueFocus else ""
    speechGoalPart = f"- speechGoal: {speechGoal}" if speechGoal else ""
    requiredAspectsPart= _formatRequiredAspects(requiredAspects)

    promptCondition = _get(spec, "promptCondition", "minC1")

    if promptCondition != "minC1":
        partyPreset = "Wenn eine Partei angegeben ist, kopiere sie exakt in das JSON Feld 'partyPreset'"
    else:
        partyPreset = "Wenn keine Partei angegeben ist, setze 'partyPreset' als leeren Strin in der JSON"

    return f"""
Kontext:
- sampleID: {sampleID}
- topicFamily: {topicFamily}
- subTopic: {subTopic}
- speakerRole: {speakerRole}
- textType: {textType}
- setting: Plenardebatte des deutschen Budestags
- register: {register}
- {partyLine}
- {issueFocusPart}
- {speechGoalPart}
- {requiredAspectsPart}
{contextLine}

Task:
Schreibe eine eigene deutsche Parlamentsrede.

Die Rede sollte:
- den issue focus direkt adressieren,
- das speech goal als kommunikative funktion des Texts nutzen,
- alle erforderlichen Aspekte auf schlüssige Weise abdecken, sofern diese Aspekte angegeben sind,
- wie ein plausibler Beitrag in einer aktuellen Plenarsitzung des Bundestages klingen,
- mit einer politischen Bewertung, einer Forderung oder einem Vorschlag abschließen.

Gliedere die Rede wie folgt:
- eine kurze Einleitung zum Thema,
- einen ausführlichen Hauptteil, der mehrere konkrete Aspekte behandelt,
- eine abschließende politische Bewertung, eine Forderung oder einen Vorschlag.

Anforderungen:
- Der Text muss auf Deutsch verfasst sein.
- Gib nur ein JSON-Objekt aus.
- Deine Antwort muss mit „{{“ beginnen und mit „}}“ enden.
- Füge keine einleitenden Sätze wie „Hier ist die JSON-Ausgabe“ hinzu.
- Füge keinen Text vor dem öffnenden „{{“ oder nach dem schließenden „}}“ ein.
- Der Text sollte wie ein plausibler Beitrag in einer Plenardebatte des Bundestages klingen.
- Er muss originell sein und darf keiner bekannten Rede zu sehr ähneln.
- Vermeide theatralische, archaische oder unplausible parlamentarische Formulierungen.
- Verwende einen nüchternen, politikorientierten parlamentarischen Ton.
- Verwende plausible Anredeformen im Stil des Bundestages wie „Herr Präsident“, „Frau Präsidentin“ oder „Meine Damen und Herren“.
- Verwende keine Formen wie „Herr/Frau Präsidentin“, „Ehrwürdige Abgeordneten“, „Guten Tag“ oder „Herr Abgeordneter“.
- Füge keine Metadaten in den Redetext ein.
- Füge keine Erklärungen oder Anmerkungen ein.
- Füge keine Markdown-Fences ein.
- Übernimm Metadatenfelder exakt aus dem bereitgestellten Kontext, sofern vorhanden.
- Erfinde oder ändere keine Metadatenwerte.
- {partyPreset}
- Verfasse etwa {targetLength} Wörter.
- Verfasse mindestens 8 vollständige Sätze.
- Verfasse mindestens 3 Absätze von nennenswerter Länge.
- Behandle alle erforderlichen Aspekte als wesentliche Bestandteile der Rede, nicht als kurze Liste.
- Jeder erforderliche Aspekt sollte in mindestens einem vollständigen Satz behandelt werden.

Gib gültiges JSON mit den folgenden Keys zurück:
sampleID, topicFamily, subTopic, partyPreset, speakerRole, textType, register, generatedText
""".strip()


#dict und objektartige specifications können eingelsesn werden
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

#gibt partyLine und ContextLine aus
def makeOptional(spec):
    promptCondition = _get(spec, "promptCondition", "minC1")
    partyPreset = _get(spec, "partyPreset", "")
    speakerRole =_get(spec, "speakerRole", "")

    if promptCondition == "minC1":
        return ("", "")
    elif promptCondition == "partyPresC2":
        return (
            f"- partyPreset: {partyPreset}",
            (
                "Zusätzliche Anweisungen:\n"
                "Wenn ein party preset angegeben ist, verwende diesen nur als grobe Orientierung für argumentative Schwerpunkte und den Stil der Rede.\n"
                "Imitiere keine echten Politiker oder bekannte Reden.\n"
                "Nenne die Partei nicht ausdrücklich, es sei denn, dies fügt sich ganz natürlich in die Rede ein."
            )
        )
    elif promptCondition == "parlamContextC3":
        return (
            f"- partyPreset: {partyPreset}",
            (
                "- debateContext: laufende Plenardebatte im Bundestag\n"
                f"- roleContext: {speakerRole}\n\n"
                "Zusätzliche Anweisungen:\n"
                "Verwende den party preset nur als grobe Orientierung für argumentative Schwerpunkte und den politischen Stil.\n"
                "Imitiere keine echten Politiker oder bekannte Reden.\n"
                "Nennen die Partei nicht ausdrücklich, es sei denn, dies fügt sich natürlich in die Rede ein."
            )
        )

    return ("", "")