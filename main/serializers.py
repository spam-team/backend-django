from rest_framework import serializers

from main.models import WalrusImage


class WalrusCountSerializer(serializers.Serializer):
    img = serializers.CharField()
    animal_type = serializers.ChoiceField(['walrus'])


class WalrusImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalrusImage
        fields = ['id', 'img', 'walrus_count', 'segmented_img']


class WalrusAreaSerializer(serializers.Serializer):
    img_id = serializers.IntegerField()
    x = serializers.IntegerField()
    y = serializers.IntegerField()
