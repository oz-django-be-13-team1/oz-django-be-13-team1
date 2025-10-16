import django_filters
from .models import Transaction

class TransactionFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    transaction_type = django_filters.CharFilter(field_name = 'transaction_type', lookup_expr = 'iexact')
    min_amount = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    max_amount = django_filters.NumberFilter(field_name='amount', lookup_expr='lte')


    class Meta:
        model = Transaction
        fields = ['end_date', 'transaction_type', 'min_amount', 'max_amount']