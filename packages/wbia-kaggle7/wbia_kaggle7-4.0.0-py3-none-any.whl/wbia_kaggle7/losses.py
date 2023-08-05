# -*- coding: utf-8 -*-
# import matplotlib.pyplot as plt
from fastai.vision import *
from fastai.basic_data import *

# from skimage.util import montage
import torch
from fastai import *

RING_ALPHA = 0.01


@dataclass
class RingLoss(Callback):
    """`Callback` that regroups lr adjustment to seq_len, AR and TAR."""

    learn: Learner
    alpha: float = RING_ALPHA

    def on_loss_begin(self, last_output: Tuple[list, list], **kwargs):
        'Save the extra outputs for later and only returns the true output.'
        self.feature_out = last_output[1]
        return {'last_output': last_output[0]}

    def on_backward_begin(
        self, last_loss: Rank0Tensor, last_input: list, last_target: Tensor, **kwargs
    ):
        x_list = self.feature_out
        ring_list = self.learn.model.module.head.rings
        num_clf = len(ring_list)
        loss = None
        for cc in range(num_clf):
            x = x_list[cc]
            R = ring_list[cc]
            x_norm = x.pow(2).sum(dim=1).pow(0.5)
            diff = torch.mean(torch.abs(x_norm - R.expand_as(x_norm)) ** 2)
            if loss is None:
                loss = diff.mean()
            else:
                loss = loss + diff.mean()
        loss = (self.alpha * loss).sum()
        last_loss += loss
        return {'last_loss': last_loss}


# @dataclass
# class CenterLoss(Callback):
#     "`Callback` that regroups lr adjustment to seq_len, AR and TAR."
#     #Adopted from
#     #https://github.com/KaiyangZhou/pytorch-center-loss/blob/master/center_loss.py
#     learn:Learner
#     alpha:float=0.5
#     lr_cent:float=0.5
#     def on_loss_begin(self, last_output:Tuple[list,list], **kwargs):
#         "Save the extra outputs for later and only returns the true output."
#         self.feature_out = last_output[1]
#         return {'last_output': last_output[0]}

#     def on_backward_begin(self,
#                           last_loss:Rank0Tensor,
#                           last_input:list,
#                           last_target:Tensor,
#                           **kwargs):
#         x_list = self.feature_out
#         labels = last_target.clone().detach().cpu()
#         batch_size = labels.size(0)
#         num_classes = self.learn.model.module.head.num_classes
#         classes = torch.arange(num_classes).long()
#         labels = labels.unsqueeze(1).expand(batch_size, num_classes)
#         centers_list = self.learn.model.module.head.centers
#         num_clf = len(centers_list)
#         loss = None
#         for cc in range(num_clf):
#             x = x_list[cc]
#             centers = centers_list[cc]
#             distmat = torch.pow(x, 2).sum(dim=1, keepdim=True).expand(batch_size, num_classes) + \
#                       torch.pow(centers, 2).sum(dim=1, keepdim=True).expand(num_classes, batch_size).t()
#             distmat.addmm_(1, -2, x, centers.t())
#             mask = labels.eq(classes.expand(batch_size, num_classes))
#             dist = []
#             for i in range(batch_size):
#                 value = distmat[i][mask[i]]
#                 value = value.clamp(min=1e-12, max=1e+12) # for numerical stability
#                 dist.append(value)
#             dist = torch.cat(dist)
#             if loss is None:
#                 loss = dist.mean()
#             else:
#                 loss = loss + dist.mean()
#         if self.alpha != 0.:
#             last_loss += (self.alpha * loss).sum()
#         return {'last_loss': last_loss}


def MultiCE(x, targs):
    loss = None
    list_ = list(x)
    for i in range(len(list_)):
        out = list_[i]
        loss_ = CrossEntropyFlat()(out, targs)
        if loss is None:
            loss = loss_
        else:
            loss += loss_
    return loss
