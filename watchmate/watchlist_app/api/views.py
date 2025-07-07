from watchlist_app.models import Watchlist , Platform , Review
from watchlist_app.api.serializers import WatchlistSerializer, PlatformSerializer , ReviewSerializer
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
# from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework import permissions
from watchlist_app.api.permissions import IsAdminOrReviewer , IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
import django_filters.rest_framework

from django.shortcuts import get_object_or_404

class ReviewCreateAV(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_scope = 'review-creation-throttle'
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        user = self.request.user
        movie = get_object_or_404(Watchlist, pk=pk)

        if Review.objects.filter(watchlist=movie, reviewer=user).exists():
            raise ValidationError("You have already reviewed this watchlist")

        rating = serializer.validated_data['rating']
        movie.avg_reviews = (movie.avg_reviews + rating) / 2 if movie.total_reviews else rating
        movie.total_reviews += 1
        movie.save()

        serializer.save(watchlist=movie, reviewer=user)
        

class Reviewlistbyuser(generics.ListAPIView):
    filterset_fields = ['reviewer',]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(reviewer = user)
    
class ReviewlistAV(generics.ListCreateAPIView):
    #queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        movie = Watchlist.objects.get(pk = pk)
        return Review.objects.filter(watchlist = movie)
    
    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        user = self.request.user
        movie = Watchlist.objects.get(pk = pk)
        if not user or not user.is_authenticated:
            raise ValidationError("Authentication required to post a review.")
        review = Review.objects.filter(watchlist = movie,reviewer = user )
        if review.exists():
            raise ValidationError("You have already reviewed this watchlist")
        
        if movie.avg_reviews == 0:
            movie.avg_reviews = serializer.validated_data['rating']
            
        else:
             movie.avg_reviews = (movie.avg_reviews + serializer.validated_data['rating']) / 2
        movie.total_reviews += 1
        movie.save()
        serializer.save(watchlist = movie, reviewer = user)

class ReviewDetailAV(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReviewer]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    

class PlatformVS(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]

    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    
    
    

# class PlatformlistAV(APIView):
#     def get(self,request):
#         lst = Platform.objects.all()
#         serializer = PlatformSerializer(lst , many = True)
#         return Response(serializer.data)


#     def post(self,request):
#         serializer = PlatformSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response ( serializer.errors , status=status.HTTP_400_BAD_REQUEST )
        
        
        

# class PlatformDetailAV(APIView):
#     def get(self,request,pk):
#         try :
#             platform = Watchlist.objects.get(pk = pk)
#         except Platform.DoesNotExist:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
        
#         serialzer = PlatformSerializer(platform)
#         return Response (serialzer.data)
#     def put(self,request,pk):
#         try :
#             platform = Platform.objects.get(pk = pk)
#         except Platform.DoesNotExist:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
        
#         serialzer = PlatformSerializer(platform, data = request.data)
        
#         if serialzer.is_valid():
#             serialzer.save()
#             return Response(serialzer.data)
#         else:
#             return Response(serialzer.error, status=status.HTTP_400_BAD_REQUEST)
        
#     def delete(self,request,pk):
#         platform = Platform.objects.get( pk = pk)
#         platform.delete()
#         return Response({"result" : "Platform Deleted! "}, status= status.HTTP_204_NO_CONTENT)
        
            
            
    
class WatchlistAV(generics.ListCreateAPIView):
    filterset_fields = ['created']
    ordering_fields = ['total_reviews',]
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = WatchlistSerializer
    def get_queryset(self):
        queryset = Watchlist.objects.all()
        platform = self.request.query_params.get('platform')
        if platform is not None:
            queryset = queryset.filter(platform__name=platform)
        return queryset
    
        
        
class WatchlistDetailAV(generics.RetrieveUpdateDestroyAPIView):
    filterset_fields = ['platform', 'active']
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
    permission_classes = [IsAdminOrReadOnly]
    

# Create your views here.
# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == "GET":
#         lst = Movie.objects.all()
#         serializer = MovieSerializer(lst,many = True)
#         return Response(serializer.data)
#     if request.method == 'POST':
#         serializer = MovieSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response ( serializer.errors )
        
# @api_view(['GET', 'PUT' , 'DELETE'])
# def get_movie(request,pk):
#     if request.method == 'GET' :
#         try :
#             movie = Movie.objects.get(pk = pk)
#         except Movie.DoesNotExist:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
        
#         serialzer = MovieSerializer(movie)
#         return Response (serialzer.data)
    
#     if request.method == 'PUT' :
#         try :
#             movie = Movie.objects.get(pk = pk)
#         except Movie.DoesNotExist:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
        
#         serialzer = MovieSerializer(movie, data = request.data)
#         if serialzer.is_valid():
#             serialzer.save()
#             return Response(serialzer.data)
#         else:
#             return Response(serialzer.error, status=status.HTTP_400_BAD_REQUEST)

#     if request.method == 'DELETE':
#         movie = Movie.objects.get( pk = pk)
#         movie.delete()
#         return Response({"result" : "Movie Deleted! "}, status= status.HTTP_204_NO_CONTENT)