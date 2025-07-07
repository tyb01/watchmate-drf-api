from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
class RegistrationTest(APITestCase):
    
    def test_registration(self):
        data = {
            "username" : "testcase",
            "email" : "testcase@gmail.com",
            "password" : "testcase@123",
            "password2" : "testcase@123"
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
class LoginLogout(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="testcase1",
            password="Password@123"
        )
        self.token, _ = Token.objects.get_or_create(user=self.user)

            
    def test_login(self):
        data = {
            "username" : "testcase1",
            "password" : "Password@123"
        }
        
        response = self.client.post(reverse('login') , data = data)
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        
    def test_logout(self):
        self.token = Token.objects.get(user__username='testcase1')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code , status.HTTP_200_OK)