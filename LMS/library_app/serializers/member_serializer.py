from rest_framework import serializers
from library_app.models.member import Member
from django.contrib.auth.models import User

class MemberSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    joined_date = serializers.DateField(read_only=True)
    
    class Meta:
        model = Member
        fields = '__all__'
