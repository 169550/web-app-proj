from django.contrib import admin

# Register your models here.
from .models import Listing, Category, CategoryAdmin, ListingAdmin

admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)