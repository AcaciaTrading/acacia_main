from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

def new_auth_token():
    try:
        new_user = User.objects.get(username='john')
        token = new_user.auth_token
    except Exception:
        new_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        new_user.save()
        token = Token.objects.create(user=new_user)
        token.save()
        
    return "Token " + str(token.key)