import random
from abc import ABC, abstractmethod
from typing import List
import numpy as np


class BasicTransform(ABC):
    def check_images(self, images):
        for im in images:
            if not (isinstance(im, np.ndarray)):
                raise TypeError

    @abstractmethod
    def transform(self, images):
        pass


class DummyTransformation(BasicTransform):
    def transform(self, images: List[np.ndarray]):
        self.check_images(images)
        return images

class Flip(BasicTransform):
    def __init__(self,V=-1,H=1):
        self.V=V
        self.H=H
    def transform(self, images: List[np.ndarray]):
        self.check_images(images)
        res = []
        for im in images:
            res.append(im[::self.V, ::self.H, :])
        return res

class Flip_Vertical(BasicTransform):
    def transform(self, images: List[np.ndarray]):
        self.check_images(images)
        res=[]
        for im in images:
            res.append(im[::-1,:,:])
        return res
class Flip_Horizental(BasicTransform):
    def transform(self, images: List[np.ndarray]):
        self.check_images(images)
        res=[]
        for im in images:
            res.append(im[:,::-1,:])
        return res

class RandomRotation90(BasicTransform):
    def __init__(self,factor=random.randint(0, 3)):
        self.factor=factor

    def transform(self, images: List[np.ndarray]):
        self.check_images(images)
        res=[]
        for im in images:
            switcher = {
                0: im,
                1: np.transpose(im, (1, 0, 2))[:, ::-1, :],
                2: np.transpose(im, (1, 0, 2))[::-1, :, :],
                3: im[::-1,:,:]
            }
            res.append(switcher.get(self.factor))
        return res