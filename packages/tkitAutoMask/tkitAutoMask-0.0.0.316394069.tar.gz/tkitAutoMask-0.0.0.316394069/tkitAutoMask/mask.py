# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import math
from functools import reduce
# import pytorch_lightning as pl
import torch
from torch import nn
import torch.nn.functional as F
import random
import numpy as np
# helpers

def prob_mask_like(t, prob):
    return torch.zeros_like(t).float().uniform_(0, 1) < prob

def mask_with_tokens(t, token_ids):
    """
    用记号遮掩
    """
    init_no_mask = torch.full_like(t, False, dtype=torch.bool)
    mask = reduce(lambda acc, el: acc | (t == el), token_ids, init_no_mask)

    # print("mask",mask)
    return mask

def get_mask_subset_with_prob(mask, prob):
    batch, seq_len, device = *mask.shape, mask.device
    max_masked = math.ceil(prob * seq_len)

    num_tokens = mask.sum(dim=-1, keepdim=True)
    mask_excess = (mask.cumsum(dim=-1) > (num_tokens * prob).ceil())
    mask_excess = mask_excess[:, :max_masked]

    rand = torch.rand((batch, seq_len), device=device).masked_fill(~mask, -1e9)
    _, sampled_indices = rand.topk(max_masked, dim=-1)
    sampled_indices = (sampled_indices + 1).masked_fill_(mask_excess, 0)

    new_mask = torch.zeros((batch, seq_len + 1), device=device)
    new_mask.scatter_(-1, sampled_indices, 1)
    return new_mask[:, 1:].bool()


def get_mask_subset_with_prob_tri(mask, prob,subset_with_prob=True):
    """优化版本  三角形 动态掩盖  对屏蔽的数据进行放弃一部分
    上三角和下三角自动随机选择

    # 添加按照比例 subset_with_prob 掩码
     """
    batch, seq_len, device = *mask.shape, mask.device
    # 自动选择头尾
    if random.choice([0,1])==0:
      a_mask = mask.triu(diagonal=2) # diagonal 设置偏移
    else:
      a_mask = mask.tril(diagonal=-2) # diagonal 设置偏移
    # a_mask.bool()
    mask1=a_mask.bool()

    # print("mask1",mask1)
    
    if subset_with_prob==True:
      # 融合概率mask
      mask2=get_mask_subset_with_prob(mask,prob*2)
      # print("mask2",mask2)
      # print("mask1",mask1)
      a_mask=torch.where(mask1==True,mask1,mask2)
      # a_mask=torch.where(a_mask==False,a_mask,mask2)
      # a_mask=get_mask_subset_with_prob(a_mask,prob)
      return a_mask
    else:
      return mask1

def get_mask_subset_with_prob_diagonal(mask, prob,subset_with_prob=True):
    """优化版本  对角线矩阵掩盖
    迭代中会自动随机掩盖  实现连续多个 掩盖。用于预测片段内容

    # 添加按照比例 subset_with_prob 掩码
     """
    batch, seq_len, device = *mask.shape, mask.device

    x = mask.triu() # diagonal 设置偏移
    diagonal=random.randint(1,int(seq_len/2)) # 生成随机的掩盖长度
    y = mask.tril(diagonal=diagonal) # diagonal 设置偏移
    a_mask=torch.where(y==0,y,x)

    # a_mask.bool()
    mask1=a_mask.bool()

    # print("mask1",mask1)
    
    if subset_with_prob==True:
      # 融合概率mask
      mask2=get_mask_subset_with_prob(mask,prob*2)
      # print("mask2",mask2)
      # print("mask1",mask1)
      a_mask=torch.where(mask1==True,mask1,mask2)
      # a_mask=torch.where(a_mask==False,a_mask,mask2)
      # a_mask=get_mask_subset_with_prob(a_mask,prob)
      return a_mask
    else:
      return mask1
# main class


# main class
class autoMask(nn.Module):
    """
    动态mask数据
    
    示例
    
    >>> from transformers import BertTokenizer
     >>> tokenizer = BertTokenizer.from_pretrained("uer/chinese_roberta_L-2_H-128") 
    # dir(tokenizer)
     >>> tomask = autoMask(
    >>>     # transformer,
     >>>     mask_token_id = tokenizer.mask_token_id,          # the token id reserved for masking
     >>>    pad_token_id = tokenizer.pad_token_id,           # the token id for padding
     >>>    mask_prob = 0.05,           # masking probability for masked language modeling
     >>>    replace_prob = 0.90,        # ~10% probability that token will not be masked, but included in loss, as detailed in the epaper
     >>>    mask_ignore_token_ids = [tokenizer.cls_token_id,tokenizer.eos_token_id]  # other tokens to exclude from masking, include the [cls] and [sep] here
    >>>  )
 
 修改默认的pad和mask_token_id 默认使用https://huggingface.co/uer/chinese_roberta_L-2_H-128/blob/main/vocab.txt
    """
    def __init__(
        self,
        # transformer,
        mask_prob = 0.15,
        replace_prob = 0.9,
        num_tokens = None,
        random_token_prob = 0.,
        mask_token_id = 103,
        pad_token_id = -100,
        mask_ignore_token_ids = [],
        probabilitis = [0.9,0.05,0.05]):
        
        super().__init__()

        # self.transformer = transformer

        # mlm related probabilities
        self.mask_prob = mask_prob
        self.replace_prob = replace_prob

        self.num_tokens = num_tokens
        self.random_token_prob = random_token_prob

        # token ids
        self.pad_token_id = pad_token_id
        self.mask_token_id = mask_token_id
        self.mask_ignore_token_ids = set([*mask_ignore_token_ids, pad_token_id])

        self.probabilitis=probabilitis

    def forward(self, input,indices=False, **kwargs):
        """
        indices :获取mask的索引
        
        """
        # do not mask [pad] tokens, or any other tokens in the tokens designated to be excluded ([cls], [sep])
        # 不要屏蔽[pad]令牌或指定排除的令牌中的任何其他令牌（[cls]、[sep]）
        # also do not include these special tokens in the tokens chosen at random
        # 也不要在随机选择的令牌中包含这些特殊令牌
        no_mask = mask_with_tokens(input, self.mask_ignore_token_ids)
        # mask = get_mask_subset_with_prob(~no_mask, self.mask_prob)

        # 设置每种方案的概率
        
        c=np.random.choice(len(self.probabilitis),1, p=self.probabilitis)
        if c[0]==0:
          # 默认 概率掩盖
          mask = get_mask_subset_with_prob(~no_mask, self.mask_prob)
        elif c[0]==1:
          # 随机上下三角
          mask = get_mask_subset_with_prob_tri(~no_mask, self.mask_prob)
        else:
          # 对角线 相当于 连续掩盖
          mask = get_mask_subset_with_prob_diagonal(~no_mask, self.mask_prob)
        # print("mask结果\n",mask)

        # get mask indices 获取掩码索引
        mask_indices = torch.nonzero(mask, as_tuple=True)

        # mask input with mask tokens with probability of `replace_prob` (keep tokens the same with probability 1 - replace_prob)
        masked_input = input.clone().detach()

        # if random token probability > 0 for mlm
        if self.random_token_prob > 0:
            assert self.num_tokens is not None, 'num_tokens keyword must be supplied when instantiating MLM if using random token replacement'
            random_token_prob = prob_mask_like(input, self.random_token_prob)
            random_tokens = torch.randint(0, self.num_tokens, input.shape, device=input.device)
            random_no_mask = mask_with_tokens(random_tokens, self.mask_ignore_token_ids)
            random_token_prob &= ~random_no_mask
            random_indices = torch.nonzero(random_token_prob, as_tuple=True)
            masked_input[random_indices] = random_tokens[random_indices]

        # [mask] input
        replace_prob = prob_mask_like(input, self.replace_prob)
        # print("replace_prob",replace_prob)
        masked_input = masked_input.masked_fill(mask * replace_prob, self.mask_token_id)

        # mask out any tokens to padding tokens that were not originally going to be masked
        labels = input.masked_fill(~mask, self.pad_token_id)
        if indices==True:
            return masked_input,labels,mask_indices
        else:
            return masked_input,labels
