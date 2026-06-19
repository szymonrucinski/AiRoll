<div align="center">

<img src="docs/assets/banner.png" alt="AiRoll — AI movie editor" width="100%">

### Drop clips + song. Robot cut montage to beat. Name every shot.

[**▶ Try live (Hugging Face Space)**](https://huggingface.co/spaces/szymonrucinski/what-a-shot)
&nbsp;·&nbsp;
[**Dataset**](https://huggingface.co/datasets/szymonrucinski/types-of-film-shots)
&nbsp;·&nbsp;
[**Model**](https://huggingface.co/szymonrucinski/what-a-shot)

`DINOv3` · `ONNX` · `Gradio` · `librosa` · `Rust/WASM` · `no CUDA needed`

</div>

---

## What AiRoll do

Old engineering-thesis idea, now alive. Two brains in one box:

- **Shot brain** — look at film frame, say shot scale: *close-up, medium, full, long, extreme-long, detail*. Vision model (DINOv3), runs on CPU.
- **Edit brain** — hear song beat (librosa), cut clips to beat, paint shot-name top-right, glue montage with music. moviepy do the rendering.

Drop few short clips + one track → get montage cut to rhythm. No editing skill needed.

## Brains (models)

Same dataset, model got smarter each round. Score = balanced accuracy on **human gold** test split.

| model | backbone | trained on | human-gold balanced acc |
|-------|----------|-----------|:--:|
| v2 | DINOv2-small | 925 human | 0.71 |
| v3 | DINOv3-small | 2.9K (human + AI) | 0.78 |
| **v4** | DINOv3-small | **53K (1000 films, Opus-checked)** | 0.75 · **live (int8)** |

v3 edges v4 on the small gold test (~1.5 σ, basically noise), but **v4 saw 53× more films** — far more varied lighting / eras / framing — so it should hold up better on real clips. Deployed as **int8 ONNX (22 MB, 4× smaller)** for fast free-CPU inference; fp32 also on the Hub.

> **Lesson baked in:** training on bulk *self-labels* (v3's own predictions) did not beat v3 on gold — a model can't out-learn its own teacher. The win is diversity + Opus-fixing the hard tail, not raw self-label count.

## Data — how 925 became 56K

Cheap-model-do-bulk, smart-model-fix-hard. Classic active learning.

```
scrape 1000+ films (film-grab.com, HTTP, no Selenium)  ->  62K frames
   -> DINOv3 label all + give confidence
        |-- confident frame -> trust it
        \-- unsure frame     -> Claude Opus re-judge (best labeler, 95% on gold)
   -> split: train (all AI, ~55K)  +  test (human gold, 863)
```

Why this way: cheap GPT vision flunked shot-scale (42%). Own DINOv3 beat it (90% on easy frames). So **own model do bulk, Opus fix the unsure tail.** Each row keeps `annotator` (human/ai), `source`, `confidence` — filter or weight how you like.

**[Dataset on the Hub ->](https://huggingface.co/datasets/szymonrucinski/types-of-film-shots)** &nbsp; 8 shot classes · `train` 55K · `test` 863 human.

## Reproduce

```bash
# 1. brain: train shot classifier (DINOv3-small) on the Hub dataset
python train_v4.py                 # validates on human gold, writes dinov3_shot_v4.onnx

# 2. shrink: fp32 ONNX -> int8 (smaller, faster CPU)
python quantize_int8.py            # -> dinov3_shot_v4_int8.onnx

# 3. scale data (optional): scrape + label more films
python scaleup/scrape.py           # film pages -> frame URLs
python scaleup/download_label.py   # download + DINOv3 label + confidence

# 4. run the app locally (Gradio)
pip install -r requirements.txt
python app.py                      # or open the Space above
```

Model auto-downloads from the Hub at runtime — nothing huge lives in this repo.

## Repo map

| path | what |
|------|------|
| `app.py`, `airoll.py` | the Gradio app (montage + shot overlay + music window) |
| `train_v3.py`, `train_v4.py` | finetune DINOv3 shot classifier |
| `quantize_int8.py` | fp32 ONNX -> int8 |
| `scaleup/` | the data-scaling pipeline (scrape -> label -> review -> build) |
| `web/` | Rust/`tract` WASM build — same classifier, 100% in-browser |
| `docs/` | static demo + assets |

## Credit

Frames from [film-grab.com](https://film-grab.com). Backbone [DINOv3](https://huggingface.co/facebook/dinov3-vits16-pretrain-lvd1689m) (Meta). Dataset CC-BY-4.0. Built by [Szymon Ruciński](https://huggingface.co/szymonrucinski).
