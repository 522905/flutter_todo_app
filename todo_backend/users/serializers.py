"""
User serializers for authentication and profile management.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'phone_number', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    tasks_count = serializers.SerializerMethodField()
    completed_tasks_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'phone_number',
            'fcm_token', 'email_notifications', 'whatsapp_notifications', 'push_notifications',
            'tasks_count', 'completed_tasks_count', 'created_at'
        )
        read_only_fields = ('id', 'email', 'created_at')

    def get_tasks_count(self, obj):
        return obj.tasks.filter(deleted_at__isnull=True).count()

    def get_completed_tasks_count(self, obj):
        return obj.tasks.filter(is_completed=True, deleted_at__isnull=True).count()
