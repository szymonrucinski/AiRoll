//! In-browser DINOv2 film-shot classifier.
//!
//! The original AiRoll ran a PyTorch/ONNX ResNet server-side. Here the SAME idea
//! runs entirely client-side: `tract` (a pure-Rust ONNX runtime) compiled to WASM
//! executes the DINOv2 graph in the browser — no upload, no server.
//!
//! JS supplies a 224x224 RGBA buffer (it already did resize+centre-crop on a canvas,
//! matching the model's `BitImageProcessor` preprocessing). We only normalise and run.

use std::cell::RefCell;
use std::io::Cursor;
use tract_onnx::prelude::*;
use wasm_bindgen::prelude::*;

// Class order = DINOv2 config id2label (alphabetical), baked in so the page needs no side file.
const LABELS: [&str; 8] = [
    "ambiguous", "closeUp", "detail", "extremeLongShot",
    "fullShot", "longShot", "mediumCloseUp", "mediumShot",
];
// ImageNet stats — model was trained with these, inputs must match.
const MEAN: [f32; 3] = [0.485, 0.456, 0.406];
const STD: [f32; 3] = [0.229, 0.224, 0.225];
const SIDE: usize = 224;

thread_local! {
    // The optimised, runnable plan. Built once from the ONNX bytes, reused per frame.
    static MODEL: RefCell<Option<TypedRunnableModel<TypedModel>>> = const { RefCell::new(None) };
}

fn err<E: std::fmt::Display>(e: E) -> JsValue {
    JsValue::from_str(&e.to_string())
}

/// Parse the ONNX bytes once, fix the input shape, optimise, and cache the plan.
#[wasm_bindgen]
pub fn init_model(onnx_bytes: &[u8]) -> Result<(), JsValue> {
    let model = tract_onnx::onnx()
        .model_for_read(&mut Cursor::new(onnx_bytes))
        .map_err(err)?
        .with_input_fact(0, f32::fact([1, 3, SIDE, SIDE]).into())
        .map_err(err)?
        .into_optimized()
        .map_err(err)?
        .into_runnable()
        .map_err(err)?;
    MODEL.with(|m| *m.borrow_mut() = Some(model));
    Ok(())
}

/// Classify one 224x224 RGBA frame. Returns JSON: [{"label","prob"}...] sorted desc.
#[wasm_bindgen]
pub fn classify(rgba: &[u8]) -> Result<String, JsValue> {
    if rgba.len() != SIDE * SIDE * 4 {
        return Err(err(format!("expected {} RGBA bytes, got {}", SIDE * SIDE * 4, rgba.len())));
    }
    // RGBA(HWC, u8) -> CHW f32, scaled to [0,1] then standardised. ViT wants planar channels.
    let mut data = vec![0f32; 3 * SIDE * SIDE];
    for px in 0..SIDE * SIDE {
        for c in 0..3 {
            let v = rgba[px * 4 + c] as f32 / 255.0;
            data[c * SIDE * SIDE + px] = (v - MEAN[c]) / STD[c];
        }
    }
    let input = tract_ndarray::Array4::from_shape_vec((1, 3, SIDE, SIDE), data)
        .map_err(err)?
        .into_tensor();

    let logits_t = MODEL.with(|m| {
        let b = m.borrow();
        let model = b.as_ref().ok_or_else(|| "model not initialised — call init_model".to_string())?;
        model.run(tvec!(input.into())).map_err(|e| e.to_string())
    }).map_err(err)?;

    let logits = logits_t[0].to_array_view::<f32>().map_err(err)?;
    let logits: Vec<f32> = logits.iter().copied().collect();

    // numerically-stable softmax
    let max = logits.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
    let exps: Vec<f32> = logits.iter().map(|l| (l - max).exp()).collect();
    let sum: f32 = exps.iter().sum();

    let mut ranked: Vec<(usize, f32)> =
        exps.iter().enumerate().map(|(i, e)| (i, e / sum)).collect();
    ranked.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());

    let items: Vec<String> = ranked
        .iter()
        .map(|(i, p)| format!("{{\"label\":\"{}\",\"prob\":{:.4}}}", LABELS[*i], p))
        .collect();
    Ok(format!("[{}]", items.join(",")))
}
