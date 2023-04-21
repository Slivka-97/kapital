from datetime import datetime

from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import InvestmentPurpose, InvestmentPortfolio, Compare
from .serializer import InvestmentPurposeSerializer, InvestmentPortfolioSerializer, CompareBaseSerializer
from .utils import Calculate


class MixinPermissionAuthenticated:
    permission_classes = [permissions.IsAuthenticated]


class RecordTypeInvestView(MixinPermissionAuthenticated, CreateAPIView):
    serializer_class = InvestmentPurposeSerializer

    def post(self, request, *args, **kwargs):
        request.data['type'] = kwargs["type_invest"]
        return super().post(request, args, kwargs)


class CalculateView(MixinPermissionAuthenticated,APIView):

    def post(self, request, *args, **kwargs):
        type_invest = kwargs["type_invest"]
        fun = getattr(Calculate, f'calculate_{type_invest}', None)
        if not fun:
            return Response('type_invest not a valid', status=status.HTTP_400_BAD_REQUEST)

        result = fun(request.data)
        if error := result.get('error'):
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        return Response(result)


class ListInvestmentPurposeView(MixinPermissionAuthenticated, ListAPIView):
    queryset = InvestmentPurpose.objects.all()
    serializer_class = InvestmentPurposeSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_superuser:
            qs = InvestmentPurpose.objects.filter(investment_portfolio__user=self.request.user). \
                select_related('investment_portfolio')

        return qs


class ListAndCreateInvestmentPortfolioView(MixinPermissionAuthenticated, ListCreateAPIView):
    queryset = InvestmentPortfolio.objects.all()
    serializer_class = InvestmentPortfolioSerializer

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        return super().post(request, args, kwargs)


class ListCompareView(MixinPermissionAuthenticated, ListAPIView):
    queryset = Compare.objects.all()
    serializer_class = CompareBaseSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_superuser:
            qs = Compare.objects.filter(purpose__investment_portfolio__user=self.request.user). \
                select_related('purpose', 'purpose__investment_portfolio')

        return qs


class UpdateForPkCompareView(MixinPermissionAuthenticated, UpdateAPIView):
    queryset = Compare.objects.all()
    serializer_class = CompareBaseSerializer


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



