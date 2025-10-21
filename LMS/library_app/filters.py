import django_filters
from library_app.models import Member, BorrowedBook

class MemberFilter(django_filters.FilterSet):
    membername = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    phone_number = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Member
        fields = ['membername', 'phone_number']

class BorrowedBookFilter(django_filters.FilterSet):
    membername = django_filters.CharFilter(field_name='member__user__username', lookup_expr='icontains')

    class Meta:
        model = BorrowedBook
        fields = ['membername']
