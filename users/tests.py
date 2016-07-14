from django.test import TestCase

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils import timezone

from user_sessions.utils.tests import Client

from utils.utils_tests import *

import datetime
import json

# Create your tests here.

class UsernameTestCase(TestCase):
        def setUp(self):
            self.client = Client()
            self.existing_username = "existing_username"
            create_example_user()
            create_example_user(self.existing_username, "j@g.co", "password")
            login(self)
            
        def test_existing_username(self):
            """The username view should return "true" when the
            username exists.
            """
            response = self.client.get(
                reverse('users:username'),
                {'username':self.existing_username}
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, "true")
            
        def test_new_username(self):
            """The username view should return "false" when the username
            doesn't exist.
            """
            response = self.client.get(
                reverse('users:username'),
                {'username':'new_username'}
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, "false")
            
        def test_no_input(self):
            """The username view should return nothing if no input
            is specified.
            """
            response = self.client.get(reverse('users:username'), {})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, "")