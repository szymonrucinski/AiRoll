"""fp32 ONNX -> int8 (dynamic quantization). Smaller file, faster on CPU.
Dynamic quant needs no calibration data — it int8s the weights, keeps activations fp32.
Usage: python quantize_int8.py [in.onnx] [out.onnx]
"""
import sys, os, numpy as np, onnxruntime as ort
from onnxruntime.quantization import quantize_dynamic, QuantType

SRC = sys.argv[1] if len(sys.argv) > 1 else "dinov3_shot_v4.onnx"
DST = sys.argv[2] if len(sys.argv) > 2 else SRC.replace(".onnx", "_int8.onnx")

quantize_dynamic(SRC, DST, weight_type=QuantType.QInt8)

# sanity: int8 should still agree with fp32 on argmax
x = np.random.rand(1, 3, 224, 224).astype(np.float32)
def run(p):
    s = ort.InferenceSession(p, providers=["CPUExecutionProvider"])
    return s.run(None, {s.get_inputs()[0].name: x})[0][0]
f32, i8 = run(SRC), run(DST)
print(f"{SRC} {os.path.getsize(SRC)/1e6:.1f}MB -> {DST} {os.path.getsize(DST)/1e6:.1f}MB")
print("argmax agree:", int(f32.argmax()) == int(i8.argmax()), "| max logit diff:", float(np.abs(f32 - i8).max()))
