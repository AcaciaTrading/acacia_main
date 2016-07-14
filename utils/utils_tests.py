from django.contrib.auth.models import User

TEST_USER_USERNAME = "test"
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "password1121"

def create_example_user(
    username=TEST_USER_USERNAME,
    email=TEST_USER_EMAIL,
    password=TEST_USER_PASSWORD
):
    user = User.objects.create_user(username, email, password)
    user.save()
    
def login(self):
    login = self.client.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
    
def logout(self):
    self.client.logout()