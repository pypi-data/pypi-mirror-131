# -*- coding: utf-8 -*-
# import matplotlib.pyplot as plt
from fastai.vision import *
from fastai.basic_data import *

# from skimage.util import montage
import torch
from fastai import *
import torchvision
import torch.nn as nn
import torch.nn.functional as F


def get_device():
    return torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


def gem(x, p=3, eps=1e-5):
    return torch.abs(
        F.avg_pool2d(x.clamp(min=eps, max=1e4).pow(p), (x.size(-2), x.size(-1))).pow(
            1.0 / p
        )
    )


class L2Norm(nn.Module):
    def __init__(self):
        super(L2Norm, self).__init__()
        self.eps = 1e-10

    def forward(self, x):
        norm = torch.sqrt(torch.sum(x * x, dim=1) + self.eps)
        x = x / norm.unsqueeze(1).expand_as(x)
        return x


class GeM(nn.Module):
    def __init__(self, p=3, eps=1e-6):
        super(GeM, self).__init__()
        self.p = Parameter(torch.ones(1) * p)
        self.eps = eps

    def forward(self, x):
        return gem(x, p=torch.clamp(self.p, min=0.1), eps=self.eps)

    def __repr__(self):
        return (
            self.__class__.__name__
            + '('
            + 'p='
            + '{:.4f}'.format(self.p.data.tolist()[0])
            + ', '
            + 'eps='
            + str(self.eps)
            + ')'
        )


class GeMConst(nn.Module):
    def __init__(self, p=3.74, eps=1e-6):
        super(GeMConst, self).__init__()
        self.p = p
        self.eps = eps

    def forward(self, x):
        return gem(x, p=self.p, eps=self.eps)

    def __repr__(self):
        return (
            self.__class__.__name__
            + '('
            + 'p='
            + '{:.4f}'.format(self.p)
            + ', '
            + 'eps='
            + str(self.eps)
            + ')'
        )


class WhaleFlukeReshape(nn.Module):
    def __init__(self):
        super(WhaleFlukeReshape, self).__init__()

    def forward(self, x):
        a = x.permute(0, 1, 3, 2)
        s = a.shape
        shape = (s[0], s[1] * s[2], s[3])
        b = a.reshape(shape)
        return b


class WhaleFlukeUnshape(nn.Module):
    def __init__(self, channels):
        super(WhaleFlukeUnshape, self).__init__()
        self.channels = channels

    def forward(self, x):
        s = x.shape
        assert s[1] % self.channels == 0
        shape = (s[0], self.channels, s[1] // self.channels)
        a = x.reshape(shape)
        return a


def make_new_densenet_block(in_feat):
    dense_blocks = nn.Sequential()

    # Each denseblock
    num_features = in_feat
    block_config = (6, 8, 6)
    growth_rate = 16
    bn_size = 4
    drop_rate = 0.5
    memory_efficient = False
    for i, num_layers in enumerate(block_config):
        block = torchvision.models.densenet._DenseBlock(
            num_layers=num_layers,
            num_input_features=num_features,
            bn_size=bn_size,
            growth_rate=growth_rate,
            drop_rate=drop_rate,
            memory_efficient=memory_efficient,
        )
        dense_blocks.add_module('top_denseblock%d' % (i + 1), block)
        num_features = num_features + num_layers * growth_rate
        if i != len(block_config) - 1:
            trans = torchvision.models.densenet._Transition(
                num_input_features=num_features, num_output_features=num_features // 4
            )
            dense_blocks.add_module('top_transition%d' % (i + 1), trans)
            num_features = num_features // 4

    # Final batch norm
    dense_blocks.add_module('top_norm5', nn.BatchNorm2d(num_features))
    return dense_blocks


def make_new_network(num_classes, num_heads, gem_const, pretrained=True):
    print('torch.cuda.is_available:', torch.cuda.is_available())
    network_model = CustomPCBNetwork(
        torchvision.models.densenet201(pretrained=pretrained),
        num_classes,
        num_heads,
        gem_const,
    )
    mutliple = torch.cuda.device_count() > 1
    if mutliple:
        print('Using', torch.cuda.device_count(), 'GPUs!')
        network_model = nn.DataParallel(network_model)
    return network_model, mutliple


class CustomPCBNetwork(nn.Module):
    def __init__(self, new_model, num_classes, num_heads, gem_const):
        super().__init__()
        self.cnn = new_model.features
        self.head = PCBRingHead2(num_classes, 256, num_heads, 1920, gem_const)

    def forward(self, x):
        x = self.cnn(x)
        out = self.head(x)
        return out


class PCBRingHead2(nn.Module):
    def __init__(
        self, num_classes, feat_dim, num_clf=4, in_feat=2048, r_init=1.5, gem_const=3.74
    ):
        super(PCBRingHead2, self).__init__()
        self.eps = 1e-10
        self.num_classes = num_classes
        self.feat_dim = feat_dim
        self.num_clf = num_clf
        self.local_FE_list = nn.ModuleList()
        self.rings = nn.ParameterList()
        self.gem_const = gem_const

        self.total_clf = nn.Sequential(
            nn.Dropout(p=0.5),
            nn.Linear(
                in_features=feat_dim * num_clf, out_features=num_classes, bias=True
            ),
        )

        for i in range(num_clf):
            self.rings.append(nn.Parameter(torch.ones(1).to(get_device()) * r_init))

        for i in range(num_clf):
            assert in_feat == 1920
            in_feat_ = 254
            # feat_size = 6
            # conv_feat_ = 254 * feat_size

            # 660, 660
            # torch.Size([4, 1920, 20, 20]) -> torch.Size([4, 1920, 20, 5])
            # torch.Size([4, 254, 5, 1])
            #
            # 325, 1300
            # torch.Size([4, 1920, 10, 40]) -> torch.Size([4, 1920, 10, 10])
            # torch.Size([4, 254, 2, 2])

            # dense_blocks = make_new_densenet_block(1920).to(get_device())

            # SZH, SZW = 400, 1550
            # dense_blocks = make_new_densenet_block(1920).to(get_device())
            # input_ = torch.rand((4, 3, SZH, SZW)).to(get_device())
            # net = nn.Sequential(
            #     network_model.module.cnn,
            #     dense_blocks,
            #     # nn.AvgPool2d((3, 1)),
            #     # GeM(),
            #     # Flatten(),
            #     WhaleFlukeReshape(),
            #     nn.Conv1d(conv_feat_, conv_feat_, 3),
            #     WhaleFlukeUnshape(in_feat_),
            #     nn.Conv1d(in_feat_, in_feat_, feat_size),
            # ).to(get_device())
            # net = nn.DataParallel(net)
            # x = net(input_)
            # print(x.shape)

            dense_blocks = make_new_densenet_block(in_feat).to(get_device())
            self.local_FE_list.append(
                nn.Sequential(
                    # nn.Dropout(p=0.5),
                    dense_blocks,
                    GeM(),
                    # nn.AvgPool2d((3, 1)),
                    # GeMConst(self.gem_const),
                    # WhaleFlukeReshape(),
                    # nn.Conv1d(conv_feat_, conv_feat_, 3),
                    # WhaleFlukeUnshape(in_feat_),
                    # nn.Conv1d(in_feat_, in_feat_, feat_size),
                    Flatten(),
                    nn.BatchNorm1d(
                        in_feat_,
                        eps=1e-05,
                        momentum=0.1,
                        affine=True,
                        track_running_stats=True,
                    ),
                    nn.Dropout(p=0.5),
                    nn.Linear(in_features=in_feat_, out_features=feat_dim, bias=True),
                    nn.ReLU(inplace=True),
                    nn.BatchNorm1d(
                        feat_dim,
                        eps=1e-05,
                        momentum=0.1,
                        affine=True,
                        track_running_stats=True,
                    ),
                )
            )

        self.local_clf_list = nn.ModuleList()
        for i in range(num_clf):
            self.local_clf_list.append(
                nn.Sequential(
                    nn.Dropout(p=0.5),
                    nn.Linear(in_features=feat_dim, out_features=num_classes, bias=True),
                )
            )

    def forward(self, x):
        assert x.size(3) % self.num_clf == 0
        stripe_w = int(x.size(3) // self.num_clf)
        local_feat_list = []
        local_preds_list = []
        for i in range(self.num_clf):
            local_feat = x[:, :, :, i * stripe_w : (i + 1) * stripe_w]
            local_feat_list.append(self.local_FE_list[i](local_feat))
            local_preds_list.append(self.local_clf_list[i](local_feat_list[i]))
        final_clf = self.total_clf(torch.cat(local_feat_list, dim=1).detach())
        local_preds_list.append(final_clf)
        return local_preds_list, local_feat_list
