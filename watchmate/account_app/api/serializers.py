from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, style={"input_type": "password"})
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
        }
        
    def save(self):
        if User.objects.filter(email = self.validated_data['email']).exists():
            raise serializers.ValidationError("Email already in use!")
        
        if self.validated_data['password'] !=  self.validated_data['password2']:
            raise serializers.ValidationError("Pass1 and Pass2 must be same!")
        
        account = User(email=self.validated_data['email'] , username = self.validated_data['username'])
        account.set_password(self.validated_data['password'])
        account.save()
        
        return account