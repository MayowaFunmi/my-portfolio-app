from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Project, ContactMe
from .permissions import IsOwner
from .serializers import RegisterSerializer, ListUserSerializer, ProjectSerializer, ContactSerializer, LogoutSerializer


# user registration view


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# user list view
class ListUserView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ListUserSerializer


class ProjectView(generics.CreateAPIView):
    queryset = Project.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProjectSerializer


class ListProjectsView(generics.ListAPIView):
    queryset = Project.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProjectSerializer


class ContactMeView(generics.CreateAPIView):
    queryset = ContactMe.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ContactSerializer


class ListContactMeView(generics.ListAPIView):
    queryset = ContactMe.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ContactSerializer


# logout views
class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
