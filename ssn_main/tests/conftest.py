from pytest import fixture


@fixture
def users_model():
    from django.contrib.auth.models import User
    return User


@fixture
def custom_users_model():
    from ssn_main.models import CustomUser
    return CustomUser


@fixture
def posts_model():
    from ssn_main.models import Post
    return Post


@fixture
def post_serializer():
    from ssn_main.serializers import PostSerializer
    return PostSerializer


@fixture
def user_serializer():
    from ssn_main.serializers import UserSerializer
    return UserSerializer


@fixture
def cli():
    from django.test import client
    data = {'username': 'user4', 'password': 'useruser'}
    cli = client.Client()
    cli.login(**data)
    return cli


@fixture
def serializer_context():
    from rest_framework.test import APIRequestFactory
    from rest_framework.request import Request
    factory = APIRequestFactory()
    request = factory.get('/')
    serializer_context = {
        'request': Request(request),
    }
    return serializer_context
