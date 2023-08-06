# 转化模型为onnx格式
import os
import numpy as np
import torch
import onnx
import onnxruntime
from onnxruntime.transformers import optimizer
from onnxruntime.transformers.onnx_model_bert import BertOptimizationOptions
from model.ernie import ErnieMatch, read_examples, convert_examples_to_features, new_tensor

os.environ["CUDA_VISIBLE_DEVICES"] = '4'

# 加载模型
pkl_checkpoint = "../resources/17.pkl"
torch_model = ErnieMatch()
if torch.cuda.is_available():
    torch_model = torch_model.cuda()

if os.path.exists(pkl_checkpoint):
    torch_model.load_state_dict(torch.load(pkl_checkpoint, map_location='cpu'))
else:
    raise FileNotFoundError(f'the resources file {pkl_checkpoint} is not found!')

# set the model to inference mode
torch_model.eval()

# 任意输入，固定维度
max_seq_len = 30
batch_size = 20
context = ['你好'] * batch_size
response = ['再见'] * batch_size
predict_examples = read_examples(context, response)
features, all_tokens = convert_examples_to_features(predict_examples, max_seq_len, torch_model.tokenizer)
# input_ids [bs_size, seq_len]
input_ids = new_tensor([f.input_ids for f in features])
# input_mask [bs_size, seq_len]
input_mask = new_tensor([f.input_mask for f in features])
# segment_ids [bs_size, seq_len]
segment_ids = new_tensor([f.segment_ids for f in features])
torch_out = torch_model(input_ids, mask=input_mask, seg=segment_ids)

# 进行转化
torch.onnx.export(torch_model,  # model being run
                  (input_ids, input_mask, segment_ids),  # model input (or a tuple for multiple inputs)
                  "ernie_match.onnx",  # where to save the model (can be a file or file-like object)
                  export_params=True,  # store the trained parameter weights inside the model file
                  opset_version=11,  # the ONNX version to export the model to
                  do_constant_folding=True,  # whether to execute constant folding for optimization
                  keep_initializers_as_inputs=False,
                  input_names=['input_ids', 'input_mask', 'segment_ids'],  # the model's input names
                  output_names=['output'])  # the model's output names

# optimized_model = optimizer.optimize_model("ernie_match_raw.onnx", model_type='bert', num_heads=12, hidden_size=768, opt_level=99, use_gpu=True)
# # optimized_model.convert_model_float32_to_float16()  # only for gpu with tensor core
# optimized_model.save_model_to_file("ernie_match.onnx")


onnx_model = onnx.load("ernie_match.onnx")
onnx.checker.check_model(onnx_model)

so = onnxruntime.SessionOptions()
so.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL
ort_session = onnxruntime.InferenceSession("ernie_match.onnx", sess_options=so)
# ort_session = onnxruntime.InferenceSession("ernie_match.onnx")
ort_session.set_providers(['CUDAExecutionProvider'])
ort_inputs = {
    ort_session.get_inputs()[0].name: input_ids.cpu().numpy(),
    ort_session.get_inputs()[1].name: input_mask.cpu().numpy(),
    ort_session.get_inputs()[2].name: segment_ids.cpu().numpy()
}
ort_outs = ort_session.run(None, ort_inputs)

# compare ONNX Runtime and PyTorch results
np.testing.assert_allclose(torch_out.detach().cpu().numpy(), ort_outs[0], rtol=1e-03, atol=1e-05)
print("Exported model has been tested with ONNXRuntime, and the result looks good!")
