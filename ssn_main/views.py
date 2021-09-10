from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.decorators import permission_classes as check_permission
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from ssn_main.serializers import *


class OwnerPermission(BasePermission):

    def __is_owner(self, obj, request):
        return hasattr(obj, 'creator_id') and obj.creator_id is not None and obj.creator_id is request.user.pk

    def __is_same_user(self, obj, request):
        return obj == CustomUser.objects.get(pk=request.user.pk)

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or self.__is_owner(obj, request) or self.__is_same_user(obj, request)


class IsPossibleToAddAsFriend(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = CustomUser.objects.get(pk=request.user.pk)
        print(user.pk != obj.pk and obj not in user.friends.all(), view.action,'++++++')
        if view.action == 'add_friend':
            return user.pk != obj.pk and obj not in user.friends.all()
        return True


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsPossibleToAddAsFriend]

    @action(detail=True, methods=['get'], name='add_friend')
    def add_friend(self, request, pk=None, *args, **kwargs):
        recipient = User.objects.get(pk=pk)
        self.check_object_permissions(request, obj=recipient)
        FriendRequest.objects.create(sender=CustomUser.objects.get(pk=request.user.pk), recipient=recipient)
        return Response(status=status.HTTP_200_OK)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ('list', 'retrieve'):
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ('add_friend',):
            permission_classes = [permissions.IsAuthenticated, IsPossibleToAddAsFriend]
        else:
            permission_classes = [permissions.IsAuthenticated, OwnerPermission]
        return [permission() for permission in permission_classes]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, OwnerPermission]

    def get_serializer_class(self):
        if self.action == 'like':
            return LikeSerializer
        if self.action == 'comment':
            return CommentSerializer
        else:
            return PostSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ('list', 'retrieve', 'like'):
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, OwnerPermission]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['GET', 'post'], name='like')
    def like(self, request, pk=None, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        if request.method == 'POST':
            liked = post.like.filter(pk=request.user.pk)
            if liked:
                post.like.remove(CustomUser.objects.get(pk=request.user))
            else:
                post.like.add(CustomUser.objects.get(pk=request.user))
        print(post.like.all(),'//////////', request.method)
        serializer = LikeSerializer(post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET', 'post'])
    def comment(self, request, pk=None, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        if request.method == 'POST':
            com = CommentSerializer(data=request.POST, context={'request': request})
            com.is_valid()
            com = com.create(com.validated_data)
            post.comments.add(com)
        serializer = CommentSerializer(post.comments.all(), context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(recipient=self.request.user)

    @action(detail=True, methods=['GET', 'post'])
    def approve_request(self, request, pk=None, *args, **kwargs):
        fr = FriendRequest.objects.get(pk=pk)
        fr.approve_request()
        return Response(status=status.HTTP_200_OK)
