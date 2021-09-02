import os
from django.urls import reverse
from rest_framework.request import Request
from django.test import client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_social_network.settings')
import django

django.setup()

from django.contrib.auth.models import User
from ssn_main.models import Post
from ssn_main.serializers import PostSerializer, UserSerializer
from rest_framework.test import APIRequestFactory

factory = APIRequestFactory()


class TestSerializers:
    request = factory.get('/')
    serializer_context = {
        'request': Request(request),
    }
    data = {'username': 'user4', 'password': 'useruser'}
    cli = client.Client()
    cli.login(**data)

    def test_get_posts(self):
        resp = self.cli.get(reverse('post-list'))

        posts = Post.objects.all()
        serialized_posts = PostSerializer(posts, context=self.serializer_context, many=True)

        assert resp.data.get('results') == serialized_posts.data
        assert resp.status_code == 200

    def test_get_users(self):
        resp = self.cli.get(reverse('user-list'))

        users = User.objects.all().order_by('-pk')
        serialized_users = UserSerializer(users, context=self.serializer_context, many=True)

        assert resp.data.get('results') == serialized_users.data
        assert resp.status_code == 200
