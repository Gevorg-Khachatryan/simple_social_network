from django.urls import reverse


class TestSerializers:

    def test_get_posts(self, cli, posts_model, post_serializer, serializer_context):
        resp = cli.get(reverse('post-list'))

        posts = posts_model.objects.all()
        serialized_posts = post_serializer(posts, context=serializer_context, many=True)

        assert resp.status_code == 200
        assert resp.data.get('results') == serialized_posts.data

    def test_get_users(self, users_model, cli, user_serializer, serializer_context):
        resp = cli.get(reverse('user-list'))

        users = users_model.objects.all().order_by('-pk')
        serialized_users = user_serializer(users, context=serializer_context, many=True)

        assert resp.status_code == 200
        assert resp.data.get('results') == serialized_users.data
