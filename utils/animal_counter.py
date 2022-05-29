import numpy as np
import math

from abc import ABC, abstractmethod
from typing import List, Tuple

import cv2
import faiss
from sklearn.cluster import DBSCAN

from main.models import WalrusImage
from utils.segment import AbstractSegmenter, WalrusSegment


class SegmentCounter:
    DEFAULT_SIZE = (1090, 920)

    def _get_mask_points(self, mask: np.array) -> np.array:
        points = np.array([
            (i, j)
            for i in range(mask.shape[0])
            for j in range(mask.shape[1])
            if mask[i, j] != 0
        ])

        return points

    def _get_count_by_area(self, points: np.array) -> int:
        dbscan = DBSCAN(eps=1)
        dbscan.fit(points)

        counts = np.unique(dbscan.labels_, return_counts=True)[1]
        m_count = np.median(counts)
        count = math.ceil(len(points) / m_count)

        return count

    def get_animal_count(self, segment_mask: np.array) -> np.array:
        points = self._get_mask_points(segment_mask)
        count = self._get_count_by_area(points)
        return count


class AbstractAnimalCounter(ABC):
    def __init__(self):
        self.segment_counter = SegmentCounter()

    @abstractmethod
    def get_segmenter(self) -> AbstractSegmenter:
        pass

    def count_animal(self, img: np.array, walrus_image: WalrusImage = None) -> int:
        segmented_image = self.get_segmenter().segment(img)
        count = self.segment_counter.get_animal_count(segmented_image)

        if walrus_image:
            walrus_image.walrus_count = count
            walrus_image.save_segmented_image(segmented_image)

        return count


class WalrusCounter(AbstractAnimalCounter):
    def get_segmenter(self) -> AbstractSegmenter:
        return WalrusSegment()
