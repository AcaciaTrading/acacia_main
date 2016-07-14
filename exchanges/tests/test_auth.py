from django.test import TestCase

from exchanges.apis.auths import get_nonce

# Create your tests here.
class NonceTestCase(TestCase):
    def setUp(self):
        self.auth_string = "auth string"
        self.nonce = get_nonce(self.auth_string)
        
    def test_new_string(self):
        """When get_nonce is supplied a new string, it should return the
        current timestamp and start incrementing.
        """
        new_string = "new string"
        
        timestamp = get_nonce(new_string)
        self.assertTrue(type(timestamp) is int)
        self.assertEqual(get_nonce(new_string), timestamp + 1)
        
    def test_existing_string(self):
        """When get_nonce is called with an existing string, it should return
        a value 1 higher than the previous one.
        """
        old_nonce = self.nonce
        self.nonce = get_nonce(self.auth_string)
        
        self.assertEqual(self.nonce, (old_nonce + 1))