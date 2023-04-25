from rest_framework import routers

from settlement_plan.views import CalculateView, ListAndCreateInvestmentPurposeView, \
    ListAndCreateInvestmentPortfolioView, UpdateAndListCompareView

router = routers.SimpleRouter()

router.register(r'investment_portfolio', ListAndCreateInvestmentPortfolioView, basename='investment_portfolio_api'),
router.register(r'calculate/sum_rent', CalculateView, basename='calculate_type_invest_api'),
router.register(r'investment_purpose', ListAndCreateInvestmentPurposeView, basename='investment_purpose_api'),
router.register(r'compare', UpdateAndListCompareView, basename='compare_update_for_pk_api'),

urlpatterns = router.urls