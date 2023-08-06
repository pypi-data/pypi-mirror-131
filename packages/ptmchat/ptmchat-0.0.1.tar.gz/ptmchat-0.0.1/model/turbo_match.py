import turbo_transformers
import json
import os
import torch
from model.ernie import ErnieMatch


class ErnieMatchTurbo:
    """
    带有全连接head的ernie模型用于微调匹配任务
    turbo transformer加速推理版，直接加载微调好的整个模型的参数
    bert_model是turbo类，其他层是torch类
    """
    def __init__(self, config):
        self.pkl = config['rank']['match_checkpoint']
        self.model = ErnieMatch()
        self.tokenizer = self.model.tokenizer
        # put model to GPU if available
        if torch.cuda.is_available():
            self.model = self.model.cuda()
        # 加载参数
        if os.path.exists(self.pkl):
            self.model.load_state_dict(torch.load(self.pkl, map_location='cpu'))
        else:
            raise FileNotFoundError(f'the checkpoint file {self.pkl} is not found!')
        self.model.eval()

        self.bert_model = turbo_transformers.BertModel.from_torch(self.model.pretrain)
        self.dropout = self.model.dropout
        self.fc1 = self.model.fc1
        self.fc2 = self.model.fc2

    def __call__(self, x, mask=None, seg=None):
        sequence_output, pooled_output = self.bert_model(x, attention_masks=mask, token_type_ids=seg)
        output = self.dropout(pooled_output)
        output = self.fc1(output)
        output = self.fc2(output).squeeze()
        return output


if __name__ == '__main__':
    from rank.ranker import ErnieRanker
    from model.ernie import convert_list_to_features, new_tensor
    os.environ["CUDA_VISIBLE_DEVICES"] = '2'
    # use 4 threads for BERT inference
    turbo_transformers.set_num_threads(4)

    # the initialization of the acceleration model
    config_file = "../config/config.json"
    with open(config_file, 'r') as f:
        config_info = json.load(f)
    turbo_model = ErnieMatchTurbo(config_info)

    # predict after loading the model
    context = '你好'
    response = ['再见'] * 20
    input_ids, input_mask, segment_ids = convert_list_to_features(context, 30, turbo_model.tokenizer, response)
    input_ids = new_tensor(input_ids)
    input_mask = new_tensor(input_mask)
    segment_ids = new_tensor(segment_ids)

    turbo_result = turbo_model(input_ids, input_mask, segment_ids)

    # compare
    torch_model = ErnieRanker(config_info)
    torch_model.load_model()
    torch_result = torch_model.model(input_ids, input_mask, segment_ids)
    print(turbo_result)
    print(torch_result)
