# Synthetic Politics: Measuring Political Bias in Synthetic German Parliamentary Speeches 

**Master Thesis** <br>

**Author: Markus Weinberger** 

---

## Abstract  

This thesis investigates political bias in synthetically generated German parliamentary speeches. As large language models (LLMs) are increasingly used for data augmentation and benchmarking, it is crucial to understand whether they reproduce empirical political discourse or systematically alter it. Using speeches from the 20th legislative period of the German Bundestag as an empirical reference, this study develops a multidimensional framework to measure bias beyond simple ideological alignment. The framework operationalizes bias through three dimensions: stance proximity to empirical faction anchors, rhetorical style framing, and content framing based on Entman’s functional schema. Four LLMs were evaluated across different prompt conditions and political topics. The results demonstrate that synthetic corpora are not a neutral approximation of real Bundestag speech, but systematically transform the empirical distribution of political language. The models exhibit a stance drift away from the AfD, DIE LINKE, and CDU/CSU towards BÜNDNIS 90/DIE GRÜNEN, FDP and the SPD, a shift that cannot be mapped onto a simple one-dimensional scale. Furthermore, framing analyses reveal a robust "rhetorical smoothing" effect, characterized by fewer confrontational markers and a compressed argumentative structure with significantly fewer causal explanations. These findings emphasize that synthetic political data should be treated as transformed data rather than direct substitutes for empirical speech, highlighting the necessity of mechanism-aware bias evaluation in multi-party contexts.


## Run

### Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Required environment variables (example)

```bash
export TOGETHER_API_KEY=...
export OPENROUTER_API_KEY=...
export OPENAI_API_KEY=...
```

### A. Build Specs

```bash
python scripts/build_specs_script.py \
  --datasetConfig config/dataset.yaml \
  --modelsConfig config/models.yaml \
  --out data/specs/specs_v1.jsonl
```

### B. Generate

```bash
python scripts/generate_dataset.py \
  --specs data/specs/specs_v1.jsonl \
  --modelsConfig config/models.yaml \
  --out data/raw/synthetic_raw_generations.jsonl
```




## Citation  

If you use our work, please cite our paper and link this repository:  

```bibtex
@misc{weinberger_2026_syn_pol_bias,  
  title   = {Synthetic Politics: Measuring Political Bias in Synthetic German Parliamentary Speeches},  
  author  = {Weinberger, Markus},  
  month   = jun,  
  year    = {2026},  
  address = {Regensburg, Germany}  
}  
```