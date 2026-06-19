# What a Shot — in-browser film-shot classifier

DINOv2 shot-type classifier ([pszemraj/dinov2-small-film-shot-classifier](https://huggingface.co/pszemraj/dinov2-small-film-shot-classifier),
trained on [szymonrucinski/types-of-film-shots](https://huggingface.co/datasets/szymonrucinski/types-of-film-shots))
running **100% client-side**: Rust + [`tract`](https://github.com/sonos/tract) (pure-Rust ONNX runtime)
compiled to WebAssembly. No server, no upload. Served from `docs/` on GitHub Pages.

8 classes: `ambiguous, closeUp, detail, extremeLongShot, fullShot, longShot, mediumCloseUp, mediumShot`.

## Build

The 87 MB ONNX is **not committed** — it lives on HF (`szymonrucinski/what-a-shot`) and the app
fetches it at runtime (the browser caches it). Only the small WASM + HTML are in the repo.

```bash
# 1. model: HF DINOv2 -> tract-friendly ONNX, then push to HF (one-off, only if retraining)
python web/build_model.py
huggingface-cli upload szymonrucinski/what-a-shot dinov2_shot_tract.onnx

# 2. wasm: Rust classifier -> docs/pkg/
cd web && wasm-pack build --target web --release --out-dir ../docs/pkg

# 3. serve (ES modules + fetch need HTTP, not file://)
cd ../docs && python -m http.server 8099   # open http://localhost:8099
```

## How it works
- `build_model.py` exports the ViT at **static batch=1, opset 16**, then `onnxsim` constant-folds
  the bicubic pos-embedding `Resize` away — leaving only ops `tract` supports.
- `src/lib.rs`: `init_model(bytes)` optimises the graph once; `classify(rgba)` normalises a
  224×224 RGBA frame (ImageNet stats) and runs inference, returning ranked `{label, prob}` JSON.
- `index.html`: canvas does resize-256 + centre-crop-224 (matching the model's preprocessing),
  hands the buffer to WASM.

Single-threaded WASM → no `SharedArrayBuffer` → no COOP/COEP headers → works on plain GitHub Pages.

## Roadmap
- int8-quantise the ONNX (~87 MB → ~22 MB) for faster first load.
- Reuse this engine for full AiRoll: classify every clip's frames, then the beat-cut/stabilise pipeline.
