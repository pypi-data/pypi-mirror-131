import os
import time
import yaml
import shutil
import random
from PIL import Image
from PIL import ImageFilter

import torch

from torchvision import transforms as TF
from torch.utils.data import Dataset


def save_config_file(model_checkpoints_folder, args):
    if not os.path.exists(model_checkpoints_folder):
        os.makedirs(model_checkpoints_folder)
        with open(os.path.join(model_checkpoints_folder, 'config.yml'), 'w') as outfile:
            yaml.dump(args, outfile, default_flow_style=False)


def save_checkpoint(state, is_best, filename='checkpoint.pth.tar'):
    torch.save(state, filename)
    if is_best:
        shutil.copyfile(filename, 'model_best.pth.tar')


class dataset_SimCLR(Dataset):
    def __init__(self, root):
        self.root = root
        self.imgs_path = self.get_img_paths(root)
        self.transform = TF.Compose(
            [
                TF.Grayscale(3),
                TF.RandomResizedCrop(64, scale=(0.85, 1.0)),
                TF.RandomHorizontalFlip(),
                TF.RandomApply([TF.RandomRotation(30)], p=0.2),
                TF.RandomApply([TF.ColorJitter(0.4, 0.4, 0.4)], p=0.4),
                TF.ToTensor(),
                TF.RandomApply([GaussianNoise()], p=0.2),
                TF.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
            ]
        )

    def __len__(self):
        return len(self.imgs_path)

    def __getitem__(self, item):
        start_time = time.perf_counter()
        path = self.imgs_path[item]
        with open(path, 'rb') as f:
            with Image.open(f) as origin_img:
                origin_img = origin_img.convert('RGB')  ## 如果不使用，convert('RGB')进行转换的话，读出来的图像是RGBA四通道的，A通道为透明通道
                # print('origin_img', origin_img)

        if self.transform is not None:
            img_i = self.transform(origin_img)
            img_j = self.transform(origin_img)

            end_time = time.perf_counter()
            # print('end_time - start_time', end_time - start_time)
            return img_i, img_j

    def get_img_paths(self, root):
        imgs = []
        for subset in os.listdir(root):
            subset_path = os.path.join(root, subset)
            for img_name in os.listdir(subset_path):
                imgs.append(os.path.join(subset_path, img_name))
        random.shuffle(imgs)
        return imgs


class GaussianBlur(object):
    """Gaussian blur augmentation in SimCLR_80% https://arxiv.org/abs/2002.05709"""

    def __init__(self, sigma=[.4, 2.]):
        self.sigma = sigma

    def __call__(self, x):
        sigma = random.uniform(self.sigma[0], self.sigma[1])
        x = x.filter(ImageFilter.GaussianBlur(radius=0.5))
        return x


class GaussianNoise(object):
    """Gaussian Noise Augmentation for tensor"""

    def __init__(self, sigma=0.1):
        self.sigma = sigma

    def __call__(self, img):
        noise = torch.randn(1, img.shape[1], img.shape[2])
        noise = torch.cat([noise, noise, noise], dim=0)
        return torch.clamp(img + self.sigma * noise, 0.0, 1.0)
