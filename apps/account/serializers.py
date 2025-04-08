from rest_framework import serializers
from rest_framework.authentication import authenticate
from apps.account.models import User
from apps.course.models import Course, Module, Lesson, Quiz, Assignment
from apps.enrollment.models import LessonCompletion, Enrollment


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
            'phone_number', 't_shirt_size', 'country', 'city', 'organization',
            'is_private', 'bio', 'portfolio', 'github', 'instagram',
            'linkedin', 'codeforces', 'job_experiences', 'skills',
        ]

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'full_name', 'profile_picture',
            'date_of_birth', 'phone_number', 't_shirt_size', 
            'country', 'city', 'organization', 'is_admin',
            'is_instructor', 'is_verified', 'is_private', 'bio', 
            'portfolio', 'github', 'instagram', 'linkedin', 
            'codeforces', 'job_experiences', 'skills',
        ]


class UserSummarySerializer(serializers.Serializer):
    running_course = serializers.SerializerMethodField()
    completed_courses = serializers.SerializerMethodField()
    completed_course_count = serializers.SerializerMethodField()
    completed_lesson_count = serializers.SerializerMethodField()
    completed_quiz_count = serializers.SerializerMethodField()
    completed_assignment_count = serializers.SerializerMethodField()
    total_course_count = serializers.SerializerMethodField()
    total_lesson_count = serializers.SerializerMethodField()
    total_quiz_count = serializers.SerializerMethodField()
    total_assignment_count = serializers.SerializerMethodField()

    def get_running_course(self, user):
        enrollment = user.enrollments.filter(is_completed=False).select_related('course').first()
        if not enrollment or not enrollment.course:
            return None

        course = enrollment.course
        return {
            "id": course.id,
            "name": course.name,
            "slug": course.slug,
            "image": course.image if course.image else None,
            "progress": float(enrollment.completed_percentage or 0.0),
            "estimate_completion_date": enrollment.estimate_completion_date,
        }

    def get_completed_courses(self, user):
        enrollments = user.enrollments.filter(is_completed=True).select_related('course')
        if not enrollments.exists():
            return []

        return [
            {
                "id": e.course.id,
                "name": e.course.name,
                "slug": e.course.slug,
                "image": e.course.image if e.course.image else None,
                "progress": float(e.completed_percentage or 0.0),
                "completed_at": e.completed_at,
            }
            for e in enrollments if e.course
        ]

    def get_completed_course_count(self, user):
        return user.enrollments.filter(is_completed=True).count()

    def get_completed_lesson_count(self, user):
        return LessonCompletion.objects.filter(enrollment__user=user).count()

    def get_completed_quiz_count(self, user):
        return LessonCompletion.objects.filter(enrollment__user=user, quiz_marks__isnull=False).count()

    def get_completed_assignment_count(self, user):
        return LessonCompletion.objects.filter(enrollment__user=user, assignment_marks__isnull=False).count()

    def get_total_course_count(self, user):
        return Course.objects.count()

    def get_total_lesson_count(self, user):
        return Lesson.objects.count()

    def get_total_quiz_count(self, user):
        return Quiz.objects.count()

    def get_total_assignment_count(self, user):
        return Assignment.objects.count()
