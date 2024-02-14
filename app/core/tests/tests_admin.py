from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client
from decimal import Decimal
from core import models


def create_user(email='exampleemail@gmail.com', password="passwordexample2345"):
    return get_user_model().objects.create_user(email= email, password=password)


class AdminSiteTests(TestCase):
     

    def setUp(self):
          self.client = Client()
          self.admin_user = get_user_model().objects.create_superuser(
               email='admin@gmail.com',
               password ='admin1234',
          )
          self.client.force_login(self.admin_user)
          self.user = get_user_model().objects.create_user(
               email='user1@gmail.com',
               password='user1234',
               name='Test user'
          ) 

    def test_users_list(self):
        url= reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
     
    def test_edit_user_page(self):
         url = reverse('admin:core_user_change', args=[self.user.id])
         res = self.client.get(url)
         self.assertEqual(res.status_code, 200)

    def test_add_user_page(self):
         url = reverse('admin:core_user_add')
         res = self.client.get(url)
         self.assertEqual(res.status_code, 200)

    def test_create_recipe_successfully(self):
         user = get_user_model().objects.create_user(
              'testemail@gmail.com',
              'testpassword1234'
         )
         recipe = models.Recipe.objects.create(
              user=user,
              title='example title',
              descriptions='example description',
              time_minutes = 25,
              price = Decimal('4.25'),
              link = 'example link',      
         )
         self.assertEqual(str(recipe), recipe.title)

    def test_create_tag_successfully(self):
         user = create_user()
         tag = models.Tag.objects.create(
              name="example name",
              user = user,
         )
         self.assertEqual(str(tag), tag.name)

