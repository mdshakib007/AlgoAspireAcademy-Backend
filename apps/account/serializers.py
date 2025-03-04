from rest_framework import serializers
from rest_framework.authentication import authenticate
from apps.account.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, password):
        """Ensures password is at least 8 characters long."""
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return password

    def create(self, validated_data):
        """Creates a new user instance securely."""
        return User.objects.create_user(**validated_data)
        

class UserLoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(required=True)  # Accepts either username or email
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        identifier = attrs.get("identifier")  # Can be username or email
        password = attrs.get("password")

        if not identifier or not password:
            raise serializers.ValidationError("Both fields are required.")

        # Check if identifier is an email or username
        user = User.objects.filter(email=identifier).first() or User.objects.filter(username=identifier).first()

        if not user:
            raise serializers.ValidationError("User not found.")

        authenticated_user = authenticate(username=user.username, password=password)
        if not authenticated_user:
            raise serializers.ValidationError("Invalid credentials.")

        # Return validated user
        attrs["user"] = authenticated_user
        return attrs
    