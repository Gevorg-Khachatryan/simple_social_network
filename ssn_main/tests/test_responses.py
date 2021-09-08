from django.urls import reverse


class TestSerializers:

    def test_get_post_list(self, cli, posts_model, post_serializer, serializer_context):
        resp = cli.get(reverse('post-list'))

        posts = posts_model.objects.all()
        serialized_posts = post_serializer(posts, context=serializer_context, many=True)

        assert resp.status_code == 200
        assert resp.data.get('results') == serialized_posts.data

    def test_get_user_list(self, users_model, cli, user_serializer, serializer_context):
        resp = cli.get(reverse('user-list'))

        users = users_model.objects.all().order_by('-pk')
        serialized_users = user_serializer(users, context=serializer_context, many=True)

        assert resp.status_code == 200
        assert resp.data.get('results') == serialized_users.data

    def test_get_user_by_id(self, users_model, cli, user_serializer, serializer_context):
        user = users_model.objects.first()
        serialized_user = user_serializer(user, context=serializer_context)

        resp = cli.get(f'/users/{user.pk}/')
        assert resp.status_code == 200
        assert resp.data == serialized_user.data

    def test_get_post_by_id(self, posts_model, cli, post_serializer, serializer_context):
        post = posts_model.objects.first()
        serialized_post = post_serializer(post, context=serializer_context)

        resp = cli.get(f'/posts/{post.pk}/')
        assert resp.status_code == 200
        assert resp.data == serialized_post.data

    def test_delete_post(self, posts_model, cli, post_serializer, serializer_context):
        post = posts_model.objects.first()
        serialized_post = post_serializer(post, context=serializer_context)
        data = serialized_post.data

        resp = cli.delete(f'/posts/{post.pk}/')
        posts_model.objects.create(**{'title': data['title'],
                                      'content': data['content'],
                                      'creator': post.creator})

        assert resp.status_code == 204

    def test_delete_user(self, custom_users_model, cli, user_serializer, serializer_context):
        new_user = custom_users_model.objects.create(**{'username': 'username@#$%^@#$',
                                                        'email': 'test@email.com'})
        new_user.set_password('test_password')
        new_user.save()

        resp = cli.delete(f'/users/{new_user.pk}/')
        user = custom_users_model.objects.filter(pk=new_user.pk).exists()
        assert resp.status_code == 204
        assert user is False

    def test_create_post(self, posts_model, cli, post_serializer, serializer_context):
        resp = cli.post('/posts/', {
            'title': 'title',
            'content': 'description'
        })

        posts_model.objects.get(id=resp.data.get('id')).delete()
        assert resp.status_code == 201

    def test_create_user(self, users_model, cli, user_serializer, serializer_context):
        resp = cli.post('/users/', {
            'username': 'test',
            'email': 'test@email.test',
            'password': 'useruser'
        })
        users_model.objects.get(id=resp.data.get('id')).delete()

        assert resp.status_code == 201

    def test_like(self, cli, posts_model, post_serializer):
        post = posts_model.objects.first()
        old_likes = list(post.like.all())
        resp = cli.post(f'/posts/{post.pk}/like/')
        updated_likes = list(post.like.all())
        assert resp.status_code == 200
        assert old_likes != updated_likes
