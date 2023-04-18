from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import InvestmentPurpose, InvestmentPortfolio, UserInfo
from .serializer import UserInfoSerializer, InvestmentPurposeSerializer, InvestmentPortfolioSerializer, \
    UserInfoBaseSerializer
from .utils import Calculate


class PermissionAdmin:
    permission_classes = [permissions.IsAdminUser]


class RecordTypeInvestView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserInfoSerializer

    def post(self, request, *args, **kwargs):
        request.data['investment_purpose']['type'] = kwargs["type_invest"]
        request.data['user'] = request.user.id
        return super().post(request, args, kwargs)


class CalculateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        type_invest = kwargs["type_invest"]
        fun = getattr(Calculate, f'calculate_{type_invest}', None)
        if not fun:
            return Response('type_invest not a valid', status=status.HTTP_400_BAD_REQUEST)

        return Response(data={'hello': fun(data)})


class ListInvestmentPurposeView(PermissionAdmin, ListAPIView):
    queryset = InvestmentPurpose.objects.all()
    serializer_class = InvestmentPurposeSerializer


class ListAndCreateInvestmentPortfolioView(PermissionAdmin, ListCreateAPIView):
    queryset = InvestmentPortfolio.objects.all()
    serializer_class = InvestmentPortfolioSerializer


class ListUserInfoView(PermissionAdmin, ListAPIView):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoBaseSerializer

