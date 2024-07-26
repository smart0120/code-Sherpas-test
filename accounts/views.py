import re
from decimal import Decimal
from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer

IBAN_REGEX = re.compile(r'^[A-Z0-9]{15,34}$')

class TransactionFilter(filters.FilterSet):
    transaction_type = filters.CharFilter(field_name="transaction_type")
    start_date = filters.DateFilter(field_name="date", lookup_expr='gte')
    end_date = filters.DateFilter(field_name="date", lookup_expr='lte')

    class Meta:
        model = Transaction
        fields = ['transaction_type', 'start_date', 'end_date']

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    # page_size_query_param = 'page_size'
    max_page_size = 100

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    @action(detail=False, methods=['post'])
    def login_or_create(self, request):
        iban = request.data.get('iban')
        if IBAN_REGEX.match(iban):
            account, created = Account.objects.get_or_create(iban=iban)
            return Response({
                'status': 'login' if not created else 'created',
                'account': AccountSerializer(account).data
            })
        return Response({'status': 'invalid IBAN'})

    @action(detail=True, methods=['post'])
    def account_detail(self, request, pk=None):
        account = self.get_object()
        return Response({
            'account': AccountSerializer(account).data
        })

    @action(detail=True, methods=['post'])
    def deposit(self, request, pk=None):
        account = self.get_object()
        amount = request.data.get('amount')
        if amount:
            try:
                amount = Decimal(amount)
                account.balance += amount
                account.save()
                transaction = Transaction.objects.create(account=account, transaction_type='deposit', amount=amount, balance=account.balance)
                return Response({'status': 'deposit successful'})
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
        return Response({'status': 'invalid request'})

    @action(detail=True, methods=['post'])
    def withdraw(self, request, pk=None):
        account = self.get_object()
        amount = request.data.get('amount')
        if amount:
            try:
                amount = Decimal(amount)
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    transaction = Transaction.objects.create(account=account, transaction_type='withdraw', amount=amount, balance=account.balance)
                    return Response({'status': 'withdrawal successful'})
                else:
                    return Response({'status': 'insufficient funds'})
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
        return Response({'status': 'invalid request'})

    @action(detail=True, methods=['post'])
    def transfer(self, request, pk=None):
        account = self.get_object()
        target_iban = request.data.get('target_iban')
        amount = request.data.get('amount')
        if amount and target_iban:
            try:
                amount = Decimal(amount)
                if account.balance >= amount:
                    if not IBAN_REGEX.match(target_iban) or account.iban == target_iban:
                        return Response({'status': 'invalid target account'})
                    try:
                        target_account = Account.objects.get(iban=target_iban)
                        account.balance -= amount
                        target_account.balance += amount
                        account.save()
                        target_account.save()
                        Transaction.objects.create(account=account, transaction_type='transfer', amount=amount, target_account=target_iban, balance=account.balance)
                        return Response({'status': 'transfer successful'})
                    except Account.DoesNotExist:
                        return Response({'status': 'invalid target account'})
                else:
                    return Response({'status': 'insufficient funds'})
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})
        return Response({'status': 'invalid request'})

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TransactionFilter

    def get_queryset(self):
        account_id = self.request.query_params.get('account', None)
        sort_order = self.request.query_params.get('sort', '-date')
        queryset = self.queryset.filter(account_id=account_id) if account_id else self.queryset
        return queryset.order_by(sort_order)
    

def index(request):
    return render(request, 'index.html')
