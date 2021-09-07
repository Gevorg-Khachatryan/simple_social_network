from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from ssn_main.serializers import *


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'like':
            return LikeSerializer
        else:
            return PostSerializer

    @action(detail=True, methods=['GET', 'post'])
    def like(self, request, pk=None, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        if request.method == 'POST':
            liked = post.like.filter(pk=request.user.pk)
            if liked:
                post.like.remove(request.user)
            else:
                post.like.add(request.user)
                post.save()

        serializer = LikeSerializer(post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
