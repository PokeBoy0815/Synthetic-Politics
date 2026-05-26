from synthetic_politics.generator import loadModelConfigs
from synthetic_politics.build_specs import buildSpecs
from synthetic_politics.data_helper import loadYaml, writeJsonl

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--datasetConfig", required=True)
    parser.add_argument("--modelsConfig", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    print("this is args: " + args.datasetConfig)

    datasetCfg = loadYaml(args.datasetConfig)
    modelCfg = loadModelConfigs(args.modelsConfig)
    specs = buildSpecs(datasetCfg, list(modelCfg.keys()))
    writeJsonl(args.out, [s.toDict() for s in specs])
    print(f"Saved {len(specs)} specs to {args.out}")
