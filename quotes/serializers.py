from rest_framework import serializers
from .models import Quote
from django.contrib.auth import get_user_model

User = get_user_model()

class QuoteSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Quote
        fields = ['id', 'text', 'author', 'created_by', 'created_by_username', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_at', 'created_by_username']

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user
