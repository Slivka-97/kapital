from django.urls import path, re_path

from .views import RecordTypeInvestView, CalculateView, ListInvestmentPurposeView, \
    ListAndCreateInvestmentPortfolioView, ListUserInfoView

urlpatterns = [
    re_path(r'^calculate/(?P<type_invest>[a-z_A-Z]+)/$', CalculateView.as_view()),

    re_path('record/(?P<type_invest>[a-z_A-Z]+)/$', RecordTypeInvestView.as_view()),

    path('investment_purpose/', ListInvestmentPurposeView.as_view()),

    path('investment_portfolio/', ListAndCreateInvestmentPortfolioView.as_view()),

    path('user_info/', ListUserInfoView.as_view())

]