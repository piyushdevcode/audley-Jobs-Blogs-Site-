from django.shortcuts import render
from knox.models import AuthToken
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.response import Response
from api import serializers
from django.contrib.auth.models import User
from .models import Feedback, Post
from rest_framework import permissions, generics
from api.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

#------------ FOR ROOT OF API------------------

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'posts': reverse('post-list', request=request, format=format),
        'feedback': reverse('feedback-list', request=request, format=format),
        'register': reverse('register',request=request,format=format),
        'login' : reverse('login',request=request,format=format),
    })


#-------------- Custom User Login via API -------------
class LoginAPIView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPIView, self).post(request, format=None)

#------------------USER-------------

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

# ----- Registering a user via API--------

class RegisterAPI(generics.GenericAPIView):
    serializer_class = serializers.RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": serializers.UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

#--------------- Posts -------------
class PostList(generics.ListAPIView):
    # Shows only published posts
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    serializer_class = serializers.PostSerializer
    # only authenticated user or admin can modify post
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

#----------------- Feedback ---------

class FeedbackList(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = serializers.FeedbackSerilaizer


class FeedbackDetail(generics.RetrieveAPIView):
    queryset = Feedback.objects.all()
    serializers_class = serializers.FeedbackSerilaizer
