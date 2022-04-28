from .views import RegisterAPI, LoginAPI, RedditPostsList
from django.urls import path
from knox import views


urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', views.LogoutAllView.as_view(), name='logoutall'),
    path('api/<str:subreddit>', RedditPostsList.as_view(), name="get_subreddit_posts")
]

# urlpatterns = [
#     path('api-token-auth/', CustomAuthToken.as_view())
# ]