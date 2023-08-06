# -*-coding:utf-8-*-
import torchvision
import torch.nn as nn
import torchvision.models as models


class BaseSimCLRException(Exception):
    """Base exception"""


class InvalidBackboneError(BaseSimCLRException):
    """Raised when the choice of backbone Convnet is invalid."""


class InvalidDatasetSelection(BaseSimCLRException):
    """Raised when the choice of dataset is invalid."""


class model_Pretrian(nn.Module):

    def __init__(self, base_model, linear1_out, linear2_out):
        super(model_Pretrian, self).__init__()
        self.resnet_dict = {"resnet18": models.resnet18(pretrained=False, num_classes=128),
                            "resnet50": models.resnet50(pretrained=False, num_classes=128)}

        self.backbone = self._get_basemodel(base_model)
        dim_mlp = self.backbone.fc.in_features

        # add mlp projection head
        self.backbone.fc = nn.Sequential(nn.Linear(dim_mlp, linear1_out), nn.ReLU(), nn.Linear(linear1_out, linear2_out))

    def _get_basemodel(self, model_name):
        try:
            model = self.resnet_dict[model_name]
        except KeyError:
            raise InvalidBackboneError(
                "Invalid backbone architecture. Check the config file and pass one of: resnet18 or resnet50")
        else:
            return model

    def forward(self, x):
        return self.backbone(x)


class model_SimCLR(nn.Module):

    def __init__(self, base_model, out_dim):
        super(model_SimCLR, self).__init__()
        self.resnet_dict = {"resnet18": models.resnet18(pretrained=False, num_classes=out_dim),
                            "resnet50": models.resnet50(pretrained=False, num_classes=out_dim)}

        self.backbone = self._get_basemodel(base_model)
        dim_mlp = self.backbone.fc.in_features

        # add mlp projection head
        self.backbone.fc = nn.Sequential(nn.Linear(dim_mlp, 2 * dim_mlp), nn.ReLU(), nn.Linear(2 * dim_mlp, out_dim))

    def _get_basemodel(self, model_name):
        try:
            model = self.resnet_dict[model_name]
        except KeyError:
            raise InvalidBackboneError(
                "Invalid backbone architecture. Check the config file and pass one of: resnet18 or resnet50")
        else:
            return model

    def forward(self, x):
        return self.backbone(x)


class model_BIDFC(nn.Module):
    def __init__(self, base_model, out_dim):
        super(model_BIDFC, self).__init__()
        self.out_dim = out_dim
        self.backbone = self.get_resnet(base_model)

    def forward(self, x):
        x = self.backbone(x)
        return x

    def get_resnet(self, name, pretrained=False):
        resnets = {"resnet18": torchvision.models.resnet18(pretrained=pretrained, num_classes=self.out_dim),
                   "resnet50": torchvision.models.resnet50(pretrained=pretrained, num_classes=self.out_dim)}
        if name not in resnets.keys():
            raise KeyError(f"{name} is not a valid ResNet version")
        return resnets[name]


if __name__ == '__main__':
    from torchstat import stat
    model1 = model_SimCLR(base_model="resnet18", out_dim=128)
    model2 = model_BIDFC(base_model='resnet18', out_dim=10)
    model3 = model_Pretrian(base_model="resnet18", linear1_out=512, linear2_out=128)
    print(model1)
    print('-'*100)
    print(model2)
    print('-' * 100)
    print(model3)