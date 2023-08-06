import torch
from transformers import BertTokenizer, BertModel
import sys

sys.path.append("..")
import numpy as np


class InputExample(object):
    """
    构造的输入对象，包括id和内容。
    Attributes:
        unique_id: 编号。
        a: 第一句
        b: 第二句
    """

    def __init__(self, unique_id, a, b=None):
        self.unique_id = unique_id
        self.a = a
        self.b = b


class InputFeatures(object):
    """
    构造的特征对象。
    Attributes:
        input_ids: 输入的token。
        segment_ids: 用于区分不同句子的序号。
        input_mask: mask。
    """

    def __init__(self, input_ids, segment_ids, input_mask):
        self.input_ids = input_ids
        self.segment_ids = segment_ids
        self.input_mask = input_mask


def new_tensor(array, requires_grad=False):
    """
    构建一个新的不参与反向传播的张量，如果gpu可用就放置到gpu上。
    Args:
        array: 待构建向量的原始数据。
        requires_grad: 是否需要参与反向传播。
    Returns:
        构建好的张量。
    """
    if torch.cuda.is_available():
        tensor = torch.as_tensor(array, device=torch.cuda.current_device())
        tensor.requires_grad_(requires_grad)
    else:
        tensor = torch.as_tensor(array)
        tensor.requires_grad_(requires_grad)
    return tensor


def read_examples(a_list, b_list=None):
    """
    读取句子构造InputExample对象。
    Args:
        a_list: 样本第一句列表。
        b_list: 样本第二句列表。
    Returns:
        构造的InputExample对象集。
    """
    examples = []
    unique_id = 0
    if b_list:
        for a, b in zip(a_list, b_list):
            examples.append(InputExample(unique_id, a, b))
            unique_id += 1
        return examples
    else:
        for a in a_list:
            examples.append(InputExample(unique_id, a))
            unique_id += 1
        return examples


def convert_examples_to_features(examples, max_seq_length, tokenizer):
    """
    把一系列InputExample对象转换为一系列InputFeatures对象。
    Args:
        examples: InputExample对象集。
        max_seq_length: 最大长度。
        tokenizer: 分词函数。
    Returns:
        转换得到的InputFeatures对象集，以及所有语句序列的token。
    """
    all_features = []
    all_tokens = []
    for example in examples:
        feature, tokens = convert_single_example(example, max_seq_length, tokenizer)
        all_features.append(feature)
        all_tokens.append(tokens)
    return all_features, all_tokens


def convert_list_to_features(a, max_seq_length, tokenizer, b_list):
    """
    把句子列表转换为特征id。适用于匹配阶段，更快。
    Args:
        a: 第一句。
        max_seq_length: 最大长度。
        tokenizer: 分词函数。
        b_list: 第二句列表。
    Returns:
        转换得到的所有样本的输入id，mask id，以及segment id。
    """
    a_tokens = tokenizer.tokenize(a)
    a_len = len(a_tokens)
    b_tokens_list = list(map(tokenizer.tokenize, b_list))
    max_half = max_seq_length // 2
    input_ids = []
    input_masks = []
    segment_ids = []
    for b_tokens in b_tokens_list:
        b_len = len(b_tokens)
        if a_len > b_len:
            a_len_trunc = max(max_half, max_seq_length - b_len)
            b_len_trunc = min(max_half, b_len)
        else:
            a_len_trunc = min(max_half, a_len)
            b_len_trunc = max(max_half, max_seq_length - a_len)
        # 截断前面
        a_tokens_trunc = a_tokens[-a_len_trunc:]
        # 截断后面
        b_tokens_trunc = b_tokens[:b_len_trunc]
        tokens = ["[CLS]"] + a_tokens_trunc + ["[SEP]"] + b_tokens_trunc + ["[SEP]"]
        ids = tokenizer.convert_tokens_to_ids(tokens)
        ids_len = len(ids)
        pad_ids = ids + [0] * (max_seq_length + 3 - ids_len)
        input_ids.append(pad_ids)
        mask = [1] * ids_len + [0] * (max_seq_length + 3 - ids_len)
        input_masks.append(mask)
        seg = [0] * (len(a_tokens_trunc) + 2) + [1] * (len(b_tokens_trunc) + 1) + [0] * (max_seq_length + 3 - ids_len)
        segment_ids.append(seg)

    input_ids = np.stack(input_ids, axis=0)
    input_masks = np.stack(input_masks, axis=0)
    segment_ids = np.stack(segment_ids, axis=0)

    return input_ids, input_masks, segment_ids


def _truncate_seq_pair(tokens_a, tokens_b, max_length):
    total_length = len(tokens_a) + len(tokens_b)
    while True:
        if total_length <= max_length:
            break
        if len(tokens_a) > len(tokens_b):
            tokens_a.pop()
        else:
            tokens_b.pop()
        total_length -= 1


def convert_single_example(example, max_seq_length, tokenizer):
    """
    把一个InputExample对象转换为一个InputFeatures对象。
    Args:
        example: 一个InputExample对象。
        max_seq_length: 最大长度。
        tokenizer: 分词函数。
    Returns:
        处理后的Inputfeature对象，和对应序列的id表示。
    """
    a_tokens = tokenizer.tokenize(example.a)
    b_tokens = None
    if example.b:
        b_tokens = tokenizer.tokenize(example.b)
    if b_tokens:
        _truncate_seq_pair(a_tokens, b_tokens, max_seq_length)
    else:
        a_tokens = a_tokens[:max_seq_length]

    tokens = ["[CLS]"]
    segment_ids = [0]
    for token in a_tokens:
        tokens.append(token)
        segment_ids.append(0)
    tokens.append("[SEP]")
    segment_ids.append(0)

    if b_tokens:
        for token in b_tokens:
            tokens.append(token)
            segment_ids.append(1)
        tokens.append("[SEP]")
        segment_ids.append(1)

    input_ids = tokenizer.convert_tokens_to_ids(tokens)

    # The mask has 1 for real tokens and 0 for padding tokens. Only real
    # tokens are attended to.
    input_mask = [1] * len(input_ids)

    # Zero-pad up to the sequence length.
    if b_tokens:
        pad_length = 3
    else:
        pad_length = 2
    while len(input_ids) < max_seq_length + pad_length:
        input_ids.append(0)
        input_mask.append(0)
        segment_ids.append(0)

    assert len(input_ids) == max_seq_length + pad_length
    assert len(input_mask) == max_seq_length + pad_length
    assert len(segment_ids) == max_seq_length + pad_length

    feature = InputFeatures(
        input_ids=input_ids,
        input_mask=input_mask,
        segment_ids=segment_ids
    )
    return feature, tokens


def infer_batch(a_batch, model, tokenizer, max_seq_len, b_batch=None):
    """
    用一个批次的数据对模型进行训练。
    Args:
        a_batch: 一个批次的样本第一句(required)。
        b_batch: 一个批次的样本第二句(optional)。
        model: 模型(required)。
        tokenizer: 模型(required)。
        max_seq_len: context长度限制(required)。
    Returns:
        预测每个样本。
    """
    # batch_size个InputExample对象
    predict_examples = read_examples(a_batch, b_batch)
    # 转换为batch_size个feature对象
    features, all_tokens = convert_examples_to_features(predict_examples, max_seq_len, tokenizer)

    # input_ids [bs_size, seq_len]
    input_ids = new_tensor([f.input_ids for f in features])
    # input_mask [bs_size, seq_len]
    input_mask = new_tensor([f.input_mask for f in features])
    # segment_ids [bs_size, seq_len]
    segment_ids = new_tensor([f.segment_ids for f in features])
    output = model(input_ids, mask=input_mask, seg=segment_ids)
    return output


class ErnieVectorizer(torch.nn.Module):
    """
    不带head的ernie预训练模型，提取特征向量
    """

    def __init__(self):
        super(ErnieVectorizer, self).__init__()
        # 加载预训练ernie模型
        self.tokenizer = BertTokenizer.from_pretrained("nghuyong/ernie-1.0")
        self.pretrain = BertModel.from_pretrained("nghuyong/ernie-1.0")

    def forward(self, x, mask=None, seg=None):
        sequence_output, pooled_output = self.pretrain(x, attention_mask=mask, token_type_ids=seg)
        return torch.mean(sequence_output, 1)


class ErnieMatch(torch.nn.Module):
    """
    带有全连接head的ernie模型用于微调匹配任务
    """

    def __init__(self):
        super(ErnieMatch, self).__init__()
        # 加载预训练ernie模型
        self.tokenizer = BertTokenizer.from_pretrained("nghuyong/ernie-1.0")
        self.pretrain = BertModel.from_pretrained("nghuyong/ernie-1.0")
        self.dropout = torch.nn.Dropout(0.1)
        self.fc1 = torch.nn.Linear(768, 512)
        self.fc2 = torch.nn.Linear(512, 1)

    def forward(self, x, mask=None, seg=None):
        sequence_output, pooled_output = self.pretrain(x, attention_mask=mask, token_type_ids=seg)
        output = self.dropout(pooled_output)
        output = self.fc1(output)
        output = self.fc2(output).squeeze()
        return output
