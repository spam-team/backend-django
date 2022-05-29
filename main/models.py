import base64

from django.core.files.base import ContentFile
from django.db import models

import numpy as np


class WalrusImage(models.Model):
    img = models.ImageField(upload_to='walruses/')

    segmented_img = models.ImageField(upload_to='segmented/', default='segmented/not-segmented-yet.png')
    walrus_count = models.IntegerField(default=0)
    preload = models.JSONField(default=dict)  # 'centroids'

    @staticmethod
    def from_base64(base64_image: str) -> 'WalrusImage':
        walrus_image = WalrusImage()
        data = ContentFile(base64.b64decode(base64_image))
        file_name = "myphoto.png"
        walrus_image.img.save(file_name, data, save=True)

        return walrus_image

    def save_segmented_image(self, segmented_img: np.array) -> None:
        file = ContentFile(segmented_img)
        self.segmented_img.save('segment.png', file, save=True)
