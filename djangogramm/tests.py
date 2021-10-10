from django.test import TestCase

from djangogramm.models import DgUser, DgPost


class TestAccount(TestCase):
    """Test djangogramm accounts"""

    def setUp(self):
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
        self.client.post('/accounts/login/', {'username': 'test_wrong_user@test.com', 'password': '12345'})
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
        self.assertEqual(resp.redirect_chain, [('/accounts/signup/done/', 302)])
        user = DgUser.objects.get(email='test_user2@test.com')
        self.assertEqual(user.email, 'test_user2@test.com')
        self.assertEqual(user.is_activated, False)
        self.assertEqual(user.is_active, False)

    def test_user_profile(self):
        """Test user profile page functionality"""
        self.client.login(username='test_user@test.com', password='12345')
        resp = self.client.post(
            '/accounts/profile/',
            {
                'email': 'test_user@test.com',
                'first_name': 'Sebastian',
                'last_name': 'Fettel',
                'bio': 'Test bio'
            }, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.redirect_chain, [('/', 302)])
        user = DgUser.objects.get(email='test_user@test.com')
        self.assertEqual(user.first_name, 'Sebastian')
        self.assertEqual(user.last_name, 'Fettel')
        self.assertEqual(user.bio, 'Test bio')


class TestPosts(TestCase):
    """Test djangogramm posts"""

    def setUp(self):
        # create test user
        test_user = DgUser.objects.create_user('test_user@test.com', '12345')
        test_user.is_active = True
        test_user.is_activated = True
        test_user.save()
        # create test posts
        for i in range(1, 4):  # create 3 test posts
            DgPost.objects.create(
                dg_user=test_user,
                title=f'Test post {i}',
                desc=f'Test post {i} desc'
            )

    def test_posts_list_page(self):
        """Test posts list page."""
        self.client.login(username='test_user@test.com', password='12345')
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)
        last_post = resp.context['object_list'][0]
        self.assertEqual(last_post.title, 'Test post 3')  # 'Test post 3' is the last post!
        self.assertEqual(last_post.desc, 'Test post 3 desc')
        self.assertEqual(last_post.dg_user.email, 'test_user@test.com')
        self.assertEqual(len(resp.context['object_list']), 3)  # total 3 posts

    def test_posts_list_page_no_login(self):
        """Test posts list page without user login"""
        resp = self.client.get('', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.redirect_chain, [('/accounts/login/?next=/', 302)])

    def test_add_post(self):
        """Test add post functionality"""
        self.client.login(username='test_user@test.com', password='12345')
        resp = self.client.post(
            '/posts/create/',
            {
                'title': 'Test post 22',
                'desc': 'Test post 22 desc'
            },
            follow=True
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.redirect_chain, [('/', 302)])
        post = DgPost.objects.get(title='Test post 22')
        self.assertEqual(post.title, 'Test post 22')
        self.assertEqual(post.desc, 'Test post 22 desc')
        self.assertEqual(post.dg_user.email, 'test_user@test.com')

    def test_add_page_no_login(self):
        """Test add post page without user login"""
        resp = self.client.get('/posts/create/', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertRedirects(resp, '/accounts/login/?next=/posts/create/')
