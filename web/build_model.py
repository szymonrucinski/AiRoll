"""Reproducible: pszemraj/dinov2-small-film-shot-classifier -> tract-friendly ONNX.

Run:  python web/build_model.py   (writes docs/dinov2_shot_tract.onnx)

Why each step matters for the pure-Rust `tract` WASM runtime:
  * opset 16  -> LayerNormalization is emitted as primitive ops (tract has no fused LN)
  * STATIC batch (no dynamic_axes) -> no Sym(batch); tract can't unify Sym with Val(1)
  * onnxsim   -> constant-folds the bicubic Resize (pos-embed interpolation) away;
                 tract only supports nearest/linear Resize, so it must vanish.
Deps: pip install torch transformers onnx onnxsim onnxruntime
"""
import numpy as np, onnx, torch, onnxruntime as ort
from onnxsim import simplify
from transformers import AutoModelForImageClassification

REPO = "pszemraj/dinov2-small-film-shot-classifier"
OUT = "dinov2_shot_tract.onnx"  # upload to HF, don't commit (the app fetches it from HF at runtime)
# upload:  huggingface-cli upload szymonrucinski/what-a-shot dinov2_shot_tract.onnx

m = AutoModelForImageClassification.from_pretrained(REPO, torchscript=True).eval()
torch.onnx.export(m, (torch.randn(1, 3, 224, 224),), "/tmp/_dinov2.onnx",
                  input_names=["pixel_values"], output_names=["logits"],
                  opset_version=16, dynamo=False)  # NOTE: no dynamic_axes -> static batch
simp, ok = simplify(onnx.load("/tmp/_dinov2.onnx"))
assert ok, "onnxsim failed"
onnx.save(simp, OUT)

x = torch.randn(1, 3, 224, 224)
with torch.no_grad():
    ref = m(x)[0].numpy()
got = ort.InferenceSession(OUT, providers=["CPUExecutionProvider"]).run(None, {"pixel_values": x.numpy()})[0]
assert np.abs(ref - got).max() < 1e-3 and ref.argmax() == got.argmax()
print(f"wrote {OUT}  (max diff {np.abs(ref - got).max():.1e}, argmax ok)")
