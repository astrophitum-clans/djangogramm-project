from django.test import TestCase
from django.urls import reverse

from djangogramm.models import DgUser, DgPost, Like


class TestAccount(TestCase):
    """Test djangogramm accounts"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # create test user
        test_user = DgUser.objects.create_user('test_user@test.com', '12345')
        test_user.is_active = True
        test_user.is_activated = True
        test_user.save()

    def test_login_page(self):
        """Test user login page"""
        resp = self.client.get('/accounts/login/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'djangogramm/login.html')

    def test_user_login(self):
        """Test user login functionality"""
        resp = self.client.post('/accounts/login/', {'username': 'test_user@test.com', 'password': '12345'},
                                follow=True)
        self.assertEqual(resp.redirect_chain, [('/', 302)])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['user'].get_username(), 'test_user@test.com')

    def test_user_login_wronguser(self):
        """Test that using the wrong username does not work"""
        self.client.post('/accounts/login/', {'username': 'test_wrong_user@test.com', 'password': '12345'})
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, '/accounts/login/?next=/')

    def test_user_logout(self):
        """Test user logout functionality"""
        self.client.post('/accounts/login/', {'username': 'test_user@test.com', 'password': '12345'})
        resp = self.client.get('/accounts/logout/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'djangogramm/logout.html')
        self.assertEqual(resp.context['user'].get_username(), '')

    def test_user_signup(self):
        """Test signup user functionality"""
        resp = self.client.post(
            '/accounts/signup/',
            {
                'email': 'test_user2@test.com',
                'password1': 'aaaaa11111',
                'password2': 'aaaaa11111'
            },
            follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, '/accounts/signup/done/')
        user = DgUser.objects.get(email='test_user2@test.com')
        self.assertEqual(user.email, 'test_user2@test.com')
        self.assertEqual(user.is_activated, False)
        self.assertEqual(user.is_active, False)

    def test_user_profile(self):
        """Test user profile page functionality"""
        self.client.login(username='test_user@test.com', password='12345')
        resp = self.client.post('/accounts/profile/',
                                {'email': 'test_user@test.com', 'first_name': 'Michail', 'last_name': 'Smith',
                                 'bio': 'Test bio'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, '/')
        user = DgUser.objects.get(email='test_user@test.com')
        self.assertEqual(user.email, 'test_user@test.com')
        self.assertEqual(user.first_name, 'Michail')
        self.assertEqual(user.last_name, 'Smith')
        self.assertEqual(user.bio, 'Test bio')


class TestPosts(TestCase):
    """Test djangogramm posts"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # create test user
        test_user = DgUser.objects.create_user('test_user@test.com', '12345')
        test_user.is_active = True
        test_user.is_activated = True
        test_user.save()
        # create test posts
        for i in range(3):  # create 3 test posts
            DgPost.objects.create(
                dg_user=test_user,
                title=f'Test post {i}',
                desc=f'Test post desc {i}'
            )

    def test_posts_list_page(self):
        """Test posts list page."""
        self.client.login(username='test_user@test.com', password='12345')
        resp = self.client.get(reverse('djangogramm:index'))
        self.assertEqual(resp.status_code, 200)
        post = resp.context['object_list'][0]
        self.assertIn('Test post', post.title)  # 'Test post 3' is the last post!
        self.assertIn('Test post desc', post.desc)
        self.assertEqual(post.dg_user.email, 'test_user@test.com')
        self.assertEqual(len(resp.context['object_list']), 3)  # total 3 posts

    def test_posts_list_page_no_login(self):
        """Test posts list page without user login"""
        resp = self.client.get(reverse('djangogramm:index'), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.redirect_chain, [('/accounts/login/?next=/', 302)])

    def test_add_post(self):
        """Test add post functionality"""
        self.client.login(username='test_user@test.com', password='12345')
        resp = self.client.post(
            reverse('djangogramm:post_create'),
            {
                'title': 'Test post 22',
                'desc': 'Test post 22 desc'
            }, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, '/')
        post = DgPost.objects.get(title='Test post 22')
        self.assertEqual(post.title, 'Test post 22')
        self.assertEqual(post.desc, 'Test post 22 desc')
        self.assertEqual(post.dg_user.email, 'test_user@test.com')

    def test_add_page_no_login(self):
        """Test add post page without user login"""
        resp = self.client.get(reverse('djangogramm:post_create'), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, '/accounts/login/?next=/posts/create/')


class TestNewsAndFollowing(TestCase):
    """Test djangogramm following functionality"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # create users
        test_user = DgUser.objects.create_user('test_user@test.com', '12345')
        test_user.is_active = True
        test_user.is_activated = True
        test_user.save()
        # create user following to test_user
        following_user = DgUser.objects.create_user('following_user@test.com', '12345')
        # add to followers
        following_user.followers.add(test_user)
        # create test posts
        DgPost.objects.create(
            dg_user=test_user,
            title='Test post',
            desc='Test post desc'
        )
        DgPost.objects.create(
            dg_user=following_user,
            title='Following user post',
            desc='Following user post desc'
        )

    def test_news_list_page(self):
        """Test news page that shows only following user`s posts """
        self.client.login(username='test_user@test.com', password='12345')
        resp = self.client.get(reverse('djangogramm:news'))
        self.assertIn(b'Following user post', resp.content)  # Following user post is in test_user news
        self.assertNotIn(b'Test post desc', resp.content)  # Other user posts are not in test_user news
        self.assertEqual(resp.status_code, 200)

    def test_news_list_page_no_login(self):
        """Test news list page without user login"""
        resp = self.client.get(reverse('djangogramm:news'), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.redirect_chain, [(f"/accounts/login/?next={reverse('djangogramm:news')}", 302)])

    def test_following(self):
        """Test following functionality"""
        test_user = DgUser.objects.get(email='test_user@test.com')
        self.client.force_login(test_user)
        third_user = DgUser.objects.create_user('third_user@test.com', '12345')
        resp = self.client.post(reverse('djangogramm:follow', kwargs={'dg_user_id': third_user.id}),
                                {'isfollow': 'follow'})
        self.assertEqual(resp.status_code, 302)
        self.assertIn(test_user, third_user.followers.all())

    def test_unfollowing(self):
        """Test unfollowing functionality"""
        test_user = DgUser.objects.get(email='test_user@test.com')
        self.client.force_login(test_user)
        following_user = DgUser.objects.get(email='following_user@test.com')
        self.assertIn(test_user, following_user.followers.all())  # is follower yet
        resp = self.client.post(
            reverse('djangogramm:follow', kwargs={'dg_user_id': following_user.id}), {'isfollow': 'unfollow'})
        self.assertNotIn(test_user, following_user.followers.all())  # Not follower now
        self.assertEqual(resp.status_code, 302)

    def test_like(self):
        """Test add like to post"""
        test_user = DgUser.objects.get(email='test_user@test.com')
        self.client.force_login(test_user)
        post = DgPost.objects.get(title='Following user post')
        resp = self.client.post(reverse('djangogramm:like', kwargs={'post_id': post.pk}), {'islike': 'like'})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(post.likes.filter(user=test_user).exists())

    def test_unlike(self):
        """Test unlike post"""
        test_user = DgUser.objects.get(email='test_user@test.com')
        self.client.force_login(test_user)
        post_user = DgUser.objects.create_user('post_user@test.com', '12345')
        post = DgPost.objects.create(
            dg_user=post_user,
            title='Test likes post',
            desc='Test likes post desc'
        )
        post.likes.create(user=test_user)
        self.assertTrue(post.likes.filter(user=test_user).exists())  # Like this post yet
        resp = self.client.post(reverse('djangogramm:like', kwargs={'post_id': post.pk}), {'islike': 'unlike'})
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(post.likes.filter(user=test_user).exists())  # Unlike this post
