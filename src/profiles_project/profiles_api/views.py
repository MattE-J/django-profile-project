from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models
from . import permissions


# Create your views here.
class HelloApiView(APIView):
    '''
    Test API View
    '''

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        '''Returns a list of APIView features'''

        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put delete',
            'Similar to Django view',
            'gives control over logic',
            'Is mapped manually to URLs',
        ]

        return Response({'message': "hello", 'an_apiview': an_apiview})

    def post(self, request):
        '''create a hello message with our name'''

        serializer = serializers.HelloSerializer(data=request.data)

        # validate
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = "Hello {0}".format(name)

            return Response({'message': message})

        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        '''handles updating an object'''
        # logic for updating goes here
        return Response({'method': 'put'})

    def patch(self, request, pk=None):
        '''partially updates an object w/ given data in req'''
        # logic for updating goes here
        return Response({'method': 'patch'})
    
    def delete(self, request, pk=None):
        '''deletes an object'''

        return Response({'method': 'delete'})

class HelloViewSet(viewsets.ViewSet):
    '''test API viewsets'''

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        '''return a hello message'''
        a_viewset = [
            'Uses actions (list, create, ret, update, partial',
            'Auto maps to URLs using routers',
            'provides more functionality w/ less code'
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        '''create a new hello message'''

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)

            return Response({'message': message})

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request, pk=None):
        '''handles getting an object by its ID'''

        return Response({'htt_method': 'GET'})
    
    def update(self, request, pk=None):
        '''handles updating object'''

        return Response({'http_method': 'PUT'})
    
    def partial_update(self, request, pk=None):
        '''updates part of an object'''

        return Response({'http_method': 'PATCH'})
    
    def destroy(self, request, pk=None):
        '''removes an object'''

        return Response({'http_method': 'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    '''handles creating and updating profiles'''

    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,) # tuple that is immutable (needs comma at end) to specify auth classes being used
    permission_classes = (permissions.UpdateOwnProfile,)

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

class LoginViewSet(viewsets.ViewSet):
    '''checks email and pw and returns an authtoken'''

    serializer_class = AuthTokenSerializer

    def create(self, request):
        '''use the obtainAuthToken APIView to validate and create a token'''

        return ObtainAuthToken().post(request)

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    '''handles creating reading and updating profile feed items'''

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    #if the following IsAuthenticatedOrReadOnly, then non users can still see status but cant update. This way they cant see or update.
    permission_classes = (permissions.PostOwnStatus, IsAuthenticated,) #throws 401 Unauthorized if non user attempts to view

    def perform_create(self, serializer):
        '''sets the user profile to the logged in user'''

        serializer.save(user_profile=self.request.user)