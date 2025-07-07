from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from watchlist_app.models import Platform , Watchlist , Review
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class PlatformTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username= "testcase2",
            password="test@123"
        )
        self.token, _ = Token.objects.get_or_create(user = self.user)
        self.stream = Platform.objects.create(
            name =  "Youtube",
            about = "Youtube, the streaming champ!",
            url =  "https://youtube.com/"
        )
        
        
    def test_register_platform(self):
        data = {
            "name" : "Youtube",
            "about" : "Youtube, the streaming champ!",
            "url" : "https://youtube.com/"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        response = self.client.post(reverse('platform-list') , data)
        self.assertEqual(response.status_code , status.HTTP_403_FORBIDDEN)
        
    def test_get_platform(self):

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        response = self.client.get(reverse('platform-detail', args = (self.stream.id,)))
        self.assertEqual(response.status_code , status.HTTP_200_OK)
        
        
class WatchlistTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="user1", password="pass@123")
        self.admin_user = User.objects.create_superuser(username="admin", password="admin@pass")
        self.token,_ = Token.objects.get_or_create(user=self.user)
        self.admin_token,_ = Token.objects.get_or_create(user=self.admin_user)
        
        self.platform = Platform.objects.create(
            name="Netflix",
            about="Streaming movies",
            url="https://netflix.com"
        )
        
        self.watchlist = Watchlist.objects.create(
            title="Movie 1",
            storyline="Good movie",
            platform=self.platform,
            active=True
        )

    def test_get_watchlist(self):
        response = self.client.get(reverse('watchlist-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_watchlist(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {
            "title": "New Movie",
            "storyline": "Interesting",
            "type" : "Movie",
            "platform": self.platform.id,
            "active": True
        }
        response = self.client.post(reverse('watchlist-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_watchlist_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        data = {
            "title": "New Movie",
            "storyline": "Interesting",
            "type" : "Movie",
            "platform": self.platform.id,
            "active": True
        }
        response = self.client.post(reverse('watchlist-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_watchlist_detail(self):
        url = reverse('watchlist-detail', args=(self.watchlist.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        
class ReviewTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="reviewer", password="pass@123")
        self.token , _ = Token.objects.get_or_create(user=self.user)

        self.platform = Platform.objects.create(
            name="Prime Video",
            about="Another platform",
            url="https://primevideo.com"
        )

        self.watchlist = Watchlist.objects.create(
            title="Prime Movie",
            storyline="Very good",
            type = "Movie",
            platform=self.platform,
            active=True
        )

    def test_create_review(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        data = {
            "rating": 4,
            "description": "Great one!",
            "watchlist": self.watchlist.id,
            "active": True
        }
        url = reverse('watchlist-review-create', args=(self.watchlist.id,))
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_reviews_for_watchlist(self):
        url = reverse('watchlist-review-list', args=(self.watchlist.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_permission(self):
        url = reverse('watchlist-review-create', args=(self.watchlist.id,))
        response = self.client.post(url, {"rating": 5, "description": "Nice", "active": True})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_review_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        response = self.client.get("/api/watchlist/reviews/by-user/?username=" + self.user.username)
        
        self.assertEqual(response.status_code , status.HTTP_200_OK)