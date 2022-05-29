import base64
import io
import cv2

from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response

import numpy as np
from PIL import Image

from main.models import WalrusImage
from main.serializers import WalrusCountSerializer, WalrusImageSerializer
from utils.animal_counter import WalrusCounter
from utils.counting import walruses_count_by_click

ANIMAL_COUNTER = {
    'walrus': WalrusCounter()
}


class WalrusCountView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = WalrusCountSerializer

    def _bytes_to_img(self, img_base64: bytes) -> np.array:
        img_base64 = base64.decodebytes(img_base64)
        img = Image.open(io.BytesIO(img_base64))
        img = np.array(img)

        if len(img.shape) > 2 and img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

        return img

    def post(self, request, format=None):
        img_base_64 = request.data['img'].encode('utf-8')

        walrus_image = WalrusImage.from_base64(img_base_64)
        img = self._bytes_to_img(img_base_64)

        counter = ANIMAL_COUNTER[request.data.get('animal_type', 'walrus')]
        count = counter.count_animal(walrus_image, img)

        return Response({
            'count': count
        })


class WalrusAreaView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny, )

    def _bytes_to_img(self, img_base64: bytes) -> np.array:
        img_base64 = base64.decodebytes(img_base64)
        img = Image.open(io.BytesIO(img_base64))
        img = np.array(img)

        if len(img.shape) > 2 and img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

        return img

    def get(self, request, image_id, x, y, format=None):
        x = float(x)
        y = float(y)

        walrus_image = WalrusImage.objects.get(id=image_id)
        centroids = walrus_image.preload['centroids']
        img = cv2.imread(walrus_image.img.path)
        count = walruses_count_by_click(img, centroids, x, y)

        return Response({
            'count': count
        })


class WalrusImageView(viewsets.ReadOnlyModelViewSet):
    queryset = WalrusImage.objects.all()
    serializer_class = WalrusImageSerializer
