from rest_framework import serializers

from .models import InvestmentPurpose, UserInfo
from .models.investment import InvestmentPortfolio
from .utils import get_year_achievement_goal


class InvestmentPurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPurpose
        fields = ('id', 'type', 'period_monthly_invest', 'start_data_invest', 'age_goal_achievement',
                  'average_sum', 'percent_rent_month', 'sum_rent_month',)

    id = serializers.SlugField(read_only=True)
    percent_rent_month = serializers.IntegerField(default=5)


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('user', 'age', 'initial_sum', 'investment_purpose', 'other_info')

    other_info = serializers.CharField(required=False)
    investment_purpose = InvestmentPurposeSerializer()
    initial_sum = serializers.IntegerField(required=False, default=None)

    def validate(self, data):
        if not data['initial_sum']:
            if portfolio := getattr(data['user'], 'user_portfolio', None):
                data['initial_sum'] = portfolio.active_sum
        return data

    def create(self, validated_data):
        investment_purpose = validated_data.pop('investment_purpose')

        inst_investment_purpose = InvestmentPurpose.objects.get_or_create(
            year_achievement_goal=get_year_achievement_goal(self.data),
            **investment_purpose
        )
        inst = UserInfo.objects.get_or_create(investment_purpose=inst_investment_purpose[0], **validated_data)
        return inst[0]


class InvestmentPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentPortfolio
        fields = "__all__"


class UserInfoBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = "__all__"


