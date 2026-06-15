#!/usr/bin/env python3
import json
import random
import argparse
from collections import defaultdict

def main():
    # Argument-Parser für die Kommandozeile einrichten
    parser = argparse.ArgumentParser(
        description="Entfernt zufällig 50 Einträge pro Modell und Topic für bestimmte Parteien aus einer JSONL-Datei."
    )
    parser.add_argument("-i", "--input", required=True, help="Pfad zur ursprünglichen JSONL-Datei")
    parser.add_argument("-o", "--output", required=True, help="Pfad für die neue, gefilterte JSONL-Datei")
    args = parser.parse_args()

    # Liste der Zielparteien
    target_parties = {"CDU/CSU", "SPD", "Bündnis 90/Die Grünen", "FDP", "AfD"}

    # 1. Alle Einträge einlesen
    alle_eintraege = []
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            for line_idx, line in enumerate(f, 1):
                line = line.strip()
                if line:
                    try:
                        alle_eintraege.append(json.loads(line))
                    except json.JSONDecodeError:
                        print(f"WARNUNG: Ungültiges JSON in Zeile {line_idx} übersprungen.")
    except FileNotFoundError:
        print(f"FEHLER: Die Datei '{args.input}' wurde nicht gefunden.")
        return

    print(f"--> {len(alle_eintraege)} Einträge erfolgreich geladen.")

    # 2. Indizes nach (modelKey, topicFamily, partyPreset) gruppieren
    gruppen = defaultdict(list)
    for index, eintrag in enumerate(alle_eintraege):
        # Nutzt 'modelKey'. Falls du 'modelID' brauchst, hier einfach ändern.
        model = eintrag.get("modelKey") 
        topic = eintrag.get("topicFamily")
        party = eintrag.get("partyPreset")
        
        gruppen[(model, topic, party)].append(index)

    # 3. Bestimmen, welche Indizes gelöscht werden sollen
    indizes_zum_loeschen = set()
    gruppen_zaehler = 0

    for (model, topic, party), indizes in gruppen.items():
        if party in target_parties:
            gruppen_zaehler += 1
            if len(indizes) >= 50:
                gesampelte_indizes = random.sample(indizes, 50)
                indizes_zum_loeschen.update(gesampelte_indizes)
            else:
                indizes_zum_loeschen.update(indizes)
                print(f"Hinweis: Gruppe ({model} | {topic} | {party}) hatte nur {len(indizes)} Einträge. Alle entfernt.")

    print(f"--> {gruppen_zaehler} passende Gruppen (Modell + Topic + Partei) gefunden.")

    # 4. Filterung anwenden und neue Datei schreiben
    geloeschte_anzahl = 0
    gespeicherte_anzahl = 0

    with open(args.output, 'w', encoding='utf-8') as f:
        for index, eintrag in enumerate(alle_eintraege):
            if index in indizes_zum_loeschen:
                geloeschte_anzahl += 1
            else:
                f.write(json.dumps(eintrag, ensure_ascii=False) + '\n')
                gespeicherte_anzahl += 1

    print("\n=== ZUSAMMENFASSUNG ===")
    print(f"Entfernte Einträge: {geloeschte_anzahl}")
    print(f"Verbleibende Einträge: {gespeicherte_anzahl}")
    print(f"Datei erfolgreich gespeichert unter: {args.output}")

if __name__ == "__main__":
    main()