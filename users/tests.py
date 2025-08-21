from django.test import TestCase
from .models import User
# to access Recipe model
from django.db import models

# Create your tests here.


class UserModelTest(TestCase):
    def setUpTestData():
        User.objects.create(username='daisyflower')

    def test_username(self):
        # Get a user object to test
        user = User.objects.get(id=1)

        # Get the metadata for the 'username' field and use it to query its data
        field_label = user._meta.get_field('username').verbose_name

        # Compare the value to the expected result
        self.assertEqual(field_label, 'username')
