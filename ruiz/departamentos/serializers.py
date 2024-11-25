from rest_framework import serializers
from django.db.models import Avg
from .models import Apartment, ApartmentImage, Amenity, Review

class ApartmentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentImage
        fields = ['image_url']

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['name']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']

class ApartmentSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    amenities = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Apartment
        fields = [
            'id', 'title', 'description', 'price_per_night',
            'location', 'bedrooms', 'bathrooms', 'max_guests',
            'contact_phone', 'is_available', 'images', 'amenities',
            'rating', 'reviews_count', 'created_at'
        ]

    def get_images(self, obj):
        return [
            img.image_url for img in obj.apartment_images.all()
        ]

    def get_amenities(self, obj):
        return [
            amenity.name for amenity in obj.apartment_amenities.all()
        ]

    def get_rating(self, obj):
        avg_rating = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg_rating, 1) if avg_rating else 0

    def get_reviews_count(self, obj):
        return obj.reviews.count()

    def create(self, validated_data):
        images_data = self.context['request'].data.getlist('images', [])
        amenities_data = self.context['request'].data.getlist('amenities', [])

        apartment = Apartment.objects.create(**validated_data)

        for idx, image_url in enumerate(images_data):
            ApartmentImage.objects.create(
                apartment=apartment,
                image_url=image_url,
                order=idx
            )

        for amenity_name in amenities_data:
            Amenity.objects.create(
                apartment=apartment,
                name=amenity_name
            )

        return apartment