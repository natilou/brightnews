from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from rest_framework.views import APIView
import praw 
import json

# Constants
LIMIT_QUANTITY_OF_POSTS = 20

# Register API

class RegisterAPI(generics.GenericAPIView): 
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response ({
            "user": UserSerializer(user, context=self.get_serializer_context()).data, 
            "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(LoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

class RedditPostsList(APIView):

    def get(self, request, subreddit, format=None):
        reddit = praw.Reddit(
            user_agent="app user agent",
        )
        responseList = []
        for submission in reddit.subreddit(f"{subreddit}").hot(limit=LIMIT_QUANTITY_OF_POSTS):
            submission_dict = {
                "title": submission.title, 
                "score": submission.score, 
                "post_url": submission.shortlink,
                "article_url": submission.url, 
                "subrredit_name": submission.subreddit.display_name,
                "img_url": submission.preview['images'][0]['source']['url'] if hasattr(submission, 'preview') and 'images' in submission.preview else ""
            }
            responseList.append(submission_dict)

        return HttpResponse(json.dumps(responseList), content_type="application/json")