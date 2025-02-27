from authentication.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from authentication.util import get_token

class RegisterSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )

    class Meta:
        model = User
        fields = ('id','email', 'password', 're_password')  # Adjust fields as needed
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        """Ensure password and confirm password match"""
        if attrs.get('password') != attrs.pop('re_password', None):
            raise serializers.ValidationError(
                {'password': "Password and Confirm Password don't match."}
            )
        return attrs

    def create(self, validated_data):
        """Use the custom UserManager to create a user"""
        return User.objects.create_user(**validated_data) 
    


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        user = authenticate(email=email, password=password)
        
        if not user:
            raise serializers.ValidationError(detail={"email":"Invalid credentials",
                                                      "password":"Invalid credentials"},code=400)
            
        tokens = get_token(user)
        
        return {"token":tokens}
    

