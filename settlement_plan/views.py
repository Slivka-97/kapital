from datetime import datetime

from rest_framework import permissions, status
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response

from .models import InvestmentPurpose, InvestmentPortfolio, Compare
from .serializer import InvestmentPurposeSerializer, InvestmentPortfolioSerializer, CompareBaseSerializer
from .service import Calculate


class CalculateView(GenericViewSet):
    queryset = InvestmentPurpose.objects.none()

    def create(self, request, *args, **kwargs):
        result = Calculate.calculate_sum_rent(request.data)
        if error := result.get('error'):
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        return Response(result)


class ListAndCreateInvestmentPurposeView(GenericViewSet):
    serializer_class = InvestmentPurposeSerializer
    queryset = InvestmentPurpose.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': serializer.errors, 'error': True}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_superuser:
            qs = InvestmentPurpose.objects.filter(investment_portfolio__user=self.request.user). \
                select_related('investment_portfolio')

        return qs


class ListAndCreateInvestmentPortfolioView(GenericViewSet):
    queryset = InvestmentPortfolio.objects.all()
    serializer_class = InvestmentPortfolioSerializer

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': serializer.errors, 'error': True}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class UpdateAndListCompareView(GenericViewSet):
    queryset = Compare.objects.all()
    serializer_class = CompareBaseSerializer

    def get_queryset(self):
        qs = Compare.objects.filter(purpose__investment_portfolio__user=self.request.user). \
            select_related('purpose', 'purpose__investment_portfolio')

        return qs

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'detail': serializer.errors, 'error': True}, status=status.HTTP_400_BAD_REQUEST)