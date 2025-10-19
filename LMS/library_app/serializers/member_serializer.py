from rest_framework import serializers
from LMS.library_app.models.member import Member

class MemberSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Member
        fields = ['id', 'user_name', 'membership_date', 'is_active']