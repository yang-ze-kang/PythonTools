from PIL import Image
from torch.utils import data
import torch
import numpy as np
import os


class DataGenerator(data.Dataset):

    def __init__(self, image_dir, anno_file_path, data_transform=None, labelname_path=None, class_weight=None, mode=None, encoding='utf-8'):
        self.img_dir = image_dir
        self.transform = data_transform
        self.class_weight = class_weight
        self.cls2id = {}
        self.mode = mode
        if labelname_path is not None:
            with open(labelname_path, 'r',encoding=encoding) as f:
                ls = f.readlines()
                for i, l in enumerate(ls):
                    its = l.strip('\n')
                    self.cls2id[its] = i
        imgs_path, imgs_label = [], []
        with open(anno_file_path, 'r', encoding=encoding) as f:
            ls = f.readlines()
            for l in ls:
                path, cls = l.strip('\n').split(' ')[:2]
                if self.img_dir is not None:
                    path = os.path.join(self.img_dir, path)
                imgs_path.append(path)
                if labelname_path is not None:
                    imgs_label.append(self.cls2id[cls])
                else:
                    imgs_label.append(int(cls))
        imgs_path = np.array(imgs_path)
        imgs_label = np.array(imgs_label)
        self.imgs_path = imgs_path
        self.imgs_label = imgs_label

    def get_weighted(self):
        return self.class_weight

    def __len__(self):
        return len(self.imgs_path)

    def __getitem__(self, index):
        img = Image.open(self.imgs_path[index])
        if img.mode != 'RGB':
            img = img.convert('RGB')
        label = self.imgs_label[index]
        if self.transform is not None:
            img = self.transform(img)
        if self.mode == 'anno':
            return self.imgs_path[index].split('/')[-1].split('.')[0], img, label
        return img, label

    @staticmethod
    def collate_fn(batch):
        if len(batch[0]) == 3:
            ids, images, labels = tuple(zip(*batch))
            images = torch.stack(images, dim=0)
            labels = torch.as_tensor(labels)
            return ids, images, labels
        images, labels = tuple(zip(*batch))
        images = torch.stack(images, dim=0)
        labels = torch.as_tensor(labels)
        return images, labels
