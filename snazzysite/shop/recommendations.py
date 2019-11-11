from django.contrib.auth.models import User
from recommends.providers import RecommendationProvider
from recommends.providers import recommendation_registry

from .models import Product, Rating

class ProductRecommendationProvider(RecommendationProvider):
    def get_users(self):
        return User.objects.filter(is_active=True, ratings__isnull=False).distinct()

    def get_items(self):
        return Product.objects.all()

    def get_ratings(self, obj):
        return Rating.objects.filter(product=obj)

    def get_rating_score(self, rating):
        return rating.score    

    def get_rating_user(self, rating):
        return rating.user

    def get_rating_item(self, rating):
        return rating.product

recommendation_registry.register(Rating, [Product], ProductRecommendationProvider)