import time
import os
import numpy as np
from importlib import import_module
import torch
import torch.nn as nn
from pytorch_pretrained_bert import BertModel, BertTokenizer
from utils import get_time_dif


class Config(object):
    """预测阶段模型配置
    """
    def __init__(self, data_dir):
        self.model_name = 'bert'
        self.class_list = [x.strip() for x in open(data_dir + '/class.txt').readlines()]    # 类别名单
        self.save_path = data_dir + '/saved_dict/' + self.model_name + '.ckpt'              # 保存模型
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')          # 设备
        self.num_classes = len(self.class_list)                                             # 类别数
        self.pad_size = 256                                                                 # 每句话处理成的长度(长切短补)
        self.bert_path = './bert_pretrain'
        self.tokenizer = BertTokenizer.from_pretrained(self.bert_path)
        self.hidden_size = 768

    def build_sequence(self, sequence):
        """对输入的sequence序列预处理，遵循长切短补原则
            1. token embedding阶段：序列首部添加 [CLS] 标记
            2. 中文的bert模型采用全掩方式，所以在长切短补的过程中，补充序列的mask信息全部用0替代，其余的mask信息全部为1
        """
        pad_size = self.pad_size
        token = self.tokenizer.tokenize(sequence.strip())
        # 首部添加[CLS]标记
        token = ['[CLS]'] + token
        token_ids = self.tokenizer.convert_tokens_to_ids(token)
        seq_len = len(token)
        mask = []
        if pad_size:
            # 短补
            if seq_len < pad_size:
                # 补充的mask信息为0
                mask = [1] * len(token_ids) + ([0] * (pad_size - seq_len))
                token_ids += ([0] * (pad_size - seq_len))
            # 长切 
            else:
                mask = [1] * pad_size
                token_ids = token_ids[:pad_size]
                seq_len = pad_size
        return torch.LongTensor([token_ids]).to(self.device), torch.LongTensor([mask]).to(self.device) 

class Model(nn.Module):
    def __init__(self, config):
        super(Model, self).__init__()
        self.bert = BertModel.from_pretrained(config.bert_path)
        for param in self.bert.parameters():
            param.requires_grad = True
        self.fc = nn.Linear(config.hidden_size, config.num_classes)

    def forward(self, x):
        context = x[0]  # 输入的句子
        mask = x[1]  # 对padding部分进行mask，和句子一个size，padding部分用0表示，如：[1, 1, 1, 1, 0, 0]
        _, pooled = self.bert(context, attention_mask=mask, output_all_encoded_layers=False)
        out = self.fc(pooled)
        return out


data_dir = 'data'   #存放类型信息和训练的模型
config = Config(data_dir)
model = Model(config).to(config.device)
model.load_state_dict(torch.load(config.save_path, map_location=config.device))


def prediction_fun(text):
    """输入text进行预测
    Args:
        text: 输入的文本
    Returns:
        label: str, 预测的标签
    """
    label_dict = {
        0: '财经', 1: '房产', 2: '教育', 3: '军事', 4: '科技',
        5: '汽车', 6: '体育', 7: '游戏', 8: '娱乐', 9: '其他'
    }

    data = config.build_sequence(text)
    with torch.no_grad():
        outputs = model(data)
        num = torch.argmax(outputs)
    return label_dict[int(num)]
