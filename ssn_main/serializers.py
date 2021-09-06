from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_registration.api.serializers import DefaultRegisterUserSerializer

from ssn_main.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'password']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    like = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ['id', 'url', 'title', 'content', 'creator_id', 'like']

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            validated_data.update({'creator_id': user.id})
        return Post.objects.create(**validated_data)


class RegisterSerializer(DefaultRegisterUserSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.model = CustomUser
        self.Meta.fields = ['username', 'password']
