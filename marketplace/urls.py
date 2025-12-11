from django.urls import path
from .views import RegisterView, CategoryListCreateView, ListingDetailView, ListingListCreateView, CategoryDetailView, \
    UserListingListView, ListingImageUploadView, ListingImageDeleteView, CreateReviewView, UserReviewsListView, \
    ReviewDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('categories/', CategoryListCreateView.as_view(), name='categories'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('listings/', ListingListCreateView.as_view(), name='listing-list-create'),
    path('listings/<int:pk>/', ListingDetailView.as_view(), name='listing-detail'),
    path('users/<int:user_pk>/listings/', UserListingListView.as_view(), name='user-listings'),
    path('listings/<int:listing_pk>/images/', ListingImageUploadView.as_view(), name='listing-image-upload'),
    path('images/<int:pk>/', ListingImageDeleteView.as_view(), name='listing-image-delete'),
    path('listings/<int:listing_pk>/review/', CreateReviewView.as_view(), name='create-review'),
    path('users/<int:user_pk>/reviews/', UserReviewsListView.as_view(), name='user-reviews'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]