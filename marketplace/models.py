from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib import admin
from django.core.exceptions import ValidationError


# Create your models here.
class Category(models.Model):
    ancestor = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'ancestors')
    list_select_related = ['ancestor']

    @admin.display(description="Ancestors")
    def ancestors(self, obj):
        current_category = obj.ancestor
        path = []
        while current_category:
            path.append(current_category.name)
            current_category = current_category.ancestor
        return " > ".join(reversed(path))


class Listing(models.Model):
    title = models.CharField(max_length=150)
    price = models.IntegerField(validators=[MinValueValidator(0)])
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    addedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    addedAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'addedBy', 'addedAt', 'updatedAt', 'listingCategory')
    list_select_related = ['cat']
    @admin.display(description="Category")
    def listingCategory(self, obj):
        current_category = obj.cat
        path = []
        while current_category:
            path.append(current_category.name)
            current_category = current_category.ancestor
        return " > ".join(reversed(path))

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='listings_photos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.listing.title}"


class Review(models.Model):
    addedBy = models.ForeignKey(User, related_name='reviews_written', on_delete=models.CASCADE)
    target_user = models.ForeignKey(User, related_name='reviews_received', on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, related_name='reviews', on_delete=models.SET_NULL, null=True)

    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('addedBy', 'listing')

    def clean(self):
        if self.addedBy == self.target_user:
            raise ValidationError("You cannot rate yourself!")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.rating}/5 for {self.target_user} by {self.addedBy}"