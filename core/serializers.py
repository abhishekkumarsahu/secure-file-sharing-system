from rest_framework import serializers
from .models import User, File

class ClientSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='CLIENT',
            is_active=True
        )
        return user

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file']

    def validate_file(self, value):
        allowed_extensions = ['.pptx', '.docx', '.xlsx']
        if not any(value.name.endswith(ext) for ext in allowed_extensions):
            raise serializers.ValidationError("Only .pptx, .docx, .xlsx files are allowed.")
        return value