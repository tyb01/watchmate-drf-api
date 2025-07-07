from rest_framework import serializers
from watchlist_app.models import Watchlist, Platform, Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ['watchlist']
        read_only_fields = ['reviewer', 'watchlist']

class WatchlistSerializer(serializers.ModelSerializer):
    review = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='review-detail'
    )

    class Meta:
        model = Watchlist
        fields = "__all__"
        read_only_fields = ['avg_reviews', 'total_reviews']

    def validate(self, data):
        if data['title'] == data['storyline']: 
            raise serializers.ValidationError("Title and storyline cannot be the same.")
        return data

    def validate_title(self, value):
        if not (3 <= len(value) <= 25):
            raise serializers.ValidationError("Title must be between 3 and 25 characters.")
        return value

class PlatformSerializer(serializers.ModelSerializer):
    watchlist = serializers.StringRelatedField(many=True, read_only=True)
    len_platform = serializers.SerializerMethodField()

    class Meta:
        model = Platform
        fields = '__all__'

    def get_len_platform(self, obj):
        return len(obj.name)
