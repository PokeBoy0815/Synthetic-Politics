import argparse
from synthetic_politics.generator import genMultiple, loadModelConfigs
from synthetic_politics.generation_schemas import GenerationSpecifications
from synthetic_politics.build_specs import buildSpecs
from synthetic_politics.data_helper import loadYaml, readJsonl, writeJsonl
from synthetic_politics.transform import transformAll




def main():
    parser = buildParser()
    args = parser.parse_args()
    args.func(args)

def cmdBuildSpecs(args):
    datasetCfg = loadYaml(args.datasetConfig)
    modelCfg = loadModelConfigs(args.modelConfig)
    specs = buildSpecs(datasetCfg, list(modelCfg.keys()))
    writeJsonl(args.out,[s.toDict() for s in specs])
    print(f"Saved {len(specs)} specs to {args.out}")

def cmdGenerate(args):
    rows = readJsonl(args.specs)
    specs = [GenerationSpecifications(**row) for row in rows]
    modelCfg = loadModelConfigs(args.modelsConfig)
    genMultiple(specs, modelCfg, args.out)
    print(f"Saved raw generations to {args.out}")

def cmdTransform(args):
    n_speeches, n_chunks = transformAll(args.raw, args.speechOut, args.chunksOut)
    print(f"Saved {n_speeches} speeches and {n_chunks} chunks")

def buildParser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("buildSpecs")
    p1.add_argument("--datasetConfig", required=True)
    p1.add_argument("--models-config", required=True)
    p1.add_argument("--out", required=True)
    p1.set_defaults(func=cmdBuildSpecs)

    p2 = sub.add_parser("generate")
    p2.add_argument("--specs", required=True)
    p2.add_argument("--models-config", required=True)
    p2.add_argument("--out", required=True)
    p2.set_defaults(func=cmdGenerate)

    p3 = sub.add_parser("transform")
    p3.add_argument("--raw", required=True)
    p3.add_argument("--speech-out", required=True)
    p3.add_argument("--chunks-out", required=True)
    p3.set_defaults(func=cmdTransform)

    return parser

if __name__ == "__main__":
    main()