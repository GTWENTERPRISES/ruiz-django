from django.contrib import admin
from .models import Apartment, ApartmentImage, Amenity, Review

class ApartmentImageInline(admin.TabularInline):
    model = ApartmentImage
    extra = 1

class AmenityInline(admin.TabularInline):
    model = Amenity
    extra = 1

@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'price_per_night', 'bedrooms', 'is_available', 'created_at']
    list_filter = ['is_available', 'bedrooms', 'bathrooms']
    search_fields = ['title', 'description', 'location']
    inlines = [ApartmentImageInline, AmenityInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['apartment', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['apartment__title', 'user__username', 'comment']