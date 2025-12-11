from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Listing, Category, ListingImage, Review


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ['id', 'image', 'created_at']

class ListingSerializer(serializers.ModelSerializer):
    images = ListingImageSerializer(many=True, read_only=True)
    class Meta:
        model = Listing
        fields = ['id', 'title', 'images', 'price', 'cat', 'addedBy', 'addedAt', 'updatedAt']
        read_only_fields = ['id', 'addedBy', 'addedAt', 'updatedAt']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'ancestor']


class CategoryTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'ancestor', 'children']

    def get_children(self, obj):
        children = obj.category_set.all()
        return CategoryTreeSerializer(children, many=True).data


class ReviewSerializer(serializers.ModelSerializer):
    addedBy = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'addedBy', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'addedBy', 'created_at']