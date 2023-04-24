from datetime import datetime

from rest_framework import permissions, status
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response

from .models import InvestmentPurpose, InvestmentPortfolio, Compare
from .serializer import InvestmentPurposeSerializer, InvestmentPortfolioSerializer, CompareBaseSerializer
from .service import Calculate


class RecordTypeInvestView(GenericViewSet):
    serializer_class = InvestmentPurposeSerializer

    def create(self, request, *args, **kwargs):
        request.data['type'] = kwargs["type_invest"]
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CalculateView(GenericViewSet):
    queryset = InvestmentPurpose.objects.none()

    def create(self, request, *args, **kwargs):
        result = Calculate.calculate_sum_rent(request.data)
        if error := result.get('error'):
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        return Response(result)


class ListInvestmentPurposeView(GenericViewSet):
    queryset = InvestmentPurpose.objects.all()
    serializer_class = InvestmentPurposeSerializer

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
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class ListCompareView(GenericViewSet):
    queryset = Compare.objects.all()
    serializer_class = CompareBaseSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        qs = Compare.objects.filter(purpose__investment_portfolio__user=self.request.user). \
            select_related('purpose', 'purpose__investment_portfolio')

        return qs


class UpdateForPkCompareView(ModelViewSet):
    queryset = Compare.objects.all()
    serializer_class = CompareBaseSerializer

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)


class UpdateCompareView(UpdateForPkCompareView):
    queryset = Compare.objects
    serializer_class = CompareBaseSerializer

    def get_object(self):
        qs = self.get_queryset()
        purpose = self.request.data['purpose']
        data = datetime.strptime(self.request.data['data'], '%Y-%m-%d').date()

        data_year = data.year
        data_month = data.month
        obj = qs.select_related('purpose', 'purpose__investment_portfolio').\
            get(purpose__investment_portfolio__user_id=self.request.user.id, purpose=purpose,
                data__year=data_year, data__month=data_month)

        return obj



