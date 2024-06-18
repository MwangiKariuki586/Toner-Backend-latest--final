from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['staffid'] = user.staffid
        token['staff_name'] = user.staff_name

        return token
class UserallSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.Department_name', read_only=True)
    location_name = serializers.CharField(source='location.Location_name', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'staff_name', 'staffid','department_name','location_name', 'is_superuser', 'is_active', 'date_joined', 'last_login']
class CustomUserSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True, required=False)
    department_name = serializers.CharField(source='department.Department_name', read_only=True)
    location_name = serializers.CharField(source='location.Location_name', read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id','staffid', 'staff_name', 'department','department_name','location_name', 'location', 'password', 'password_confirmation', 'is_active','is_staff', 'is_superuser','date_joined', 'last_login']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'password_confirmation': {'write_only': True, 'required': False},
        }

   
    def validate(self, data):
        if self.instance:
            # During update
            password = data.get('password')
            password_confirmation = data.get('password_confirmation')
        else:
            # During creation
            password = data.get('password', '')
            password_confirmation = data.get('password_confirmation', '')
            department = data.get('department')
            location = data.get('location')

            if department is None:
                raise serializers.ValidationError("Department is required for user creation.")
            if location is None:
                raise serializers.ValidationError("Location is required for user creation.")

        if password and password != password_confirmation:
            raise serializers.ValidationError("Password and password confirmation do not match.")

        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('password_confirmation', None)  # Remove password_confirmation before saving
        user = CustomUser.objects.create(**validated_data)
        
        if password:
            user.set_password(password)
        else:
            raise serializers.ValidationError("Password is required for user creation.")
        
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('password_confirmation', None)

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update password if provided
        if password:
            instance.set_password(password)

        instance.save()
        return instance
class LoginSerializer(serializers.Serializer):
    staffid = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)

class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()