from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
USER_TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')
def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            'email': 'email@gmail.com',
            'password': 'pass1234',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
         payload = {
        'email': 'email@gmail.com',
        'password': 'pass1234',
        'name': 'Test Name'
        }
         create_user(**payload)
         res = self.client.post(CREATE_USER_URL, payload)

         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        payload = {
        'email': 'email@gmail.com',
        'password': '234',
        'name': 'Test Name'
        }    
        res = self.client.post(CREATE_USER_URL, payload) 
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_authetication_success(self):
        user_details = {
            'email': 'example@gmail.com',
            'password': 'good_passsord123',
            'name': 'test name'
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(USER_TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        
    def test_create_token_bad(self):
        create_user(email='examle@gmail.com', password='goodpass')
        payload = {
            'email': 'email@gmail.com',
            'password': 'badpassword',
        } 
        res = self.client.post(USER_TOKEN_URL, payload)
        self.assertNotIn('token', res.data)  
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_blank_password(self):
        payload = {
            'email': 'email@gmail.com',
            'password': '',
        }     
        res = self.client.post(USER_TOKEN_URL, payload)
        self.assertNotIn('token', res.data)  
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITest(TestCase):

    def setUp(self):
        self.user = create_user(
            email='email@gmail.com',
            name='Test name',
            password='passwordexample1876'
            )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data,{
                          'email': self.user.email,
                          'name': self.user.name
                          })
        
    def test_post_not_allowed(self):
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        payload = {'name': 'New name', 'password': 'updated_password3426'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'] )
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)



            

    




