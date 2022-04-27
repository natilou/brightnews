from .views import RegisterAPI
from django.urls import path

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
]

# urlpatterns = [
#     path('api-token-auth/', CustomAuthToken.as_view())
# ]