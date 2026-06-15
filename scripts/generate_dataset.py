from synthetic_politics.generator import genMultiple, loadModelConfigs
from synthetic_politics.generation_schemas import GenerationSpecifications
from synthetic_politics.data_helper import readJsonl
<<<<<<< HEAD
=======
import os
import json
>>>>>>> full-synthesis


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--specs", required=True)
    parser.add_argument("--modelsConfig", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    rows = readJsonl(args.specs)
<<<<<<< HEAD
    specs = [GenerationSpecifications(**row) for row in rows]
    model_cfg = loadModelConfigs(args.modelsConfig)
    genMultiple(specs, model_cfg, args.out)
    print(f"Saved raw generations to {args.out}")
=======
    allSpecs = [GenerationSpecifications(**row) for row in rows]
    model_cfg = loadModelConfigs(args.modelsConfig)

    #eine resume logik, für dne fall, dass nicht alle auf einmal durchlaufen
    processedIDs = set()
    if os.path.exists(args.out):
        with open(args.out, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        data = json.loads(line)
                        #eindeutiger identifikator
                        processedIDs.add(data.get("sampleID")) 
                    except json.JSONDecodeError:
                        continue

    #specs filtern
    specsToProcess = [spec for spec in allSpecs if spec.sampleID not in processedIDs]

    print(f"Gefunden: {len(allSpecs)} Specs insgesamt.")
    print(f"Bereits erledigt: {len(processedIDs)}. Starte Verarbeitung der restlichen {len(specsToProcess)} Specs.")

    #gefilterte lsite übergeben
    if specsToProcess:
        genMultiple(specsToProcess, model_cfg, args.out)
        print(f"Saved raw generations to {args.out}")
    else:
        print("Alle Specs wurden bereits generiert. Beende Skript.")

    """
    genMultiple(specs, model_cfg, args.out)
    print(f"Saved raw generations to {args.out}")
    """
>>>>>>> full-synthesis
