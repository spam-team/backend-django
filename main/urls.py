from django.urls import path, include
from rest_framework import routers

from .views import WalrusCountView, WalrusImageView, WalrusAreaView


router = routers.DefaultRouter()
router.register('walruses', WalrusImageView)


urlpatterns = [
    path('', include(router.urls)),
    path('count_animals/', WalrusCountView.as_view()),
    path('get_area/<int:image_id>/<str:x>/<str:y>', WalrusAreaView.as_view())
]
