from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions


# Create your views here.
class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIViews features"""
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)'
            'Is similar to a traditional django view'
            'Gives you the most control over your application logic'
            'Is mapped manually to URLS'
        ]

        return Response({'message' : 'Hello', 'an_apiview' : an_apiview})

    def post(self, request):
        """Create a hello message with our name"""
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello API {name}'
            return Response({'message' : message})

        else:
            return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        """Handle updating an object"""
        return Response({"method API" : 'PUT'})

    def patch(self, request, pk=None):
        """Handle a partial update"""
        return Response({'method API' : "PATCH"})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'Method API' : 'Delete'})



class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello message"""

        a_viewset = [
        'Uses Actions (list, create, retrieve, update, partial_update)',
        'Automatically maps to URLs using Routers',
        'Provides more functionality with less code'
        ]

        return Response ({'message ViewSet' : 'Hello', 'A  viewset' : a_viewset})


    def create(self, request):
        """Create a new hello message"""
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message ViewSet' : message})
        else:
            return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )


    def retrieve(self, request, pk=None):
        """Handle Getting an object using its ID"""
        return Response({'http_method ViewSet':'GET'})

    def update(self, request, pk=None):
        """Handle Updating an object"""
        return Response({'Http_Method ViewSet':'PUT'})

    def partial_update(self, request, pk=None):
        """Handle updating update of an object"""
        return Response({'http_method ViewSet':'PATCH'})

    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method ViewSet':'DELETE'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle Creating and updating profiles"""

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email')


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles CRUD profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user progile to the logged in user"""
        serializer.save(user_profile = self.request.user)
