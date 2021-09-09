from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_registration.api.serializers import DefaultRegisterUserSerializer

from ssn_main.models import *
from ssn_main.models import CustomUser as User


class FriendRequestListSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'url', 'sender', 'status']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    received_requests = FriendRequestListSerializer(read_only=True, many=True)
    friends = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'friends', 'received_requests', 'password']


class LikeSerializer(serializers.ModelSerializer):
    like = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ['like']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comment = serializers.CharField()
    created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = ['author', 'comment', 'created']

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            validated_data.update({'author_id': user.id})
        return Comment.objects.create(**validated_data)


class PostSerializer(serializers.HyperlinkedModelSerializer):
    like = UserSerializer(read_only=True, many=True)
    comments = CommentSerializer(read_only=True, many=True)
    created = serializers.DateTimeField(read_only=True)
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'url', 'title', 'content', 'creator', 'created', 'like', 'comments']

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


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'url', 'sender', 'status']
        read_only_fields = ['status']
