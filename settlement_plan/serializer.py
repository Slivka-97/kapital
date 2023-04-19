import datetime
from .models.investment import InvestmentPortfolio, InvestmentPurpose
from .utils import get_year_achievement_goal
from rest_framework import serializers


class InvestmentPurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPurpose
        fields = ('id', 'age', 'initial_sum', 'type', 'period_monthly_invest', 'start_data_invest', 'age_goal_achievement',
                  'average_sum', 'percent_rent_month', 'sum_rent_month', 'investment_portfolio')

    id = serializers.SlugField(read_only=True)
    initial_sum = serializers.IntegerField(required=False)
    percent_rent_month = serializers.IntegerField(default=5)


    def validate(self, data):
        if not data.get('initial_sum'):
            portfolio = InvestmentPortfolio.objects.get(id=data['investment_portfolio'].id)
            data['initial_sum'] = portfolio.fact_price
        return data

    def create(self, validated_data):
        inst_investment_purpose = InvestmentPurpose.objects.get_or_create(
            year_achievement_goal=get_year_achievement_goal(self.data),
            **validated_data
        )
        return inst_investment_purpose[0]


class InvestmentPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPortfolio
        fields = "__all__"

    def validate(self, data):
        if not data.get('year'):
            data['year'] = datetime.date.today()
        return data

    def create(self, validated_data):
        inst = InvestmentPortfolio.objects.get_or_create(**validated_data)
        return inst[0]


class InvestmentPurposeBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPurpose
        fields = "__all__"


