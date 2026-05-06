from synthetic_politics.generator import genMultiple, loadModelConfigs
from synthetic_politics.generation_schemas import GenerationSpecifications
from synthetic_politics.data_helper import readJsonl


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--specs", required=True)
    parser.add_argument("--modelsConfig", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    rows = readJsonl(args.specs)
    specs = [GenerationSpecifications(**row) for row in rows]
    model_cfg = loadModelConfigs(args.modelsConfig)
    genMultiple(specs, model_cfg, args.out)
    print(f"Saved raw generations to {args.out}")
