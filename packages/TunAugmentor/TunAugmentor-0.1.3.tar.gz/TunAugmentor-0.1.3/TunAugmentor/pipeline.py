import numpy
from TunAugmentor.transformations import BasicTransform
from typing import List

class Pipeline ():
    transformations: List[BasicTransform] = []

    def __init__(self, transformations: List[BasicTransform]):
        for transformation in transformations:
            if not(isinstance(transformation,BasicTransform)):
                raise TypeError
        self.transformations=transformations
    def apply(self,images: List[numpy.ndarray]):
        for transformation in self.transformations:
            images=images+transformation.transform(images)
        return images
