from rest_framework import routers

from .views import RecordTypeInvestView, CalculateView, ListInvestmentPurposeView, \
    ListAndCreateInvestmentPortfolioView, ListCompareView, UpdateForPkCompareView, UpdateCompareView

router = routers.SimpleRouter()

router.register(r'investment_portfolio', ListAndCreateInvestmentPortfolioView, basename='investment_portfolio_api'),
router.register(r'compare', ListCompareView, basename='compare_api'),
router.register(r'calculate/sum_rent', CalculateView, basename='calculate_type_invest_api'),
router.register(r'^investment_purpose/(?P<type_invest>[a-z_A-Z]+)/', RecordTypeInvestView, basename='investment_purpose_type_invest_record'),
router.register(r'investment_purpose/', ListInvestmentPurposeView, basename='investment_purpose_api'),
router.register(r'compare/<int:pk>/', UpdateForPkCompareView, basename='compare_update_for_pk_api'),
router.register(r'compare/update/', UpdateCompareView, basename='compare_update_api'),

urlpatterns = router.urls