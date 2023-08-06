from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from martor.utils import markdownify, VersionNotCompatible


class SimpleTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user1',
            email='user1@mail.com',
            password='TestEgg@1234',
            is_active=True
        )
        self.client.force_login(self.user)

    def test_form(self):
        response = self.client.get('/test-form-view/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('test_form_view.html')
        self.assertContains(response, 'main-martor-description')
        self.assertContains(response, 'main-martor-wiki')

    @override_settings(MARTOR_ENABLE_CONFIGS={
        'emoji': 'true',  # enable/disable emoji icons.
        'imgur': 'true',  # enable/disable imgur/custom uploader.
        'mention': 'true',  # enable/disable mention
        'jquery': 'true',  # include/revoke jquery (require for admin django)
        'living': 'false',  # enable/disable live updates in preview
        'spellcheck': 'false',  # enable/disable spellcheck in form textareas
        'hljs': 'true',  # enable/disable hljs highlighting in preview
    })
    def test_markdownify(self):
        # Heading
        response = self.client.post(
            '/martor/markdownify/',
            {'content': '# Hello world!'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content.decode('utf-8'),
            '<h1>Hello world!</h1>'
        )

        # Link
        response = self.client.post(
            '/martor/markdownify/',
            {'content': '[python](https://python.web.id)'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content.decode('utf-8'),
            '<p><a href="https://python.web.id">python</a></p>'
        )

        # Image
        response = self.client.post(
            '/martor/markdownify/',
            {'content': '![image](https://imgur.com/test.png)'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content.decode('utf-8'),
            '<p><img alt="image" src="https://imgur.com/test.png" /></p>'
        )

        # # Mention
        # response = self.client.post(
        #     '/martor/markdownify/',
        #     {'content': f'@[{self.user.username}]'}
        # )
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(
        #     response.content.decode('utf-8'),
        #     '...fixme'
        # )

    def test_markdownify_error(self,):
        # This tests that real errors don't raise VersionNotCompatible
        #  errors, which could be misleading.
        try:
            markdownify(None)
        except Exception as e:
            self.assertNotIsInstance(e, VersionNotCompatible)
        else:
            self.fail('no assertion raised')
