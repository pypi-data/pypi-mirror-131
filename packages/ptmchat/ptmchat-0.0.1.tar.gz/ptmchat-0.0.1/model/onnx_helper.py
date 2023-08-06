import numpy as np
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit


class ONNXClassifierWrapper:
    def __init__(self, file, out_size, target_dtype=np.float32):
        self.target_dtype = target_dtype
        self.out_size = out_size
        self.load(file)
        self.stream = None

    def load(self, file):
        f = open(file, "rb")
        runtime = trt.Runtime(trt.Logger(trt.Logger.WARNING))
        engine = runtime.deserialize_cuda_engine(f.read())
        self.context = engine.create_execution_context()

    def allocate_memory(self, input1, input2, input3):
        # Need to set both input and output precisions to FP16 to fully enable FP16
        self.output = np.empty(self.out_size, dtype=self.target_dtype)

        # Allocate device memory
        self.d_input1 = cuda.mem_alloc(1 * input1.nbytes)
        self.d_input2 = cuda.mem_alloc(1 * input2.nbytes)
        self.d_input3 = cuda.mem_alloc(1 * input3.nbytes)
        self.d_output = cuda.mem_alloc(1 * self.output.nbytes)

        self.bindings = [int(self.d_input1), int(self.d_input2), int(self.d_input3), int(self.d_output)]

        self.stream = cuda.Stream()

    def predict(self, input1, input2, input3):  # result gets copied into output
        if self.stream is None:
            self.allocate_memory(input1, input2, input3)

        # Transfer input data to device
        cuda.memcpy_htod_async(self.d_input1, input1, self.stream)
        cuda.memcpy_htod_async(self.d_input2, input2, self.stream)
        cuda.memcpy_htod_async(self.d_input3, input3, self.stream)
        # Execute model
        self.context.execute_async_v2(self.bindings, self.stream.handle, None)
        # Transfer predictions back
        cuda.memcpy_dtoh_async(self.output, self.d_output, self.stream)
        # Syncronize threads
        self.stream.synchronize()

        return self.output


if __name__ == '__main__':
    import os
    import json
    import sys
    sys.path.append('../')
    from transformers import BertTokenizer
    from rank.ranker import ErnieRanker
    from model.ernie import convert_list_to_features, new_tensor

    os.environ["CUDA_VISIBLE_DEVICES"] = '5'

    batch_size = 20
    trt_model = ONNXClassifierWrapper("ernie_match.trt", batch_size)

    # config_file = "../config/config.json"
    # with open(config_file, 'r') as f:
    #     config_info = json.load(f)
    # torch_model = ErnieRanker(config_info)
    # torch_model.load_model()

    # predict after loading the model
    query = '请问'
    response = ['哈哈', '你好', '什么东西？', '呵呵哒', '你要问啥？', '哈哈', '你好', '什么东西？', '呵呵哒', '你要问啥？', '哈哈', '你好', '什么东西？', '呵呵哒', '你要问啥？', '哈哈', '你好', '什么东西？', '呵呵哒', '你要问啥？']
    tokenizer = BertTokenizer.from_pretrained("nghuyong/ernie-1.0")
    input_ids, input_mask, segment_ids = convert_list_to_features(query, 30, tokenizer, response)
    input_ids = np.asarray(input_ids, dtype=np.int32)
    input_mask = np.asarray(input_mask, dtype=np.int32)
    segment_ids = np.asarray(segment_ids, dtype=np.int32)

    trt_result = trt_model.predict(input_ids, input_mask, segment_ids)
    print(trt_result)

    # input_ids = new_tensor(input_ids)
    # input_mask = new_tensor(input_mask)
    # segment_ids = new_tensor(segment_ids)
    #
    # # compare
    # torch_model.model.eval()
    # torch_result = torch_model.model(input_ids, input_mask, segment_ids)
    # print(torch_result.detach().cpu().numpy())
