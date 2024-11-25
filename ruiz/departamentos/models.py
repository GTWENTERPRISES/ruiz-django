from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Apartment(models.Model):
    title = models.CharField("Título", max_length=200)
    description = models.TextField("Descripción")
    price_per_night = models.DecimalField(
        "Precio por noche",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    location = models.CharField("Ubicación", max_length=200)
    bedrooms = models.PositiveIntegerField("Dormitorios")
    bathrooms = models.PositiveIntegerField("Baños")
    max_guests = models.PositiveIntegerField("Máximo de huéspedes")
    contact_phone = models.CharField("Teléfono de contacto", max_length=20)
    is_available = models.BooleanField("Disponible", default=True)
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True)
    updated_at = models.DateTimeField("Última actualización", auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Apartamento"
        verbose_name_plural = "Apartamentos"

    def __str__(self):
        return self.title

class ApartmentImage(models.Model):
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name='apartment_images',
        verbose_name="Apartamento"
    )
    image_url = models.URLField("URL de la imagen")
    order = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Imagen del Apartamento"
        verbose_name_plural = "Imágenes del Apartamento"

class Amenity(models.Model):
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name='apartment_amenities',
        verbose_name="Apartamento"
    )
    name = models.CharField("Nombre", max_length=100)

    class Meta:
        verbose_name = "Amenidad"
        verbose_name_plural = "Amenidades"

    def __str__(self):
        return self.name

class Review(models.Model):
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Apartamento"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    rating = models.PositiveIntegerField(
        "Calificación",
        validators=[MinValueValidator(1)],
        choices=[(i, str(i)) for i in range(1, 6)]
    )
    comment = models.TextField("Comentario")
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['apartment', 'user']
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"

    def __str__(self):
        return f'Reseña de {self.user.username} para {self.apartment.title}'
