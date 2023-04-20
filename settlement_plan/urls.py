from django.urls import path, re_path

from .views import RecordTypeInvestView, CalculateView, ListInvestmentPurposeView, \
    ListAndCreateInvestmentPortfolioView, ListCompareView, UpdateForPkCompareView, UpdateCompareView

urlpatterns = [
    path('investment_portfolio/', ListAndCreateInvestmentPortfolioView.as_view(), name='investment_portfolio_api'),
    re_path(r'^calculate/(?P<type_invest>[a-z_A-Z]+)/$', CalculateView.as_view(), name='calculate_type_invest_api'),
    re_path(r'^investment_purpose/(?P<type_invest>[a-z_A-Z]+)/$', RecordTypeInvestView.as_view(),
            name='investment_purpose_type_invest_record'),
    path('investment_purpose/', ListInvestmentPurposeView.as_view(), name='investment_purpose_api'),
    path('compare/', ListCompareView.as_view(), name='compare_api'),
    path('compare/<int:pk>/', UpdateForPkCompareView.as_view(), name='compare_update_for_pk_api'),
    path('compare/update/', UpdateCompareView.as_view(), name='compare_update_api'),

]