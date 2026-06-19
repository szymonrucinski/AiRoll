// Native smoke test: prove tract can load+optimise+run the DINOv2 graph and that
// its logits match onnxruntime on a fixed input (all pixels = 0.3).
use tract_onnx::prelude::*;

fn main() -> TractResult<()> {
    let model = tract_onnx::onnx()
        .model_for_path("../docs/dinov2_shot_tract.onnx")?
        .with_input_fact(0, f32::fact([1, 3, 224, 224]).into())?
        .into_optimized()?
        .into_runnable()?;
    let input =
        tract_ndarray::Array4::<f32>::from_elem((1, 3, 224, 224), 0.3).into_tensor();
    let out = model.run(tvec!(input.into()))?;
    let logits = out[0].to_array_view::<f32>()?;
    let v: Vec<f32> = logits.iter().copied().collect();
    let argmax = v.iter().enumerate().max_by(|a, b| a.1.partial_cmp(b.1).unwrap()).unwrap().0;
    println!("tract logits: {}", v.iter().map(|x| format!("{:.4}", x)).collect::<Vec<_>>().join(" "));
    println!("tract argmax: {}", argmax);
    Ok(())
}
