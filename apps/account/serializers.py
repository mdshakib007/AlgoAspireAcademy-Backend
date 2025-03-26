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
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New password and confirm password do not match.")
        if len(attrs['new_password']) < 8:
            raise serializers.ValidationError("New password must be at least 8 characters long.")
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'full_name', 'profile_picture', 'date_of_birth', 
            'phone_number', 't_shirt_size', 'country', 'city', 'organization'
        ]