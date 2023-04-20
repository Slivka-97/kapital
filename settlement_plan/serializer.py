import datetime
import calendar

from django.db.transaction import atomic

from .models.investment import InvestmentPortfolio, InvestmentPurpose, Compare
from .utils import get_year_achievement_goal
from rest_framework import serializers


class InvestmentPurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPurpose
        fields = ('id', 'age', 'initial_sum', 'type', 'period_monthly_invest', 'start_data_invest', 'age_goal_achievement',
                  'average_sum', 'percent_rent_month', 'sum_rent_month', 'investment_portfolio', 'investment_sum')

    id = serializers.SlugField(read_only=True)
    initial_sum = serializers.IntegerField(required=False)
    percent_rent_month = serializers.IntegerField(default=5)
    investment_sum = serializers.IntegerField(write_only=True)

    def validate(self, data):
        if not data.get('initial_sum'):
            portfolio = InvestmentPortfolio.objects.get(id=data['investment_portfolio'].id)
            data['initial_sum'] = portfolio.fact_price
        return data

    def create(self, validated_data):
        _investment_sum = validated_data.pop('investment_sum')
        inst_investment_purpose = InvestmentPurpose.objects.get_or_create(
            year_achievement_goal=get_year_achievement_goal(self.data),
            **validated_data
        )
        self._create_compare(_investment_sum, inst_investment_purpose[0], validated_data)

        return inst_investment_purpose[0]

    @atomic
    def _create_compare(self, investment_sum, purpose, data):
        lst_compare = list()
        next_month_date = data['start_data_invest']
        month_invest = data['period_monthly_invest'] * 12
        invested_funds_plan = 0
        portfolio_value_end_month_plan = data['initial_sum']
        try:
            for _ in range(month_invest):
                invested_funds_plan += investment_sum
                portfolio_value_end_month_plan += invested_funds_plan

                lst_compare.append(Compare(
                    data=next_month_date,
                    monthly_payment_plan=investment_sum,
                    invested_funds_plan=invested_funds_plan,
                    portfolio_value_end_month_plan=portfolio_value_end_month_plan,
                    average_monthly_value_plan=(portfolio_value_end_month_plan//100)*5,
                    purpose=purpose,
                ))

                days = calendar.monthrange(next_month_date.year, next_month_date.month)[1]
                next_month_date = next_month_date + datetime.timedelta(days=days)

            Compare.objects.bulk_create(lst_compare)
        except BaseException as x:
            raise Exception(x)


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


