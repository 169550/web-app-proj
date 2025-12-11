from rest_framework import generics, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .serializers import UserRegistrationSerializer, ListingSerializer, CategoryTreeSerializer, CategorySerializer, \
    ListingImageSerializer, ReviewSerializer
from django.contrib.auth.models import User
from .models import Listing, Category, ListingImage, Review
from .permissions import IsOwnerOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

class ListingListCreateView(generics.CreateAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(addedBy=self.request.user)


class ListingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsOwnerOrReadOnly]

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.filter(ancestor__isnull=True).prefetch_related('category_set')

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategorySerializer
        return CategoryTreeSerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]


class UserListingListView(generics.ListAPIView):
    serializer_class = ListingSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        user_id = self.kwargs['user_pk']
        return Listing.objects.filter(addedBy_id=user_id)

class ListingImageUploadView(generics.CreateAPIView):
    serializer_class = ListingImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        listing_id = self.kwargs['listing_pk']
        listing = get_object_or_404(Listing, pk=listing_id)
        if listing.addedBy != self.request.user:
            raise PermissionDenied("You cannot add images to someone else's listing!")
        serializer.save(listing=listing)

class ListingImageDeleteView(generics.DestroyAPIView):
    queryset = ListingImage.objects.all()
    permission_classes = [IsAuthenticated]
    def perform_destroy(self, instance):
        if instance.listing.addedBy != self.request.user:
            raise PermissionDenied("This is not your photo!")
        instance.delete()


class CreateReviewView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        listing_id = self.kwargs['listing_pk']
        listing = get_object_or_404(Listing, pk=listing_id)
        user = self.request.user

        if listing.addedBy == user:
            raise serializers.ValidationError("You cannot review yourself!")

        if Review.objects.filter(addedBy=user, listing=listing).exists():
            raise serializers.ValidationError("You have already reviewer this listing!")

        serializer.save(addedBy=user, target_user=listing.addedBy, listing=listing)

class UserReviewsListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        target_user_id = self.kwargs['user_pk']
        return Review.objects.filter(target_user_id=target_user_id)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save()