import os
import torch
from model.ernie import ErnieMatch, infer_batch


class ErnieRanker:
    def __init__(self, config):
        """
        精排模型
        :param args:
        """
        super().__init__()
        self.max_seq_len = config['rank']['max_seq_len']
        self.pkl = config['rank']['match_checkpoint']
        # 加载模型
        self.model = ErnieMatch()
        self.tokenizer = self.model.tokenizer
        # put model to GPU if available
        if torch.cuda.is_available():
            self.model = self.model.cuda()

    def load_model(self):
        """
        加载一个模型文件
        :return: 无返回值。
        """
        if os.path.exists(self.pkl):
            self.model.load_state_dict(torch.load(self.pkl, map_location='cpu'))
        else:
            raise FileNotFoundError(f'the checkpoint file {self.pkl} is not found!')
        self.model.eval()

    def predict(self, contexts, responses):
        """
        调用模型批量预测所有历史和回复对的match分数，选择最高的一个
        :param contexts: 一批历史
        :param responses: 一批回复
        :return: 最好的一个回复。
        """
        logits = infer_batch(contexts, self.model, self.tokenizer, self.max_seq_len, responses)
        logits = torch.sigmoid(logits)
        score = torch.max(logits).item()
        pred = torch.argmax(logits).item()
        return responses[pred], score