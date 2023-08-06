### 基于预训练模型的开放域聊天

#### 基本流程
1. 通过ERINE1.0获得候选语句、查询语句的向量化表达
2. 通过FaissGPU，进行语义近似召回，获得Top候选相关文档ID列表
3. 通过ElasticSearch，进一步过滤候选相关文档
4. 通过基于ERNIE1.0的排序模型，进行Context与Response的相关性排序，返回Response

#### 服务部署
1. chat.py：人机多轮聊天的服务
2. run.py：使用pytorch的pkl模型文件，不进行推理加速的服务

#### 推理加速实验
1. run_onnx.py：先使用model目录下的convert.py将pytorch模型文件转换为onnx格式模型文件，再使用onnx格式的模型文件启动服务，目前最佳的推理加速方案。
2. run_turbo.py：使用腾讯的turbo transformers进行推理加速，参考https://github.com/Tencent/TurboTransformers
&nbsp;&nbsp;先下载包含turbo transformers库的docker镜像，然后启动服务
3. run_trt.py：参见trt guide.txt文件进行tensorrt相关环境的安装，onnx文件转trt文件。
&nbsp;&nbsp;基于trt模型文件，启动tensorrt推理加速的服务