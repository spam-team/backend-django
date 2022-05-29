from abc import ABC, abstractmethod
import numpy as np


class AbstractSegmenter(ABC):
    @abstractmethod
    def segment(self, img: np.array) -> np.array:
        pass


class WalrusSegment(AbstractSegmenter):
    def segment(self, img: np.array) -> np.array:
        return img
