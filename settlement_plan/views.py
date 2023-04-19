from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import InvestmentPurpose, InvestmentPortfolio
from .serializer import InvestmentPurposeSerializer, InvestmentPortfolioSerializer
from .utils import Calculate


class MixinPermissionAdmin:
    permission_classes = [permissions.IsAdminUser]


class RecordTypeInvestView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InvestmentPurposeSerializer

    def post(self, request, *args, **kwargs):
        request.data['type'] = kwargs["type_invest"]
        return super().post(request, args, kwargs)


class CalculateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        type_invest = kwargs["type_invest"]
        fun = getattr(Calculate, f'calculate_{type_invest}', None)
        if not fun:
            return Response('type_invest not a valid', status=status.HTTP_400_BAD_REQUEST)

        result = fun(request.data)
        return Response(result)


class ListInvestmentPurposeView(MixinPermissionAdmin, ListAPIView):
    queryset = InvestmentPurpose.objects.all()
    serializer_class = InvestmentPurposeSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_superuser:
            qs = InvestmentPurpose.objects.filter(investment_portfolio__user=self.request.user). \
                select_related('investment_portfolio')

        return qs


class ListAndCreateInvestmentPortfolioView(MixinPermissionAdmin, ListCreateAPIView):
    queryset = InvestmentPortfolio.objects.all()
    serializer_class = InvestmentPortfolioSerializer

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        return super().post(request, args, kwargs)

