import datetime
import calendar

from django.db.transaction import atomic

from .models.investment import InvestmentPortfolio, InvestmentPurpose, Compare
from rest_framework import serializers


class InvestmentPurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPurpose
        fields = ('id', 'age', 'initial_sum', 'type', 'period_intensity_invest', 'start_data_invest',
                  'age_goal_achievement', 'annual_return_investment', 'percent_rent_month', 'sum_rent_month',
                  'investment_portfolio', 'investment_sum', 'year_achievement_goal')

    id = serializers.SlugField(read_only=True)
    initial_sum = serializers.IntegerField(required=False)
    percent_rent_month = serializers.IntegerField(default=5)
    investment_sum = serializers.IntegerField(write_only=True)
    year_achievement_goal = serializers.IntegerField(required=False)

    def validate(self, data):
        if not data.get('initial_sum'):
            portfolio = InvestmentPortfolio.objects.get(id=data['investment_portfolio'].id)
            data['initial_sum'] = portfolio.fact_price
        return data

    def create(self, validated_data):
        _investment_sum = validated_data.pop('investment_sum')

        inst_investment_purpose = InvestmentPurpose.objects.create(
            year_achievement_goal=InvestmentPurpose.get_year_achievement_goal(self.data)
            if validated_data.get('year_achievement_goal') is None else validated_data.pop('year_achievement_goal'),
            **validated_data
        )
        self._create_compare(_investment_sum, inst_investment_purpose, validated_data)

        return inst_investment_purpose

    @atomic
    def _create_compare(self, investment_sum, purpose, data):
        lst_compare = list()
        next_month_date = data['start_data_invest']
        month_invest = data['period_intensity_invest'] * 12
        invested_funds_plan = 0
        portfolio_value_end_month_plan = data['initial_sum']
        percent_rent_month = data['percent_rent_month']
        try:
            for _ in range(month_invest):
                invested_funds_plan += investment_sum
                portfolio_value_end_month_plan += invested_funds_plan

                lst_compare.append(Compare(
                    data=next_month_date,
                    monthly_payment_plan=investment_sum,
                    invested_funds_plan=invested_funds_plan,
                    portfolio_value_end_month_plan=portfolio_value_end_month_plan, #???
                    average_monthly_value_plan=(portfolio_value_end_month_plan / 100) * (percent_rent_month / 12),
                    purpose=purpose,
                ))

                days = calendar.monthrange(next_month_date.year, next_month_date.month)[1]
                next_month_date = next_month_date + datetime.timedelta(days=days)

            Compare.objects.bulk_create(lst_compare)
        except Exception as ex:
            raise Exception(ex)


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


class CompareBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compare
        fields = "__all__"

    purpose = serializers.SlugField(required=False)

    def update(self, instance, validated_data):
        try:
            monthly_payment_fact = validated_data['monthly_payment_fact']
            invested_funds_fact = instance.get_sum_invested_funds_fact(InvestmentPurpose.objects.get(id=instance.purpose.id))
            instance.invested_funds_fact = invested_funds_fact + monthly_payment_fact
            portfolio_value_end_month_fact = instance.purpose.initial_sum + invested_funds_fact + monthly_payment_fact
            instance.portfolio_value_end_month_fact = portfolio_value_end_month_fact
            instance.monthly_payment_fact = monthly_payment_fact
            instance.average_monthly_value_fact = (portfolio_value_end_month_fact//100)*5

            instance.save()
        except Exception as ex:
            raise Exception(ex)

        return instance


class CalculateSerializer(serializers.Serializer):

    class Meta:
        fields = ('age', 'initial_sum', 'percent_rent_month', 'sum_rent_month', 'year_achievement_goal',
                  'annual_return_investment', 'investment_sum', 'period_intensity_invest')

    age = serializers.IntegerField(required=True)
    initial_sum = serializers.IntegerField(required=True)
    percent_rent_month = serializers.IntegerField(required=True)
    annual_return_investment = serializers.IntegerField(required=True)
    year_achievement_goal = serializers.IntegerField(required=False)
    investment_sum = serializers.IntegerField(required=False)
    period_intensity_invest = serializers.IntegerField(required=False)
    sum_rent_month = serializers.IntegerField(required=False)



