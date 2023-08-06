#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2021/3/1 2:40 下午
# @File  : label_model.py
# @Author: johnson
# @Contact : github: johnson7788
# @Desc  : memnet 模型预测推理
# 依赖包 pip install transformers==3.0.2 torch numpy
import os
import torch
import math
import torch.nn as nn
import numpy as np
import torch.nn.functional as F


class Attention(nn.Module):
    def __init__(self, embed_dim, hidden_dim=None, out_dim=None, n_head=1, score_function='dot_product', dropout=0):
        ''' Attention Mechanism 注意力机制
        :param embed_dim: 嵌入维度; eg: 768
        :param hidden_dim: 隐藏维度; eg: 96
        :param out_dim: 输出维度   eg:300
        :param n_head: num of head (Multi-Head Attention)  head的数量  eg:8
        :param score_function: scaled_dot_product / mlp (concat) / bi_linear (general dot)   eg: mlp， bi_linear， dot_product, scaled_dot_product
        :return (?, q_len, out_dim,)
        '''
        super(Attention, self).__init__()
        if hidden_dim is None:
            hidden_dim = embed_dim // n_head
        if out_dim is None:
            out_dim = embed_dim
        self.embed_dim = embed_dim
        self.hidden_dim = hidden_dim
        self.n_head = n_head
        self.score_function = score_function
        # Q和K的计算
        self.w_k = nn.Linear(embed_dim, n_head * hidden_dim)
        self.w_q = nn.Linear(embed_dim, n_head * hidden_dim)
        # attention的投影层计算
        self.proj = nn.Linear(n_head * hidden_dim, out_dim)
        self.dropout = nn.Dropout(dropout)
        if score_function == 'mlp':
            self.weight = nn.Parameter(torch.Tensor(hidden_dim * 2))
        elif self.score_function == 'bi_linear':
            self.weight = nn.Parameter(torch.Tensor(hidden_dim, hidden_dim))
        else:  # dot_product / scaled_dot_product
            self.register_parameter('weight', None)
        self.reset_parameters()

    def reset_parameters(self):
        """权重初始化"""
        stdv = 1. / math.sqrt(self.hidden_dim)
        if self.weight is not None:
            self.weight.data.uniform_(-stdv, stdv)

    def forward(self, k, q):
        """
        计算MHA， Mutil Head attention
        :param k: 默认输入维度 [batch_size, seq_length, embedding_dim]
        :param q:  [batch_size, seq_length, embedding_dim]
        :return:
        """
        if len(q.shape) == 2:  # q_len missing
            q = torch.unsqueeze(q, dim=1)
        if len(k.shape) == 2:  # k_len missing
            k = torch.unsqueeze(k, dim=1)
        # mb_size 是batch_size
        mb_size = k.shape[0]  # ?
        # k_len和q_len是seq_len
        k_len = k.shape[1]
        q_len = q.shape[1]
        # score: (n_head*?, q_len, k_len,)
        # output: (?, q_len, out_dim,)
        # self.w_k(k)的维度[batch-size,seq_len, n_head * hidden_dim]
        # kx 维度 [batch-size,seq_len, n_head, hidden_dim]
        kx = self.w_k(k).view(mb_size, k_len, self.n_head, self.hidden_dim)
        # 【heads, batch_size, seq_len, hidden_dim】kx.permute(2, 0, 1, 3).contiguous().shape --> torch.Size([8, 16, 55, 96])
        # view(-1, k_len, self.hidden_dim) 合并head和bath_size维度 [heads * batch_size, seq_len,hidden_dim]
        kx = kx.permute(2, 0, 1, 3).contiguous().view(-1, k_len, self.hidden_dim)
        # qx同 kx维度
        qx = self.w_q(q).view(mb_size, q_len, self.n_head, self.hidden_dim)
        qx = qx.permute(2, 0, 1, 3).contiguous().view(-1, q_len, self.hidden_dim)
        #
        if self.score_function == 'dot_product':
            kt = kx.permute(0, 2, 1)
            score = torch.bmm(qx, kt)
        elif self.score_function == 'scaled_dot_product':
            kt = kx.permute(0, 2, 1)
            qkt = torch.bmm(qx, kt)
            score = torch.div(qkt, math.sqrt(self.hidden_dim))
        elif self.score_function == 'mlp':
            # torch.unsqueeze(kx, dim=1) 对kx扩充一个维度, [heads * batch_size, seq_len,hidden_dim]--> [heads * batch_size, 1, seq_len,hidden_dim]
            # expand(-1, q_len, -1, -1)， 把维度2扩充到seq_len维度, [heads * batch_size, seq_len, seq_len,hidden_dim]
            kxx = torch.unsqueeze(kx, dim=1).expand(-1, q_len, -1, -1)
            # torch.unsqueeze(qx, dim=2) -->  [heads * batch_size, seq_len,hidden_dim]  --> [heads * batch_size,seq_len, 1 ,hidden_dim]
            # 把维度3扩充到seq_len维度, [heads * batch_size, seq_len, seq_len,hidden_dim]
            qxx = torch.unsqueeze(qx, dim=2).expand(-1, -1, k_len, -1)
            # kq.shape (n_head*batch_size, q_len, k_len, hidden_dim*2)
            kq = torch.cat((kxx, qxx), dim=-1)
            # kq = torch.unsqueeze(kx, dim=1) + torch.unsqueeze(qx, dim=2)
            # score shape [heads * batch_size, q_len, seq_len]
            score = torch.tanh(torch.matmul(kq, self.weight))
        elif self.score_function == 'bi_linear':
            qw = torch.matmul(qx, self.weight)
            kt = kx.permute(0, 2, 1)
            score = torch.bmm(qw, kt)
        else:
            raise RuntimeError('invalid score_function')
        # score shape  [heads * batch_size, q_len, seq_len]
        score = F.softmax(score, dim=-1)
        # bmm， 批次的batch1和batch2内的矩阵进行批矩阵乘操作 [heads * batch_size, q_len, hidden_dim]
        output = torch.bmm(score, kx)  # (n_head*?, q_len, hidden_dim)
        # torch.split(output, mb_size, dim=0) --> 拆分出8个head，每个维度[batch_size, q_len,hidden_dim], 然后拼接所有n_head
        # output的维度 [batch_size, q_len,hidden_dim *n_head]
        output = torch.cat(torch.split(output, mb_size, dim=0), dim=-1)
        # [batch_size, seq_len, proj_layer_hidden_dim] eg: torch.Size([16, 55, 300])
        output = self.proj(output)  # (?, q_len, out_dim)
        output = self.dropout(output)
        return output, score


class SqueezeEmbedding(nn.Module):
    """
    挤压序列嵌入长度为批次中最长的
    由默认全部一样的默认序列长度，挤压成这个batch中最大的序列长度
    """

    def __init__(self, batch_first=True):
        """
        初始化
        :param batch_first:
        """
        super(SqueezeEmbedding, self).__init__()
        self.batch_first = batch_first

    def forward(self, x, x_len):
        """
        sequence -> sort -> pad and pack -> unpack ->unsort
        由默认全部一样的默认序列长度，挤压成这个batch中最大的序列长度,
        :param x: sequence embedding vectors  未排序的x [batch_size, seq_length]  eg: [16,80]
        :param x_len: numpy/tensor list   x的每个句子的长度 eg:[55,33,30,29,...]
        :return:  x维度 [16,55], 把多余的padding的0挤压出去了
        """
        """排序，从句子长度最长到最短"""
        x_sort_idx = torch.sort(-x_len)[1].long()
        x_unsort_idx = torch.sort(x_sort_idx)[1].long()
        # 长度从大到小排列
        x_len = x_len[x_sort_idx]
        # x也调整成这个排列
        x = x[x_sort_idx]
        """pack 将一个填充过的变长序列 压紧"""
        x_emb_p = torch.nn.utils.rnn.pack_padded_sequence(x, x_len.cpu(), batch_first=self.batch_first)
        """unpack: out, 这个操作和pack_padded_sequence()是相反的。把压紧的序列再填充回来"""
        out = torch.nn.utils.rnn.pad_packed_sequence(x_emb_p, batch_first=self.batch_first)  # (sequence, lengths)
        # unpack回来的序列x, out.shape [batch_size, max_seq_len]
        out = out[0]  #
        """unsort"""
        out = out[x_unsort_idx]
        return out


class Tokenizer(object):
    def __init__(self, max_seq_len, lower=True):
        """
        初始化tokenizer
        :param max_seq_len:  最大序列长度
        :param lower:  是否转换成小写
        """
        self.lower = lower
        self.max_seq_len = max_seq_len
        self.word2idx = {}
        self.idx2word = {}
        self.idx = 1

    def pad_and_truncate(self, sequence, maxlen, dtype='int64', padding='post', truncating='post', value=0):
        """
        对序列进行padding和截取
        :param sequence: 序列id，例如 [2021, 1996, 3095, 2001, 2061, 9202, 2000, 2149, 1012]
        :param maxlen: 最大序列长度
        :param dtype: 数据转换成numpy int64格式
        :param padding: post 还是pre
        :param truncating: post 还是pre
        :param value: 默认填充的值，默认用0填充
        :return: [2021 1996 3095 2001 2061 9202 2000 2149 1012    0    0    0    0    0,    0    0    0    0    0    0    0    0    0    0    0    0    0    0,    0    0    0    0    0    0    0    0    0    0    0    0    0    0,    0    0    0    0    0    0    0    0    0    0    0    0    0    0,    0    0    0    0    0    0    0    0    0    0    0    0    0    0,    0    0    0    0    0    0    0    0    0    0]
        """
        # 初始化创建maxlen序列长度的numpy 列表，
        x = (np.ones(maxlen) * value).astype(dtype)
        if truncating == 'pre':
            # 从前面截断
            trunc = sequence[-maxlen:]
        else:
            # 从后面截断
            trunc = sequence[:maxlen]
        # 截断后的数据转换成numpy
        trunc = np.asarray(trunc, dtype=dtype)
        # 从前还是后面padding
        if padding == 'post':
            x[:len(trunc)] = trunc
        else:
            x[-len(trunc):] = trunc
        return x

    def text_to_sequence(self, text, reverse=False, padding='post', truncating='post', english=False, max_seq_len=70):
        if self.lower:
            text = text.lower()
        if english:
            words = text.split()
        else:
            words = [w for w in text]
        unknownidx = len(self.word2idx) + 1
        sequence = [self.word2idx[w] if w in self.word2idx else unknownidx for w in words]
        if len(sequence) == 0:
            sequence = [0]
        if reverse:
            sequence = sequence[::-1]
        seq = self.pad_and_truncate(sequence, max_seq_len, padding=padding, truncating=truncating)
        return seq


class MemNet(nn.Module):

    def __init__(self, embedding_matrix, device, embed_dim=300, class_num=2):
        self.device = device
        #attention的迭代次数
        self.hops = 3
        super(MemNet, self).__init__()
        self.embed = nn.Embedding.from_pretrained(embedding_matrix, freeze=True)
        self.squeeze_embedding = SqueezeEmbedding(batch_first=True)
        self.attention = Attention(embed_dim, score_function='mlp')
        self.x_linear = nn.Linear(embed_dim, embed_dim)
        self.dense = nn.Linear(embed_dim, class_num)

    def forward(self, inputs):
        text_raw_without_keword_indices, keword_indices = inputs[0], inputs[1]
        memory_len = torch.sum(text_raw_without_keword_indices != 0, dim=-1)
        keword_len = torch.sum(keword_indices != 0, dim=-1)
        nonzeros_keword = keword_len.to(self.device)

        memory = self.embed(text_raw_without_keword_indices)
        memory = self.squeeze_embedding(memory, memory_len)
        keword = self.embed(keword_indices)
        keword = torch.sum(keword, dim=1)
        tmp_data = nonzeros_keword.view(nonzeros_keword.size(0), 1).to(torch.float)
        keword = torch.div(keword, tmp_data)
        x = keword.unsqueeze(dim=1)
        for _ in range(self.hops):
            x = self.x_linear(x)
            out_at, _ = self.attention(memory, x)
            x = out_at + x
        x = x.view(x.size(0), -1)
        out = self.dense(x)
        return out


class LabelComponentModel:
    """
    成分判别模型
    """
    def __init__(self, root_model_path='/data/share/nlp/label/component'):
        # 模型推理
        # 1代表是成分，0代表不是成分
        self.label_list = [0, 1]
        self.label_name = ["不是成分", "是成分"]
        # 模型状态文件
        self.state_dict_path = os.path.join(root_model_path, 'memnet_components_step1400_val_acc0.8947')
        # tokenizer文件
        self.tokenizer_file = os.path.join(root_model_path, 'components_tokenizer.dat')
        # embedding文件
        self.embeeding_file = os.path.join(root_model_path, '300_components_embedding_matrix.dat')
        self.embed_dim = 300
        self.hidden_dim = 300
        self.max_seq_len = 70
        self.class_num = len(self.label_list)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.load_eval_model()

    def load_eval_model(self):
        self.tokenizer = self.load_tokenizer(dat_fname=self.tokenizer_file)
        embedding_matrix = self.load_embedding_matrix(dat_fname=self.embeeding_file)
        self.model = MemNet(embedding_matrix, device=self.device, embed_dim=self.embed_dim, class_num=self.class_num)
        print('加载模型:{0}'.format(self.state_dict_path))
        self.model.load_state_dict(torch.load(self.state_dict_path, map_location=self.device))
        self.model = self.model.to(self.device)
        # 模型评估
        self.model.eval()
        torch.autograd.set_grad_enabled(False)

    def load_embedding_matrix(self, dat_fname):
        """
        :param dat_fname:  缓存文件名字
        :return: embedding_matrix
        """
        print('加载 embedding_matrix:', dat_fname)
        embedding_matrix = torch.load(dat_fname, map_location=self.device)
        return embedding_matrix

    def load_tokenizer(self, dat_fname):
        """
        加载缓存好的tokeniner file
        :param dat_fname:  token 数据文件的名字 eg： 'restaurant_tokenizer.dat'
        :return:
        """
        print('加载 tokenizer 文件:', dat_fname)
        tokenizer = Tokenizer(self.max_seq_len)
        tokenizer.word2idx, tokenizer.idx2word = torch.load(dat_fname, map_location=self.device)
        return tokenizer

    def predict(self, content, keword, start, end):
        """
        单条数据
        :param content: 内容
        :param keword: 成分关键字
        :param start: 成分关键字开始位置索引
        :param end: 成分关键字结束位置索引
        :return:
        """
        if content[start:end] != keword:
            print("请注意keword的关键字的位置信息不准确")
        context_seq = self.tokenizer.text_to_sequence(content,max_seq_len=self.max_seq_len)
        keword_seq = self.tokenizer.text_to_sequence(keword,max_seq_len=self.max_seq_len)
        context_indices = torch.tensor([context_seq], dtype=torch.int64).to(self.device)
        keword_indices = torch.tensor([keword_seq], dtype=torch.int64).to(self.device)

        t_inputs = [context_indices, keword_indices]
        t_outputs = self.model(t_inputs)
        t_probs = F.softmax(t_outputs, dim=-1).cpu().detach().numpy()
        label_idx = t_probs.argmax(axis=-1)
        label_num = self.label_list[label_idx[0]]
        label_name = self.label_name[label_idx[0]]

        if label_num == 1:
            return True
        else:
            return False

    def predict_batch(self, test_data):
        """
        test_data数据格式 [[content,keword, start,end],...]
        eg: [['它含有的茶多酚能有效的阻止一些致癌物质的合成','茶多酚', 4,7],...]
        """
        context_seqs = []
        keword_seqs = []
        for data in test_data:
            content, keword, start, end = data
            context_seq = self.tokenizer.text_to_sequence(content,max_seq_len=self.max_seq_len)
            keword_seq = self.tokenizer.text_to_sequence(keword,max_seq_len=self.max_seq_len)
            context_seqs.append(context_seq)
            keword_seqs.append(keword_seq)
        context_indices = torch.tensor(context_seqs, dtype=torch.int64).to(self.device)
        keword_indices = torch.tensor(keword_seqs, dtype=torch.int64).to(self.device)

        t_inputs = [context_indices, keword_indices]
        t_outputs = self.model(t_inputs)

        t_probs = F.softmax(t_outputs, dim=-1).cpu().detach().numpy()
        label_idx = t_probs.argmax(axis=-1)
        label_num = [self.label_list[idx] for idx in label_idx]

        label_name = [idx == 1 for idx in label_num]
        return label_name


def test_one():
    """
    测试一条数据
    """
    model = LabelComponentModel()
    content = '减少癌症的发生几率，改善癌症的病情。它含有的茶多酚能有效的阻止一些致癌物质的合成，如亚硝酸铵，对癌细胞还有着破坏的作用。'
    keword = '茶多酚'
    start = 22
    end = 25
    label_result = model.predict(content, keword, start, end)
    print(content)
    print(label_result)


def test_batch():
    """
    测试一条数据
    """
    model = LabelComponentModel()
    test_data = [
        ['减少癌症的发生几率，改善癌症的病情。它含有的茶多酚能有效的阻止一些致癌物质的合成，如亚硝酸铵，对癌细胞还有着破坏的作用。', '茶多酚', 22, 25],
        ['也是品牌的产品，购买放心。是秒杀价时购买的。价位合适。是花兰花香型的。家里男生和女生都适用。使用时泡沫丰富，发质丝滑，', '兰花', 22, 25],
        ['减少癌症的发生几率，改善癌症的病情。它含有的茶多酚能有效的阻止一些致癌物质的合成，如亚硝酸铵，对癌细胞还有着破坏的作用。', '茶多酚', 22, 25]
    ]
    label_result = model.predict_batch(test_data)
    for idx, d in enumerate(test_data):
        print("----")
        print(d[0])
        print(label_result[idx])


if __name__ == '__main__':
    test_one()
    # test_batch()