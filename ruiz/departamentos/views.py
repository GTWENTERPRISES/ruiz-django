from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Apartment, Review
from .serializers import ApartmentSerializer, ReviewSerializer
from rest_framework import generics

class ApartmentCreateView(generics.CreateAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer

    def perform_create(self, serializer):
        # Establece el propietario como el usuario autenticado
        # Puedes comentar o eliminar la siguiente línea si deseas permitir la creación sin autenticación
        serializer.save(owner=self.request.user)

class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['price_per_night', 'created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price_per_night__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_night__lte=max_price)

        # Filter by number of bedrooms
        bedrooms = self.request.query_params.get('bedrooms')
        if bedrooms:
            queryset = queryset.filter(bedrooms=bedrooms)

        # Filter by number of guests
        guests = self.request.query_params.get('guests')
        if guests:
            queryset = queryset.filter(max_guests__gte=guests)

        # Filter by availability
        available = self.request.query_params.get('available')
        if available is not None:
            queryset = queryset.filter(is_available=available.lower() == 'true')

        return queryset

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        apartment = self.get_object()
        reviews = Review.objects.filter(apartment=apartment)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if query:
            queryset = self.queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(location__icontains=query)
            )
        else:
            queryset = self.queryset
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)