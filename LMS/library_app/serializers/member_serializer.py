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
        fields = ['id', 'username', 'password', 'user_name', 'joined_date', 'phone_number']

    # def create(self, validated_data):
    #     username = validated_data['username']
    #     password = validated_data['password']
    #     phone_number = validated_data.get('phone_number', '')

    #     user = User.objects.create_user(username=username, password=password)
    #     return Member.objects.create(user=user, phone_number=phone_number)
