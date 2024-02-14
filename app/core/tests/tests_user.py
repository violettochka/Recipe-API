from django.test import TestCase
from django.contrib.auth import get_user_model



class ModelTests(TestCase):

    def test_create_user_with_email(self):
        email = 'example@.com'
        password = 'passwordex1234'
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_normalize_email(self):
        email_expected = [
            ['test1@GMAIL.COm', 'test1@gmail.com'],
            ['Test1@gmail.coM', 'Test1@gmail.com'],
            ['test2@gmaiL.com', 'test2@gmail.com']
        ]
        for email, expected in email_expected:
            user = get_user_model().objects.create_user(email, '3282893')
            self.assertEqual(user.email, expected)

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', '4373')

    def test_superuser_create(self):
        user = get_user_model().objects.create_superuser('test1@gmail.com', '7838')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

